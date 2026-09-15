# Robustness check: re-evaluate the exact Lemma-14 total at theta* at 100 dps
# on a finer grid near the 50-dps grid minimum (mu=1, eta=eta0/9) to confirm
# the negative is not a quadrature/grid artifact.
import mpmath as mp
mp.mp.dps = 100
kap = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
       mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
K = mp.mpf(16); T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12
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
        return mp.mpf(1)/s*mp.quad(lambda t: mp.e**(-t)*w(t/s, th), [0, min(b*s, mp.mpf(80))])
    return mp.quad(lambda v: mp.e**(-s*v)*w(v, th), [0, b])
def F(z, sigma, eta, th):
    return sum(kap[m]*W((z+(2*sigma-1)*m)/eta, th) for m in range(7))
def LHS(mu, eta, th, A0):
    sigma = 1 - mu*eta
    return a1*F(sigma-1+eta, sigma, eta, th) + a1*F(sigma-eta, sigma, eta, th) - a0*F(sigma-1, sigma, eta, th)
ths = mp.mpf('0.057151961'); A0s = mp.mpf('0.396708119308')
sigma0 = 1 - A0s/mp.log(K*H+T0); eta0 = A0s/mp.log(H); mu0 = (1-sigma0)/eta0
print(f"theta*={mp.nstr(ths,10)} A0={mp.nstr(A0s,12)} mu0={mp.nstr(mu0,8)} eta0={mp.nstr(eta0,8)}")
print("=== finer eta grid at mu=1 (100 dps) ===")
for j in [9, 18, 36, 72]:
    eta = eta0/mp.mpf(j)
    v = LHS(mp.mpf(1), eta, ths, A0s)
    print(f"mu=1 eta=eta0/{j}={mp.nstr(eta,6)}: LHS={mp.nstr(v,10)}")
print("=== mu grid at eta=eta0/9 (100 dps) ===")
eta = eta0/9
for mu in ['0.91198149','0.95','1.0']:
    v = LHS(mp.mpf(mu), eta, ths, A0s)
    print(f"mu={mu} eta=eta0/9: LHS={mp.nstr(v,10)}")
