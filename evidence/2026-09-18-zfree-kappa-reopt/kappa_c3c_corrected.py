import mpmath as mp
mp.mp.dps = 50
# ---- w(u) exact (Definition 1) ----
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
# ---- W(s) = Laplace transform of w ----
def W(s):
    return mp.quad(lambda v: mp.e**(-s*v)*w(v), [0, u_max], maxterms=800, limit=400)
# ---- kappa_m: paper + K*x^6, CORRECTED K ----
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
K = mp.mpf('0.0382944246562725')   # corrected (C3a-holding) K
kap_new = list(kap_paper); kap_new[6] = kap_new[6] + K
kap = sum(kap_new)
# ---- Lemma 14 params ----
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def Ffun(z, sigma, eta):
    s = mp.mpf(0)
    for m in range(7):
        s += kap_new[m]*W((z + (2*sigma-1)*m)/eta)
    return s
def Dval(mu, eta):
    sigma = 1 - mu*eta
    L = a1*Ffun(sigma-1+eta, sigma, eta) + a1*Ffun(sigma-eta, sigma, eta) - a0*Ffun(sigma-1, sigma, eta)
    R = C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
    return L - R
print("K (corrected)  =", mp.nstr(K,17))
print("kappa (modified) =", mp.nstr(kap,17))
print("mu0 =", mp.nstr(mu0,10), " eta0 =", eta0)
# ---- fine grid over mu in [mu0,1], eta in (0,eta0] ----
Nmu=Neta=20
minD=mp.mpf('inf'); minpt=None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(1, Neta+1):
        eta = eta0*mp.mpf(j)/Neta
        v = Dval(mu,eta)
        if v < minD: minD=v; minpt=(mp.nstr(mu,8),mp.nstr(eta,10))
print("grid %dx%d min D = %s at (mu,eta)=%s" % (Nmu,Neta,mp.nstr(minD,10),minpt))
# ---- monotonicity in mu: for several eta, is min at mu=mu0? ----
print("--- mu-monotonicity (D at mu0 vs mu=1 for fixed eta) ---")
for j in [1,2,5,10,20,40]:
    eta = eta0*mp.mpf(j)/Neta
    d0 = Dval(mu0,eta); d1 = Dval(mp.mpf(1),eta)
    print("eta=%s  D(mu0)=%s  D(mu=1)=%s  (mu0 smaller? %s)" % (mp.nstr(eta,8),mp.nstr(d0,8),mp.nstr(d1,8),bool(d0<d1)))
# ---- small-eta tail at mu=mu0 ----
print("--- small-eta tail at mu=mu0 ---")
for e in ['1e-3','1e-4','1e-5','1e-6']:
    eta = mp.mpf(e)
    print("eta=%s  D(mu0,eta)=%s" % (e, mp.nstr(Dval(mu0,eta),10)))
