import mpmath as mp
mp.mp.dps = 50
theta = mp.mpf('1.1338')
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
H  = mp.mpf(3)*mp.mpf(10)**12; K = mp.mpf(16); T0 = mp.mpf(10)**10
A0 = mp.mpf(1)/mp.mpf('4.896')
eta0 = A0/mp.log(H); sigma0 = 1 - A0/mp.log(K*H + T0)
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
s2 = 1/mp.cos(theta)**2; ct = mp.cot(theta); tt = mp.tan(theta); L = 2*theta*ct
def w(u):
    if u < 0 or u > L: return mp.mpf(0)
    return s2*( s2*(theta*ct - u/2)*mp.cos(u*tt) + 2*theta*ct - u
                + mp.sin(2*theta - u*tt)/mp.sin(2*theta)
                - 2*(1 + mp.sin(theta - u*tt)/mp.sin(theta)) )
def W(z):
    return mp.quad(lambda u: mp.e**(-z*u)*w(u), [0, L])
kap0 = [mp.mpf(1),mp.mpf(-851)/859,mp.mpf(780)/859,mp.mpf(-525)/859,
        mp.mpf(171)/859,mp.mpf(28)/859,mp.mpf(-29)/859]
M = 6
def F(z, sigma, eta, kap):
    s = mp.mpf(0)
    for m in range(M+1):
        s += kap[m]*W((z+(2*sigma-1)*m)/eta)
    return s
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def margin(sigma, eta, kap):
    mu = (1-sigma)/eta
    lhs = a1*F(sigma-1+eta,sigma,eta,kap) + a1*F(sigma-eta,sigma,eta,kap) - a0*F(sigma-1,sigma,eta,kap)
    rhs = C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
    return lhs-rhs, mu

best = mp.mpf('inf'); bestpt=None
for eta_frac in [0.05, 0.02, 0.01, 0.005, 0.001]:
    eta = eta_frac*eta0
    lo = max(sigma0, 1-eta); hi = 1-mu0*eta
    for sf in [0.0, 0.25, 0.5, 0.75, 1.0]:
        sigma = lo + sf*(hi-lo)
        mg, mu = margin(sigma, eta, kap0)
        if mg < best: best=mg; bestpt=(eta,sigma,mu)
        print("  eta=%.6f sigma=%.8f mu=%.5f  margin=%.6e"%(eta, sigma, mu, mg))
print("\nMIN so far: margin=%.6e at eta=%.6f sigma=%.8f mu=%.5f"%(best, bestpt[0], bestpt[1], bestpt[2]))
