"""
Track B step 3 (t_0 question): can our verified GL quadrature (claim #4) reach the
Polymath15 barrier region? Paper's X_0 := 6e10 + 83952 (Sec 8.1, p. 37); barrier
location X = X_0 - 0.5 = 6e10 + 83951.5 (Fig 11 caption, p. 39); region
X_0-0.5 <= x <= X_0+0.5, y in [0.2,1], t in [0,0.2] (Sec 8.2, regions (a)/(iii)).
Verified against fetched paper tick 44:
evidence/2026-08-21-ht-barrier/x0-verification.txt. Integrand cos(z u) with z_re ~ 6e10 oscillates
with period 2*pi/z_re ~ 1e-10 in u; GL n=32/64 on [0,2] cannot resolve it.
Machine test: degree-difference radius (n=32 vs n=64) at the barrier point vs at the
verified z=35+10i. Falsification (pre-registered): if the barrier radius is SMALL
(comparable to the z=35+10i radius ~1e-29 rel), the quadrature DOES reach the barrier
and no AFE is needed.
Self-contained: copies GL machinery from ht_quadrature.py (claim #4 source) to avoid
running its unguarded main block.
"""
import flint
from fractions import Fraction
from mpmath import mp
flint.ctx.prec = 160
acb = flint.acb
fmpq = flint.fmpq
PI = acb('3.141592653589793238462643383279502884197169399375105820974944592307816406286')
GRID = [0.0, 0.25, 0.5, 0.75, 1.0, 1.1, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, 1.6, 2.0]
N_MAX = 4

def q(x):
    f = Fraction(str(x)); return fmpq(f.numerator, f.denominator)

def _legendre_coeffs(n):
    if n == 0: return [mp.mpf(1)]
    Pk = [mp.mpf(1), mp.mpf(0)]; Pkm1 = [mp.mpf(1)]
    for k in range(1, n):
        xPk = Pk + [mp.mpf(0)]
        term = [(2*k + 1) * c for c in xPk]
        for i, c in enumerate(Pkm1): term[i + 2] -= k * c
        Pkm1, Pk = Pk, [c / (k + 1) for c in term]
    return Pk

def _ev(cs, x):
    r = mp.mpf(0)
    for c in cs: r = r * x + c
    return r

def gl_ref(n):
    mp.dps = 150
    cs = _legendre_coeffs(n)
    dcs = [(n - i) * cs[i] for i in range(n)]
    csn1 = _legendre_coeffs(n - 1)
    xs = []
    for k in range(1, n + 1):
        if k == 1: x = 1 - mp.mpf('1.8657') / (n * n)
        elif k == n: x = -(1 - mp.mpf('1.8657') / (n * n))
        else: x = mp.cos(mp.pi * (k - 0.25) / (n + 0.5))
        for _it in range(300):
            fx = _ev(cs, x); dfx = _ev(dcs, x); step = fx / dfx
            if abs(fx) < mp.mpf('1e-115') or abs(step) < mp.mpf('1e-118'): break
            x -= step
        else: raise RuntimeError(f"GL root k={k}/n={n} not converged")
        xs.append(x)
    xs.sort()
    ws = [2 * (1 - x * x) / (n * n * _ev(csn1, x) ** 2) for x in xs]
    return xs, ws

def gl_mapped(n, a, b):
    xs, ws = gl_ref(n)
    aq, bq = q(a), q(b)
    mid = acb((aq + bq) / 2); half = acb((bq - aq) / 2)
    return [mid + half*acb(q(x)) for x in xs], [half*acb(q(w)) for w in ws]

def Ht_quad_z(t, z_re, z_im, n1, n2, nmax=4):
    z = acb(q(z_re), q(z_im))
    t = acb(q(t))
    def f(u):
        s = acb(0)
        for n in range(1, nmax + 1):
            nn = acb(n)
            s += (2*PI**2*nn**4*acb.exp(9*u) - 3*PI*nn**2*acb.exp(5*u)) \
                 * acb.exp(-PI*nn**2*acb.exp(4*u))
        return acb.exp(t*u*u) * s * acb.cos(z*u)
    Q1 = acb(0); Q2 = acb(0)
    for a, b in zip(GRID[:-1], GRID[1:]):
        x1, w1 = gl_mapped(n1, a, b)
        x2, w2 = gl_mapped(n2, a, b)
        for x, w in zip(x1, w1): Q1 += w * f(x)
        for x, w in zip(x2, w2): Q2 += w * f(x)
    return Q2, abs(Q2 - Q1)

def relrad(val, rad):
    m = float(abs(val).abs_upper())
    return float(rad.abs_upper()) / m if m > 0 else float('inf')

print("=== reference: z=35+10i, t=0.2 (verified region) ===")
v, r = Ht_quad_z(0.2, 35, 10, 32, 64)
print(f"  H_0.2(35+10i) = {v}")
print(f"  degree-diff radius = {r.abs_upper()}  rel = {relrad(v, r):.3e}")

print("=== barrier-like: z=1000+0.2i, t=0.2 (moderate oscillation) ===")
v, r = Ht_quad_z(0.2, 1000, 0.2, 32, 64)
print(f"  H_0.2(1000+0.2i) = {v}")
print(f"  degree-diff radius = {r.abs_upper()}  rel = {relrad(v, r):.3e}")

print("=== BARRIER: z=6e10+83951.5+0.2i, t=0.2 (X = X_0-0.5, y=0.2) ===")
X0 = 60000000000 + 83951.5
v, r = Ht_quad_z(0.2, X0, 0.2, 32, 64)
print(f"  H_0.2(X0+0.2i) = {v}")
print(f"  degree-diff radius = {r.abs_upper()}  rel = {relrad(v, r):.3e}")
print(f"  VERDICT: barrier rel radius {'SMALL (quadrature reaches barrier)' if relrad(v,r) < 1e-6 else 'LARGE (quadrature does NOT converge; AFE needed)'}")
