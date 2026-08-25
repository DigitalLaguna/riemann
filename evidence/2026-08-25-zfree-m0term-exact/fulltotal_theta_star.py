# Full Lemma-14 total at theta*: LHS = a1F(s-1+eta)+a1F(s-eta)-a0F(s-1), exact W.
# Question (pre-registered tick 220): is LHS > 0 for all mu in [mu0,1], eta in (0,eta0]
#  at theta* = 0.057151961, A0 = 0.396708119308? If yes, m=0 constraint vacuous,
#  A0_max = 0.3967 (const 2.5207) survives. Validate pipeline at paper theta=1.1338.
import mpmath as mp
mp.mp.dps = 50

# fixed kappa (eq 18), M=6
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
    # exact Laplace transform; stable substitution for large s
    b = 2*th/mp.tan(th)
    if s > 40:
        # W(s) = (1/s) int_0^{b s} e^{-t} w(t/s) dt ; e^{-t} kills t>~40
        return mp.mpf(1)/s*mp.quad(lambda t: mp.e**(-t)*w(t/s, th), [0, min(b*s, mp.mpf(60))])
    return mp.quad(lambda v: mp.e**(-s*v)*w(v, th), [0, b])

def F(z, sigma, eta, th):
    return sum(kap[m]*W((z+(2*sigma-1)*m)/eta, th) for m in range(7))

def LHS(mu, eta, th, A0):
    sigma0 = 1 - A0/mp.log(K*H+T0)
    sigma = 1 - mu*eta
    return a1*F(sigma-1+eta, sigma, eta, th) + a1*F(sigma-eta, sigma, eta, th) - a0*F(sigma-1, sigma, eta, th)

def params(A0):
    sigma0 = 1 - A0/mp.log(K*H+T0)
    eta0 = A0/mp.log(H)
    mu0 = (1-sigma0)/eta0
    return sigma0, eta0, mu0

def scan(th, A0, nmu=7, neta=9):
    sigma0, eta0, mu0 = params(A0)
    best = None; bestpt = None
    for i in range(nmu):
        mu = mu0 + (1-mu0)*i/(nmu-1)
        for j in range(neta):
            eta = eta0*(j+1)/neta
            v = LHS(mu, eta, th, A0)
            if best is None or v < best:
                best = v; bestpt = (mu, eta)
    return best, bestpt, mu0, eta0

print("=== VALIDATION at paper theta=1.1338, A0=(4.8596)^-1 ===")
thp = mp.mpf('1.1338'); A0p = 1/mp.mpf('4.8596')
best, pt, mu0, eta0 = scan(thp, A0p)
print(f"paper: mu0={mp.nstr(mu0,8)} eta0={mp.nstr(eta0,8)}")
print(f"min LHS (paper) = {mp.nstr(best,10)} at mu={mp.nstr(pt[0],6)} eta={mp.nstr(pt[1],6)} -> {'POSITIVE' if best>0 else 'NEGATIVE'}")
# paper lower bound at that point for comparison
mu, eta = pt
C1 = mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
lb = C1 + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3
print(f"paper LB C1(mu)+3.909eta+26eta^2-3897eta^3 at that pt = {mp.nstr(lb,10)}")

print()
print("=== MAIN at theta*=0.057151961, A0=0.396708119308 ===")
ths = mp.mpf('0.057151961'); A0s = mp.mpf('0.396708119308')
best, pt, mu0, eta0 = scan(ths, A0s)
print(f"theta*: mu0={mp.nstr(mu0,8)} eta0={mp.nstr(eta0,8)} w(0)={mp.nstr(w(0,ths),8)}")
print(f"min LHS (theta*) = {mp.nstr(best,12)} at mu={mp.nstr(pt[0],6)} eta={mp.nstr(pt[1],6)} -> {'POSITIVE' if best>0 else 'NEGATIVE'}")
# decompose at the min point
mu, eta = pt
sigma = 1-mu*eta
m0 = a1*W(1-mu, ths) - a0*W(-mu, ths)
mge1 = sum(kap[m]*(a1*W((2*sigma-1)*m/eta-mu+1, ths) - a0*W((2*sigma-1)*m/eta-mu, ths)) for m in range(1,7))
a1F = a1*F(sigma-eta, sigma, eta, ths)
print(f"decompose @min: m0={mp.nstr(m0,10)} m>=1={mp.nstr(mge1,10)} a1F(s-eta)={mp.nstr(a1F,10)} sum={mp.nstr(m0+mge1+a1F,10)}")
