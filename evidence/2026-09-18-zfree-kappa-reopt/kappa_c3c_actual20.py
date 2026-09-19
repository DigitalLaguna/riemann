import mpmath as mp
mp.mp.dps = 40
# ---- w(u) exact (Definition 1), same as kappa_c3c_rigorous.py ----
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
# ---- W(s) = Laplace transform of w = int_0^{u_max} e^{-s v} w(v) dv ----
def W(s):
    return mp.quad(lambda v: mp.e**(-s*v)*w(v), [0, u_max], maxterms=400, limit=200)
# ---- kappa_m: paper + K*x^6 (K = Kmax_c3a) ----
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
Kmax_c3a = mp.mpf('0.03830132421')
kap_new = list(kap_paper); kap_new[6] = kap_new[6] + Kmax_c3a
kap = sum(kap_new)
# ---- Lemma 14 params ----
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def Ffun(z, sigma, eta):
    # F(z) = sum_m kap_m W((z + (2 sigma -1) m)/eta)
    s = mp.mpf(0)
    for m in range(7):
        s += kap_new[m]*W((z + (2*sigma-1)*m)/eta)
    return s
def LHS(sigma, eta):
    return a1*Ffun(sigma-1+eta, sigma, eta) + a1*Ffun(sigma-eta, sigma, eta) - a0*Ffun(sigma-1, sigma, eta)
def rhs14(mu, eta):
    return C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
# ---- grid over (mu, eta) ----
Nmu = Neta = 20
minmargin = mp.mpf('inf'); minpt = None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(1, Neta+1):
        eta = eta0*mp.mpf(j)/Neta
        sigma = 1 - mu*eta
        L = LHS(sigma, eta)
        R = rhs14(mu, eta)
        margin = L - R
        if margin < minmargin:
            minmargin = margin; minpt = (mp.nstr(mu,8), mp.nstr(eta,10), mp.nstr(L,10), mp.nstr(R,10))
print("kappa (modified) =", mp.nstr(kap,15))
print("grid %dx%d over mu in [%.6f,1], eta in (0,%.7f]" % (Nmu,Neta, float(mu0), float(eta0)))
print("min (LHS - [C1+3.909eta+26eta^2-3897eta^3]) =", mp.nstr(minmargin,10))
print("at (mu,eta,LHS,RHS) =", minpt)
print("Lemma14 lower bound holds on grid ? ", bool(minmargin > 0))
