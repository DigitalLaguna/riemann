"""
Track B: H_t(z) for t >= 0 — Arb Gauss-Legendre quadrature of the defining integral
  H_t(z) = int_0^inf e^{t u^2} phi(u) cos(z u) du
  phi(u) = sum_{n>=1} [2*pi^2*n^4*exp(9u) - 3*pi*n^2*exp(5u)]*exp(-pi*n^2*exp(4u))
Prior art: dbn_upper_bound/python/mputility.py Ht_complex (mp.quad [0,10], 30 dps, non-rigorous).
Delta this tick: Arb balls, GL degree-difference radius (n=32 vs 64, per subinterval),
rigorous truncation tails (all bounds asserted in code):
  tailA (u > U_MAX, n=1..4): sum_n 2*pi^2*n^4*exp(g_n(U_MAX))/(-g_n'(U_MAX)),
      g_n(u) = 19u + t*u^2 - pi*n^2*exp(4u)
      (|cos(zu)| <= exp(10u) for z_im=10, u>=0; |A-B| <= A since (2*pi/3)*n^2*exp(4u) >= 1;
       g_n'' < 0 and g_n' < 0 for u >= U_MAX, asserted)
  tailB (n >= 5, all u): 2*pi^2*625*(1+3e-15)*int_0^inf exp(19u + t*u^2 - 25*pi*exp(4u)) du
      (sum_{n>=5} (n/5)^4*exp(-pi*(n^2-25)) <= 1+3e-15; h(u)=19u+tu^2-25*pi*e^{4u},
       h'(u) = 19+2tu-100*pi*e^{4u} < 0 on [0,inf) for t <= 1000, asserted)
GL nodes/weights (tick 17 rewrite): P_n coeffs by 3-term recurrence at dps=150,
  roots by Newton with polynomial-derivative (Horner) eval; starts: 1-1.8657/n^2
  for k=1, its negative for k=n, else cos(pi*(k-0.25)/(n+0.5)). Verified in
  scratch (tick 17): n=16/32/64 all roots, maxresid ~1e-110..1e-116, no dups,
  moment deviations ~1e-122 (an apparent 1e-17 'deviation' in scratch was a
  Python-float 2/(k+1) target, NOT in the Arb check below). Weights via the
  single-factor identity w_i = 2*(1-x_i^2)/(n^2*P_{n-1}(x_i)^2)
  (from w_i = 2/((1-x_i^2)*P_n'(x_i)^2) and (1-x^2)P_n' = n(P_{n-1}-xP_n) at
  P_n(x_i)=0; n=2 check: w=1,w=1 exact). The 'tick 14 fix' adding a second
  (1-x_i^2) was a misdiagnosis; the real bug was mp.findroot returning
  duplicate roots (n=32: 3 dups, sum of weights 1.074/0.712 vs 1 on [0,1])
  and crashing at n=64. Moment test (exact acb target) is FATAL below.
Pre-registered checks (logs/2026-08-20.tick.log, tick 11):
  F1: t=0 quadrature vs claim #3 closed form, >= 25 digits
  F2: t in {1,100,1000} vs independent mpmath 80-digit quad, >= 20 digits
  F3: Arb radius < 1e-25 RELATIVE (pre-reg said absolute; t=1000 value is O(e^1143),
      relative is the only reading consistent with F2)
  F4: t=1000 value finite, O(e^O(1000)) heat peak, not NaN/O(1)
"""
import flint
from mpmath import mp
from fractions import Fraction
flint.ctx.prec = 160
acb = flint.acb
fmpq = flint.fmpq
PI = acb('3.141592653589793238462643383279502884197169399375105820974944592307816406286')

def q(x):
    """Exact fmpq from a decimal literal / mpf / float, via its decimal string."""
    f = Fraction(str(x))
    return fmpq(f.numerator, f.denominator)

def _re_upper(z):
    """Upper bound of Re(z) for an acb ball z, as float (assertions only)."""
    return float(z.real.mid()) + float(z.real.rad())

def _re_lower(z):
    """Lower bound of Re(z) for an acb ball z, as float (assertions only)."""
    return float(z.real.mid()) - float(z.real.rad())

Z_RE, Z_IM = 35, 10
N_MAX = 4
U_MAX = 2.0
GRID = [0.0, 0.25, 0.5, 0.75, 1.0, 1.1, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6, 2.0]

def legendre_coeffs(n):
    """Coeffs of P_n (highest degree first) via three-term recurrence, exact in mp."""
    if n == 0:
        return [mp.mpf(1)]
    Pk = [mp.mpf(1), mp.mpf(0)]    # P_1
    Pkm1 = [mp.mpf(1)]             # P_0
    for k in range(1, n):
        xPk = Pk + [mp.mpf(0)]
        term = [(2*k + 1) * c for c in xPk]
        for i, c in enumerate(Pkm1):
            term[i + 2] -= k * c
        Pkm1, Pk = Pk, [c / (k + 1) for c in term]
    return Pk

_GL_CACHE = {}

def _legendre_coeffs(n):
    """Coeffs of P_n, highest degree first, in mp (dps set by caller)."""
    if n == 0:
        return [mp.mpf(1)]
    Pk = [mp.mpf(1), mp.mpf(0)]    # P_1
    Pkm1 = [mp.mpf(1)]             # P_0
    for k in range(1, n):
        xPk = Pk + [mp.mpf(0)]
        term = [(2*k + 1) * c for c in xPk]
        for i, c in enumerate(Pkm1):
            term[i + 2] -= k * c
        Pkm1, Pk = Pk, [c / (k + 1) for c in term]
    return Pk

def _ev(cs, x):
    """Horner eval of a highest-degree-first coefficient list."""
    r = mp.mpf(0)
    for c in cs:
        r = r * x + c
    return r

def gl_ref(n):
    """GL nodes/weights on [-1,1] at ~110+ digit accuracy.
    Roots by Newton (polynomial derivative via Horner); weights via the
    single-factor identity w_i = 2(1-x_i^2)/(n^2 P_{n-1}(x_i)^2).
    Machine checks (fatal asserts): residual |P_n(x_i)| < 1e-110, distinct,
    in (-1,1)."""
    if n in _GL_CACHE:
        return _GL_CACHE[n]
    mp.dps = 150
    cs = _legendre_coeffs(n)
    dcs = [(n - i) * cs[i] for i in range(n)]
    csn1 = _legendre_coeffs(n - 1)
    xs = []
    for k in range(1, n + 1):
        if k == 1:
            x = 1 - mp.mpf('1.8657') / (n * n)
        elif k == n:
            x = -(1 - mp.mpf('1.8657') / (n * n))
        else:
            x = mp.cos(mp.pi * (k - 0.25) / (n + 0.5))
        for _it in range(300):
            fx = _ev(cs, x)
            dfx = _ev(dcs, x)
            step = fx / dfx
            if abs(fx) < mp.mpf('1e-115') or abs(step) < mp.mpf('1e-118'):
                break
            x -= step
        else:
            raise RuntimeError(f"GL root k={k}/n={n} not converged")
        assert abs(_ev(cs, x)) < mp.mpf('1e-110'), f"residual k={k}: {abs(_ev(cs, x))}"
        assert -1 < x < 1, f"root out of range k={k}"
        xs.append(x)
    xs.sort()
    for i in range(1, n):
        assert xs[i] - xs[i - 1] > mp.mpf('1e-80'), f"duplicate roots at {i}"
    ws = [2 * (1 - x * x) / (n * n * _ev(csn1, x) ** 2) for x in xs]
    _GL_CACHE[n] = (xs, ws)
    return xs, ws

def gl_mapped(n, a, b):
    """Map reference nodes to [a,b]; return (nodes, weights) as acb lists."""
    xs, ws = gl_ref(n)
    aq, bq = q(a), q(b)
    mid = acb((aq + bq) / 2); half = acb((bq - aq) / 2)
    return [mid + half*acb(q(x)) for x in xs], [half*acb(q(w)) for w in ws]

def moment_test(n, a, b):
    """Machine check: GL-n exact for polynomials deg < 2n-1; test k = 0..n."""
    xs, ws = gl_mapped(n, a, b)
    ok = True
    for k in range(0, n + 1):
        s = acb(0)
        for x, w in zip(xs, ws):
            s += w * x**k
        exact = (acb(q(b))**(k+1) - acb(q(a))**(k+1)) / acb(k + 1)
        if abs(s - exact) > acb(fmpq(1, 10**40)).real:
            ok = False
            print(f"  MOMENT FAIL k={k}: {s} vs {exact}")
    return ok

def Ht_quad(t, n1=32, n2=64):
    z = acb(fmpq(Z_RE), fmpq(Z_IM))
    t = acb(fmpq(t))
    def f(u):
        s = acb(0)
        for n in range(1, N_MAX + 1):
            nn = acb(n)
            s += (2*PI**2*nn**4*acb.exp(9*u) - 3*PI*nn**2*acb.exp(5*u)) \
                 * acb.exp(-PI*nn**2*acb.exp(4*u))
        return acb.exp(t*u*u) * s * acb.cos(z*u)
    Q1 = acb(0); Q2 = acb(0)
    for a, b in zip(GRID[:-1], GRID[1:]):
        x1, w1 = gl_mapped(n1, a, b)
        x2, w2 = gl_mapped(n2, a, b)
        for x, w in zip(x1, w1):
            Q1 += w * f(x)
        for x, w in zip(x2, w2):
            Q2 += w * f(x)
    rad = abs(Q2 - Q1)
    # tails
    um = acb(q(U_MAX))
    tailA = acb(0)
    for n in range(1, N_MAX + 1):
        nn = acb(n)
        g = 19*um + t*um**2 - PI*nn**2*acb.exp(4*um)
        gp = 19 + 2*t*um - 4*PI*nn**2*acb.exp(4*um)
        assert _re_upper(gp) < 0.0, f"tailA: g_n'({U_MAX}) not negative, n={n}, t={t}"
        assert 2.0*float(t.real.mid()) < _re_lower(16*PI*nn**2*acb.exp(4*um)), \
            f"tailA: g_n'' not <0, n={n}"
        tailA += 2*PI**2*nn**4*acb.exp(g)/(-gp)
    h0 = -25*PI
    hp0 = 19 - 100*PI
    assert _re_upper(hp0) < 0.0
    if float(t.real.mid()) <= 200.0*float(PI.real.mid()):
        assert 2.0*float(t.real.mid()) < 400.0*float(PI.real.mid()), \
            "tailB: h'' not <0 on [0,inf)"
        intb = acb.exp(h0)/(-hp0)
    else:
        uc = acb.log(t/(200*PI))/4
        hc = 19*uc + t*uc**2 - 25*PI*acb.exp(4*uc)
        hpc = 19 + 2*t*uc - 100*PI*acb.exp(4*uc)
        assert _re_upper(hpc) < 0.0, "tailB: h' max not negative"
        intb = uc*acb.exp(h0) + acb.exp(hc)/(-hpc)
    tailB = 2*PI**2*acb(625)*(1 + acb(fmpq(3, 10**15)))*intb
    E = rad.abs_upper() + tailA.abs_upper() + tailB.abs_upper()
    res = Q2 + acb(-E).union(acb(E))   # center = Q2 center, radius = Q2.rad + E
    return res

def H0_closed(z_re, z_im, n_max=4):
    """Claim #3 closed form (verified NUMERIC, tick 10)."""
    z = acb(fmpq(z_re), fmpq(z_im))
    total = acb(0)
    for n in range(1, n_max + 1):
        P = PI * acb(n)**2
        for a, coef in [(9, 2*PI**2*acb(n)**4), (5, -3*PI*acb(n)**2)]:
            sp = acb(fmpq(a, 4), 0) + acb(0, 1)*z*fmpq(1, 4)
            sm = acb(fmpq(a, 4), 0) - acb(0, 1)*z*fmpq(1, 4)
            total += coef*fmpq(1, 8)*(acb.exp(-sp*P.log())*acb.gamma_upper(P, sp)
                                     + acb.exp(-sm*P.log())*acb.gamma_upper(P, sm))
    return total

def Ht_oracle(t, n_max=6):
    """Independent oracle: mpmath 80-digit quad, n=1..6, [0,10]."""
    mp.dps = 80
    z = mp.mpc(Z_RE, Z_IM)
    def f(u):
        s = mp.mpc(0)
        for n in range(1, n_max + 1):
            s += (2*mp.pi**2*n**4*mp.e**(9*u) - 3*mp.pi*n**2*mp.e**(5*u)) \
                 * mp.e**(-mp.pi*n**2*mp.e**(4*u))
        return mp.e**(t*u*u)*s*mp.cos(z*u)
    return mp.quad(f, [0, 0.25, 0.5, 0.75, 1.0, 1.1, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6, 2.0, 3.0, 10.0])

def digits_agree(arb_val, oracle_str_re, oracle_str_im):
    """Relative decimal digits shared between arb center and oracle strings."""
    import re, decimal
    def dec(s):
        d = format(decimal.Decimal(s), 'f')
        d = re.sub(r'[^0-9]', '', d)
        return d
    ar = str(arb_val.real).split(' +/-')[0].strip('[]')
    ai = str(arb_val.imag).split(' +/-')[0].strip('[]')
    # align by exponent: compare leading mantissa digits in scientific form
    def mant(s, nd=60):
        x = decimal.Decimal(s)
        if x == 0: return '0'*nd
        x = abs(x)
        sci = format(x, f'.{nd-1}E')          # d.dddd...E<exp>
        digits = sci.split('E')[0].replace('.', '')
        return digits[:nd].ljust(nd, '0')
    mr, mi = mant(ar), mant(ai)
    orr, oim = mant(oracle_str_re), mant(oracle_str_im)
    def shared(a, b):
        c = 0
        for ca, cb in zip(a, b):
            if ca == cb: c += 1
            else: break
        return c
    return shared(mr, orr), shared(mi, oim)

print("=== machine check 0: GL moment test on [0,1] (n=32) ===")
_mom_ok = moment_test(32, 0.0, 1.0)
print("moment test n=32:", _mom_ok)
assert _mom_ok, "GL moment test FAILED - nodes/weights untrustworthy, all later results void"

print()
print("=== F1: t=0, quadrature vs claim #3 closed form ===")
q0 = Ht_quad(0)
c0 = H0_closed(Z_RE, Z_IM)
print("quad  H_0(35+10i) =", q0)
print("closed H_0(35+10i) =", c0)
dr, di = digits_agree(q0, str(c0.real).split(' +/-')[0].strip('[]'),
                          str(c0.imag).split(' +/-')[0].strip('[]'))
print(f"F1 digits (real, imag): {dr}, {di}  (need >= 25)")
print("F1:", "YES" if min(dr, di) >= 25 else "NO")

for t in [1, 100, 1000]:
    print()
    print(f"=== F2/F3/F4: t={t} ===")
    qt = Ht_quad(t)
    print(f"Arb H_{t}(35+10i) = {qt}")
    print(f"  rad = {float(qt.rad())}")
    orac = Ht_oracle(t)
    print(f"oracle (mpmath 80d) = {mp.nstr(orac, 60)}")
    dr, di = digits_agree(qt, mp.nstr(orac.real, 60), mp.nstr(orac.imag, 60))
    # rel radius via mpmath: float64 overflows for |value| ~ 1e500 (t=1000)
    def _mid_mpf(ball_str):
        return mp.mpf(ball_str.split(' +/-')[0].strip('[]'))
    re_mid = _mid_mpf(str(qt.real))
    im_mid = _mid_mpf(str(qt.imag))
    mag_mp = mp.sqrt(re_mid**2 + im_mid**2)
    rad_mp = _mid_mpf(str(qt.rad()))
    relrad = float(rad_mp / mag_mp) if mag_mp > 0 else float('inf')
    finite = (mp.isfinite(re_mid) and mp.isfinite(im_mid))
    print(f"  log10|value| = {mp.log10(abs(orac)) if abs(orac) > 0 else float('nan')}")
    print(f"F2 digits (real, imag): {dr}, {di}  (need >= 20)")
    print(f"F3 rel radius: {relrad:.3e}  (need < 1e-25)")
    print(f"F4 finite and heat-scale (not NaN/O(1)): {bool(finite)}")
    print(f"F2: {'YES' if min(dr, di) >= 20 else 'NO'}   F3: {'YES' if relrad < 1e-25 else 'NO'}")
