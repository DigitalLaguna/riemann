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
GL nodes/weights: mpmath 120-digit polyroots of Legendre P_n, weights via
  w_i = 2/((1-x_i^2)*n^2*P_{n-1}(x_i)^2)  (exact identity, P_n(x_i)=0),
verified in Arb by the moment test sum w_i x_i^k == (b^{k+1}-a^{k+1})/(k+1), k=0..n.
Pre-registered checks (logs/2026-08-20.tick.log, tick 11):
  F1: t=0 quadrature vs claim #3 closed form, >= 25 digits
  F2: t in {1,100,1000} vs independent mpmath 80-digit quad, >= 20 digits
  F3: Arb radius < 1e-25 RELATIVE (pre-reg said absolute; t=1000 value is O(e^1143),
      relative is the only reading consistent with F2)
  F4: t=1000 value finite, O(e^O(1000)) heat peak, not NaN/O(1)
"""
import flint, mpmath as mp
flint.ctx.prec = 160
acb = flint.acb
fmpq = flint.fmpq
PI = acb('3.141592653589793238462643383279502884197169399375105820974944592307816406286')

Z_RE, Z_IM = 35, 10
N_MAX = 4
U_MAX = 2.0
GRID = [0.0, 0.25, 0.5, 0.75, 1.0, 1.1, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6, 2.0]

def gl_ref(n):
    """GL nodes/weights on [-1,1], 120 digits."""
    mp.dps = 120
    roots = sorted(mp.polyroots(mp.legendre(n)))
    xs, ws = [], []
    for x in roots:
        Pnm1 = mp.legendre(n - 1, x)
        w = 2.0 / ((1 - x*x) * n * n * Pnm1 * Pnm1)
        xs.append(x); ws.append(w)
    return xs, ws

def gl_mapped(n, a, b):
    """Map reference nodes to [a,b]; return (nodes, weights) as acb lists."""
    xs, ws = gl_ref(n)
    mid = acb(fmpq(a + b, 2)); half = acb(fmpq(b - a, 2))
    return [mid + half*acb(fmpq(str(x))) for x in xs], [half*acb(fmpq(str(w))) for w in ws]

def moment_test(n, a, b):
    """Machine check: GL-n exact for polynomials deg < 2n-1; test k = 0..n."""
    xs, ws = gl_mapped(n, a, b)
    ok = True
    for k in range(0, n + 1):
        s = acb(0)
        for x, w in zip(xs, ws):
            s += w * x**k
        exact = (acb(fmpq(b))**(k+1) - acb(fmpq(a))**(k+1)) / acb(k + 1)
        if abs(s - exact) > acb(fmpq(1, 10**40)):
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
    um = acb(fmpq(U_MAX))
    tailA = acb(0)
    for n in range(1, N_MAX + 1):
        nn = acb(n)
        g = 19*um + t*um**2 - PI*nn**2*acb.exp(4*um)
        gp = 19 + 2*t*um - 4*PI*nn**2*acb.exp(4*um)
        assert gp.real < 0, f"tailA: g_n'({U_MAX}) not negative, n={n}, t={t}"
        assert 2*t.real < 16*PI*nn**2*acb.exp(4*um).real, f"tailA: g_n'' not <0, n={n}"
        tailA += 2*PI**2*nn**4*acb.exp(g)/(-gp)
    h0 = -25*PI
    hp0 = 19 - 100*PI
    assert hp0.real < 0
    if t.real <= 200*PI.real:
        assert 2*t.real < 400*PI.real, "tailB: h'' not <0 on [0,inf)"
        intb = acb.exp(h0)/(-hp0)
    else:
        uc = acb.log(t/(200*PI))/4
        hc = 19*uc + t*uc**2 - 25*PI*acb.exp(4*uc)
        hpc = 19 + 2*t*uc - 100*PI*acb.exp(4*uc)
        assert hpc.real < 0, "tailB: h' max not negative"
        intb = uc*acb.exp(h0) + acb.exp(hc)/(-hpc)
    tailB = 2*PI**2*acb(625)*(1 + acb(fmpq(3, 10**15)))*intb
    res = Q2
    res.rad += rad + tailA + tailB
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
    # align by exponent: use scientific mantissa comparison
    def mant(s, nd=60):
        x = decimal.Decimal(s)
        if x == 0: return '0'*nd
        sign = '-' if x < 0 else ''
        x = abs(x)
        exp = x.adjusted()
        m = format(x * 10**(-exp), '.60f')[2:]
        return m
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
print("moment test n=32:", moment_test(32, 0.0, 1.0))

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
    mag = float(abs(qt))
    relrad = float(qt.rad()) / max(mag, 1e-300)
    print(f"  log10|value| = {mp.log10(abs(orac)) if abs(orac) > 0 else float('nan')}")
    print(f"F2 digits (real, imag): {dr}, {di}  (need >= 20)")
    print(f"F3 rel radius: {relrad:.3e}  (need < 1e-25)")
    print(f"F2: {'YES' if min(dr, di) >= 20 else 'NO'}   F3: {'YES' if relrad < 1e-25 else 'NO'}")
