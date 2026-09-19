# GAP check for claim #58 (kappa_m re-opt): verify the Lemma-14 C1+C2 lower bound
#   actual LHS >= C1(mu) + 3.909*eta + 26*eta^2 - 3897*eta^3
# holds on the domain (mu in [mu0,1], eta in (0,eta0]) for the MODIFIED kappa_m
# (paper + K*x^6, K=0.03830132421). This is the bound the A_final formula uses.
# If min(LHS - bound) < 0 anywhere -> the Lemma-14 bound is violated for the
# modified kappa -> the re-optimization is INVALID (idea DEAD).
import mpmath as mp
mp.mp.dps = 50
T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12; K = mp.mpf(16)
xKT = mp.log(K*H + T0); xH = mp.log(H)
def eta0(A0): return A0/xH
def sig0(A0): return 1 - A0/xKT
def w0(th): return mp.sec(th)**2*(th*mp.tan(th) + 3*th/mp.tan(th) - 3)
def g(A0, th):
    L = (2*sig0(A0)-1)/eta0(A0)
    c0 = 1/mp.sin(th)*mp.sec(th)**2
    c1 = (th - mp.sin(th)*mp.cos(th))*mp.tan(th)**4
    c2 = mp.tan(th)**3*mp.sin(th)**2
    c3 = (th - mp.sin(th)*mp.cos(th))*mp.tan(th)**2
    C = c0*L*(c2*(L+1)**2*(mp.e**(-2*L*th)/mp.tan(th) + 1) + c1*L + c3*L**3)/(L**2 - mp.tan(th)**2)**2
    return eta0(A0)**2*C/(mp.mpf('0.0005')*(2*sig0(A0)-1)*w0(th))
def A0_g(th):
    lo, hi = mp.mpf('0.001'), mp.mpf(10)
    for _ in range(170):
        mid = (lo+hi)/2
        if g(mid, th) < 1: lo = mid
        else: hi = mid
    return lo
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
Kmod = mp.mpf('0.03830132421')
kap_mod = list(kap_paper); kap_mod[6] = kap_mod[6] + Kmod
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
def w(u, th):
    b = 2*th/mp.tan(th)
    if u < 0 or u > b: return mp.mpf(0)
    s2 = mp.sec(th)**2
    return s2*(s2*(th/mp.tan(th)-u/2)*mp.cos(u*mp.tan(th)) + 2*th/mp.tan(th)-u
               + mp.sin(2*th-u*mp.tan(th))/mp.sin(2*th)
               - 2*(1+mp.sin(th-u*mp.tan(th))/mp.sin(th)))
def W(s, th):
    b = 2*th/mp.tan(th)
    if s > 40:
        return mp.mpf(1)/s*mp.quad(lambda t: mp.e**(-t)*w(t/s, th), [0, min(b*s, mp.mpf(60))])
    return mp.quad(lambda v: mp.e**(-s*v)*w(v, th), [0, b])
def F(z, sigma, eta, th, kap):
    return sum(kap[m]*W((z+(2*sigma-1)*m)/eta, th) for m in range(7))
def LHS(mu, eta, th, kap):
    sigma = 1 - mu*eta
    return a1*F(sigma-1+eta, sigma, eta, th, kap) + a1*F(sigma-eta, sigma, eta, th, kap) - a0*F(sigma-1, sigma, eta, th, kap)
def C1(x): return mp.mpf('0.87637') + mp.mpf('0.12002')*x + mp.mpf('0.01017')*x**2 - mp.mpf('0.00073')*x**3
def bound(mu, eta):
    return C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
# Pinned point (claim #54)
hi = mp.mpf('0.376216048449719989')
A0_hi = A0_g(hi)
sigma0 = 1 - A0_hi/xKT; e0 = A0_hi/xH; mu0 = (1-sigma0)/e0
print("pinned: A0 =", mp.nstr(A0_hi,15), " sigma0 =", mp.nstr(sigma0,12),
      " eta0 =", mp.nstr(e0,12), " mu0 =", mp.nstr(mu0,12))
print("bound at (mu0,eta0) =", mp.nstr(bound(mu0,e0),12),
      "  bound at (1,eta0) =", mp.nstr(bound(1,e0),12))
# Fine grid: min of (LHS - bound) for MODIFIED kappa
nmu, neta = 60, 60
best = None; bestpt = None
for i in range(nmu):
    mu = mu0 + (1-mu0)*mp.mpf(i)/mp.mpf(nmu-1)
    for j in range(neta):
        eta = e0*mp.mpf(j+1)/mp.mpf(neta)
        v = LHS(mu, eta, hi, kap_mod) - bound(mu, eta)
        if best is None or v < best: best, bestpt = v, (mu, eta)
print("MODIFIED: min(LHS - bound) =", mp.nstr(best,12),
      " at mu =", mp.nstr(bestpt[0],8), " eta =", mp.nstr(bestpt[1],8))
# Same for PAPER kappa (sanity: should be >= 0, Lemma 14 is a theorem)
bestp = None; bestptp = None
for i in range(nmu):
    mu = mu0 + (1-mu0)*mp.mpf(i)/mp.mpf(nmu-1)
    for j in range(neta):
        eta = e0*mp.mpf(j+1)/mp.mpf(neta)
        v = LHS(mu, eta, hi, kap_paper) - bound(mu, eta)
        if bestp is None or v < bestp: bestp, bestptp = v, (mu, eta)
print("PAPER:    min(LHS - bound) =", mp.nstr(bestp,12),
      " at mu =", mp.nstr(bestptp[0],8), " eta =", mp.nstr(bestptp[1],8))
print("VERDICT: modified Lemma-14 C1+C2 bound holds everywhere?", bool(best >= 0))
