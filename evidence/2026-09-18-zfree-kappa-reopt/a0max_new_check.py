# Check: does A0_max survive the kappa_m modification (paper + K*x^6, K=0.0383)?
# A0_max (claim #54) is pinned at (th=hi, A0=A0_g(hi)) for the PAPER's kap.
# The only kappa_m-dependent constraint is the Lemma-14 LHS (via F -> kap).
# If the LHS (fulltotal) is still >= 0 at (hi, A0_g(hi)) with the MODIFIED kap,
# then A0_max_new >= A0_g(hi) = 0.3921 > A_final(kappa_max) = 0.3603,
# so the re-optimization improvement is VALID.
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
# PAPER kap vs MODIFIED kap (kappa_6 += K)
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
def LHS(mu, eta, th, A0, kap):
    sigma = 1 - mu*eta
    return a1*F(sigma-1+eta, sigma, eta, th, kap) + a1*F(sigma-eta, sigma, eta, th, kap) - a0*F(sigma-1, sigma, eta, th, kap)
def fulltotal(th, A0, kap, nmu=7, neta=9):
    sigma0 = 1 - A0/xKT; e0 = A0/xH; mu0 = (1-sigma0)/e0
    best = None; bestpt = None
    for i in range(nmu):
        mu = mu0 + (1-mu0)*mp.mpf(i)/mp.mpf(nmu-1)
        for j in range(neta):
            v = LHS(mu, e0*mp.mpf(j+1)/mp.mpf(neta), th, A0, kap)
            if best is None or v < best: best, bestpt = v, (mu, e0*mp.mpf(j+1)/mp.mpf(neta))
    return best, bestpt
# Pinned point (claim #54)
hi = mp.mpf('0.376216048449719989')
A0_hi = A0_g(hi)
print("pinned: hi =", mp.nstr(hi,18), " A0_g(hi) =", mp.nstr(A0_hi,18))
vf_p, pt_p = fulltotal(hi, A0_hi, kap_paper)
vf_m, pt_m = fulltotal(hi, A0_hi, kap_mod)
print("fulltotal min (PAPER kap)  =", mp.nstr(vf_p,12), "at mu=",mp.nstr(pt_p[0],6)," eta=",mp.nstr(pt_p[1],6))
print("fulltotal min (MODIFIED kap) =", mp.nstr(vf_m,12), "at mu=",mp.nstr(pt_m[0],6)," eta=",mp.nstr(pt_m[1],6))
A_final_max = mp.mpf('0.360276469795491')
print("A0_g(hi) > A_final(kappa_max)?", bool(A0_hi > A_final_max), " (A0_g(hi)=",mp.nstr(A0_hi,12),")")
print("MODIFIED feasible at pinned point (fulltotal>=0)?", bool(vf_m >= 0))
print("=> if feasible: A0_max_new >= A0_g(hi) =", mp.nstr(A0_hi,12), "> A_final_max =", mp.nstr(A_final_max,12), " => improvement VALID")
