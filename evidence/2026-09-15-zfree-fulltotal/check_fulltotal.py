# Re-verify the full-total claim: the exact Lemma-14 total LHS is NEGATIVE at
# theta*=0.057151961, A0=0.396708119308 (min over the 7x9 grid of mu in [mu0,1],
# eta in (0,eta0] < 0). Re-runs the same 50-dps grid as the main run.
import mpmath as mp, sys
mp.mp.dps = 50
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
        return mp.mpf(1)/s*mp.quad(lambda t: mp.e**(-t)*w(t/s, th), [0, min(b*s, mp.mpf(60))])
    return mp.quad(lambda v: mp.e**(-s*v)*w(v, th), [0, b])
def F(z, sigma, eta, th):
    return sum(kap[m]*W((z+(2*sigma-1)*m)/eta, th) for m in range(7))
def LHS(mu, eta, th, A0):
    sigma = 1 - mu*eta
    return a1*F(sigma-1+eta, sigma, eta, th) + a1*F(sigma-eta, sigma, eta, th) - a0*F(sigma-1, sigma, eta, th)
def scan(th, A0, nmu=7, neta=9):
    sigma0 = 1 - A0/mp.log(K*H+T0); eta0 = A0/mp.log(H); mu0 = (1-sigma0)/eta0
    best = None
    for i in range(nmu):
        mu = mu0 + (1-mu0)*i/(nmu-1)
        for j in range(neta):
            v = LHS(mu, eta0*(j+1)/neta, th, A0)
            if best is None or v < best: best = v
    return best
ths = mp.mpf('0.057151961'); A0s = mp.mpf('0.396708119308')
mins = scan(ths, A0s)
print(f"min LHS (theta*=0.057151961, A0=0.396708119308) = {mp.nstr(mins,12)}")
ok = mins < 0
print(f"CHECK theta*<0 = {ok} -> {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
