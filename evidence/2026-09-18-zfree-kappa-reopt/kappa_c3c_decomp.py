import mpmath as mp
mp.mp.dps = 50
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
def W(s):
    return mp.quad(lambda v: mp.e**(-s*v)*w(v), [0, u_max], maxterms=800, limit=400)
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
K = mp.mpf('0.0382944246562725')
kap_new = list(kap_paper); kap_new[6] = kap_new[6] + K
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def Ffun(kap, z, sigma, eta):
    s = mp.mpf(0)
    for m in range(7):
        s += kap[m]*W((z + (2*sigma-1)*m)/eta)
    return s
def Dval(kap, mu, eta):
    sigma = 1 - mu*eta
    L = a1*Ffun(kap, sigma-1+eta, sigma, eta) + a1*Ffun(kap, sigma-eta, sigma, eta) - a0*Ffun(kap, sigma-1, sigma, eta)
    R = C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
    return L - R
def bracket6(mu, eta):
    sigma = 1 - mu*eta
    x1 = (sigma-1+eta + (2*sigma-1)*6)/eta
    x2 = (sigma-eta     + (2*sigma-1)*6)/eta
    x3 = (sigma-1       + (2*sigma-1)*6)/eta
    return a1*W(x1) + a1*W(x2) - a0*W(x3)
print("=== DECOMPOSITION CHECK: D_mod == D_paper + K*B6 ? ===")
maxerr = mp.mpf(0)
for (mu,eta) in [(mu0,eta0),(mu0,eta0/2),(mp.mpf(1),eta0),(mp.mpf(1),eta0/4),(0.95,0.003),(mu0,0.001)]:
    dm = Dval(kap_new, mu, eta); dp = Dval(kap_paper, mu, eta); b6 = bracket6(mu, eta)
    err = abs(dm - (dp + K*b6))
    maxerr = max(maxerr, err)
    print("mu=%s eta=%s  D_mod=%s  D_paper+K*B6=%s  err=%s" % (mp.nstr(mu,6),mp.nstr(eta,9),mp.nstr(dm,8),mp.nstr(dp+K*b6,8),mp.nstr(err,3)))
print("MAX DECOMP ERR =", mp.nstr(maxerr,3))
print()
print("=== B6 landscape (fine grid) ===")
Nmu=Neta=40
minB6=mp.mpf('inf'); minpt=None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(1,Neta+1):
        eta = eta0*mp.mpf(j)/Neta
        b = bracket6(mu,eta)
        if b < minB6: minB6=b; minpt=(mp.nstr(mu,7),mp.nstr(eta,9))
print("grid %dx%d min B6 = %s at (mu,eta)=%s" % (Nmu,Neta,mp.nstr(minB6,10),minpt))
print()
print("=== D_mod landscape (fine grid) ===")
minD=mp.mpf('inf'); minDpt=None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(1,Neta+1):
        eta = eta0*mp.mpf(j)/Neta
        d = Dval(kap_new, mu, eta)
        if d < minD: minD=d; minDpt=(mp.nstr(mu,7),mp.nstr(eta,9))
print("grid %dx%d min D_mod = %s at (mu,eta)=%s" % (Nmu,Neta,mp.nstr(minD,10),minDpt))
