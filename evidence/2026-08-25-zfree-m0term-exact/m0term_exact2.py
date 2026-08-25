# Follow-up: (1) c* with the |.| kink at u = log a1 split out (smooth pieces);
# (2) I(theta*, mu) at 100 dps with split intervals (quadrature cross-check);
# (3) I(theta, mu=1) on a theta grid (behavior near theta*).
import mpmath as mp
mp.mp.dps = 100

def w(u, th):
    b = 2*th/mp.tan(th)
    if u < 0 or u > b:
        return mp.mpf(0)
    s2 = mp.sec(th)**2
    return s2*(s2*(th/mp.tan(th) - u/2)*mp.cos(u*mp.tan(th)) + 2*th/mp.tan(th) - u
               + mp.sin(2*th - u*mp.tan(th))/mp.sin(2*th)
               - 2*(1 + mp.sin(th - u*mp.tan(th))/mp.sin(th)))

a0 = mp.mpf(1)
a1 = mp.mpf(865534)/mp.mpf(497079)
uk = mp.log(a1)   # kink: a1 e^{-u} = a0

th_paper = mp.mpf('1.1338')
b = 2*th_paper/mp.tan(th_paper)
# c* split at the kink
cs_split = mp.quad(lambda u: u**3*(a1*mp.e**(-u) - a0)*w(u, th_paper), [0, uk]) \
         + mp.quad(lambda u: u**3*(a0 - a1*mp.e**(-u))*w(u, th_paper), [uk, b])
print(f"c* split at u=log(a1)={mp.nstr(uk,10)}: {mp.nstr(cs_split,15)}")
print(f"paper c* = 0.0190417514  diff = {mp.nstr(cs_split-mp.mpf('0.0190417514'),3)}  match8? {abs(cs_split-mp.mpf('0.0190417514')) < mp.mpf('5e-9')}")

def I_exact(th, mu):
    bb = 2*th/mp.tan(th)
    return mp.quad(lambda u: mp.e**(mu*u)*(a1*mp.e**(-u) - a0)*w(u, th), [0, bb])

T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12; K = mp.mpf(16)
mu0 = mp.log(H)/mp.log(K*H + T0)
th_star = mp.mpf('0.057151961')
print()
print("=== I(theta*, mu) at 100 dps, split at kink ===")
for mu, lab in [(mu0, 'mu0'), (mp.mpf(1), 'mu=1')]:
    bb = 2*th_star/mp.tan(th_star)
    v = mp.quad(lambda u: mp.e**(mu*u)*(a1*mp.e**(-u) - a0)*w(u, th_star), [0, uk]) \
      + mp.quad(lambda u: mp.e**(mu*u)*(a1*mp.e**(-u) - a0)*w(u, th_star), [uk, bb])
    v2 = I_exact(th_star, mu)
    print(f"I(theta*, {lab}) = {mp.nstr(v,15)}  (unsplit: {mp.nstr(v2,15)}, agree? {abs(v-v2) < mp.mpf('1e-40')})")
print()
print("=== I(theta, mu=1) grid (sign structure) ===")
for th in ['0.02', '0.05', '0.057151961', '0.1', '0.3', '0.5', '0.980175494979', '1.1338']:
    v = I_exact(mp.mpf(th), mp.mpf(1))
    print(f"theta={th}: I = {mp.nstr(v,10)}")
