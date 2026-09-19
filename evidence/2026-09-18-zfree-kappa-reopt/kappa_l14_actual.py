import mpmath as mp
mp.mp.dps = 80
# ---- w(u), Definition 1, theta=1.1338 ----
theta = mp.mpf('1.1338')
A  = 1/mp.cos(theta)**2
B  = theta*mp.cos(theta)/mp.sin(theta)
C  = mp.sin(theta)/mp.cos(theta)
D  = 2*theta
E  = mp.sin(2*theta)
F  = mp.sin(theta)
u_max = 2*B
def w(u):
    if u < 0 or u > u_max: return mp.mpf(0)
    inner = (A*(B - u/2)*mp.cos(u*C) + (2*B - u)
             + mp.sin(D - u*C)/E - 2*(1 + mp.sin(theta - u*C)/F))
    return A*inner
w0 = w(0)
assert abs(w0 - mp.mpf('5.672787598')) < mp.mpf('1e-6'), w0
# W(z) = int_0^{u_max} e^{-z u} w(u) du
def W(z):
    return mp.quad(lambda u: mp.e**(-z*u)*w(u), [0, u_max], maxdiv=60, limit=300)
# ---- constants ----
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
K = mp.mpf('0.03830132421')
kap_mod = kap_paper[:]; kap_mod[6] = kap_mod[6] + K
M = 6
def C1(x): return mp.mpf('0.87637') + mp.mpf('0.12002')*x + mp.mpf('0.01017')*x**2 - mp.mpf('0.00073')*x**3
def LHS(kap, mu, eta):
    sigma = 1 - mu*eta
    tot = mp.mpf(0)
    for m in range(M+1):
        d = (2*sigma - 1)*m
        z1 = (sigma - 1 + eta + d)/eta   # a1 F(sigma-1+eta)
        z2 = (sigma - eta + d)/eta       # a1 F(sigma-eta)
        z3 = (sigma - 1 + d)/eta         # -a0 F(sigma-1)
        tot += kap[m]*(a1*W(z1) + a1*W(z2) - a0*W(z3))
    return tot
def RHS(mu, eta):
    return C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
# ---- scan ----
Nmu = Neta = 200
minD = mp.mpf('inf'); minpt = None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(1, Neta+1):
        eta = eta0*mp.mpf(j)/Neta
        Dv = LHS(kap_mod, mu, eta) - RHS(mu, eta)
        if Dv < minD: minD = Dv; minpt = (mp.nstr(mu,8), mp.nstr(eta,12))
# also paper kappa for sanity
minDp = mp.mpf('inf'); minptp = None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(1, Neta+1):
        eta = eta0*mp.mpf(j)/Neta
        Dv = LHS(kap_paper, mu, eta) - RHS(mu, eta)
        if Dv < minDp: minDp = Dv; minptp = (mp.nstr(mu,8), mp.nstr(eta,12))
print("mu0 =", mp.nstr(mu0,10), " eta0 =", mp.nstr(eta0,10))
print("MODIFIED: min (LHS - RHS) =", mp.nstr(minD,12), "at (mu,eta)=", minpt)
print("PAPER:    min (LHS - RHS) =", mp.nstr(minDp,12), "at (mu,eta)=", minptp)
print("MODIFIED LHS>=RHS everywhere on grid ?", bool(minD >= 0))
