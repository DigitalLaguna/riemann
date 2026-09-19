import mpmath as mp, time
t0=time.time()
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
    return mp.quad(lambda v: mp.e**(-s*v)*w(v), [0, u_max], maxterms=120, limit=200)
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
K = mp.mpf('0.0382944246562725')
kap = list(kap_paper); kap[6] = kap[6] + K
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def Ffun(z, sigma, eta):
    s = mp.mpf(0)
    for m in range(7):
        s += kap[m]*W((z + (2*sigma-1)*m)/eta)
    return s
def Dval(mu, eta):
    sigma = 1 - mu*eta
    L = a1*Ffun(sigma-1+eta, sigma, eta) + a1*Ffun(sigma-eta, sigma, eta) - a0*Ffun(sigma-1, sigma, eta)
    R = C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
    return L - R
def inner_pp(u):
    return A*C*mp.sin(u*C) - A*C**2*(B - u/2)*mp.cos(u*C) \
           - C**2*mp.sin(D - u*C)/E + 2*C**2*mp.sin(theta - u*C)/F
W2 = u_max * A * (A*C + A*C**2*B + C**2/E + 2*C**2/F)
def LB(mu, eta):
    x3 = mp.mpf(6)/eta - mp.mpf(13)*mu
    x1 = x3 + 1; x2 = x3 + 1/eta - 1
    t1 = a1/x1 + a1/x2 - a0/x3
    t3 = a1/x1**2 + a1/x2**2 + a0/x3**2
    return w0*t1 - W2*t3 - mp.mpf('1e-370')
def bracket6(mu, eta):
    sigma = 1 - mu*eta
    x1 = (sigma-1+eta + (2*sigma-1)*6)/eta
    x2 = (sigma-eta     + (2*sigma-1)*6)/eta
    x3 = (sigma-1       + (2*sigma-1)*6)/eta
    return a1*W(x1) + a1*W(x2) - a0*W(x3)
Nmu=Neta=20
minD=mp.mpf('inf'); maxLBminusD=mp.mpf('-inf'); maxLBminusB=mp.mpf('-inf')
minDpt=None; worstpt=None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(1, Neta+1):
        eta = eta0*mp.mpf(j)/Neta
        d = Dval(mu,eta); lb = LB(mu,eta); b = bracket6(mu,eta)
        if d < minD: minD=d; minDpt=(mp.nstr(mu,7),mp.nstr(eta,9))
        if lb - d > maxLBminusD: maxLBminusD=lb-d; worstpt=(mp.nstr(mu,7),mp.nstr(eta,9))
        if lb - b > maxLBminusB: maxLBminusB=lb-b
    if i % 5 == 0: print("row %d/%d  elapsed %.1fs" % (i,Nmu,time.time()-t0), flush=True)
print("min true D          =", mp.nstr(minD,10), "at", minDpt)
print("max (LB - D)        =", mp.nstr(maxLBminusD,10), "at", worstpt, "  (<=0 => LB valid lower bound on D)")
print("max (LB - bracket6) =", mp.nstr(maxLBminusB,10), "  (<=0 => LB valid lower bound on m=6 bracket)")
print("kappa_6 (modified)  =", mp.nstr(kap[6],10))
print("total elapsed %.1fs" % (time.time()-t0))
