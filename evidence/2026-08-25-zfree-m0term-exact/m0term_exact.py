# Exact m=0 term I(theta,mu) = int_0^{2theta cot theta} e^{mu u}(a1 e^{-u}-a0) w(u) du
# (BTY-2026, arXiv:2603.21490 v1, lines 2203-2268; w = Heath-Brown Definition 1,
#  a0 = 1, a1 = 865534/497079). Question: is the m=0 constraint theta >= theta_min
#  (claim #47, from the Taylor-remainder bound R(x) <= x^4/18 on [0,1.3143]) real,
#  or an artifact? If I(theta*, mu) > 0 at theta* = 0.057151961, it is an artifact.
import mpmath as mp
mp.mp.dps = 60

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

def cn(th, n):
    b = 2*th/mp.tan(th)
    return mp.quad(lambda u: u**n*(a1*mp.e**(-u) - a0)*w(u, th), [0, b])

def cstar(th):
    b = 2*th/mp.tan(th)
    return mp.quad(lambda u: u**3*abs(a1*mp.e**(-u) - a0)*w(u, th), [0, b])

def I_exact(th, mu):
    b = 2*th/mp.tan(th)
    return mp.quad(lambda u: mp.e**(mu*u)*(a1*mp.e**(-u) - a0)*w(u, th), [0, b])

th_paper = mp.mpf('1.1338')
print("=== F1 pipeline validation at paper theta = 1.1338 ===")
w0c = w(mp.mpf(0), th_paper)
w0p = mp.sec(th_paper)**2*(th_paper*mp.tan(th_paper) + 3*th_paper/mp.tan(th_paper) - 3)
print(f"w(0) computed = {mp.nstr(w0c,12)}  formula = {mp.nstr(w0p,12)}  paper = 5.672787598  match? {abs(w0c-mp.mpf('5.672787598')) < mp.mpf('5e-8')}")
# w >= 0 on support (Heath-Brown w is non-negative)
b = 2*th_paper/mp.tan(th_paper)
mn = min(w(mp.mpf(i)/2000*b, th_paper) for i in range(2001))
print(f"w >= 0 on [0, {mp.nstr(b,6)}] (grid 2001)? min = {mp.nstr(mn,6)} -> {mn >= 0}")
paper_c = [mp.mpf('0.8763706262'), mp.mpf('0.1200272738'), mp.mpf('0.0203537951'), mp.mpf('0.0004382722')]
ok = True
for n in range(4):
    v = cn(th_paper, n)
    m = abs(v - paper_c[n]) < mp.mpf('5e-9')
    ok = ok and m
    print(f"c{n}: computed = {mp.nstr(v,12)}  paper = {paper_c[n]}  match8? {m}")
cs = cstar(th_paper)
mcs = abs(cs - mp.mpf('0.0190417514')) < mp.mpf('5e-9')
ok = ok and mcs
print(f"c*: computed = {mp.nstr(cs,12)}  paper = 0.0190417514  match8? {mcs}")
print(f"F1 PIPELINE: {'PASS' if ok else 'FAIL'}")

print()
print("=== F2 exact m=0 integral ===")
T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12; K = mp.mpf(16)
mu0 = mp.log(H)/mp.log(K*H + T0)
print(f"mu0 = (1-sigma0)/eta0 = log H/log(KH+T0) = {mp.nstr(mu0,12)} (A0-independent)")
th_star = mp.mpf('0.057151961')
print(f"theta* = {th_star}  2*theta*cot(theta) = {mp.nstr(2*th_star/mp.tan(th_star),10)}")
for mu, lab in [(mu0, 'mu0'), (mp.mpf(1), 'mu=1 (worst case)')]:
    v = I_exact(th_star, mu)
    print(f"I(theta*, {lab}) = {mp.nstr(v,12)}  -> {'POSITIVE' if v > 0 else 'NEGATIVE'}")
for mu, lab in [(mu0, 'mu0'), (mp.mpf(1), 'mu=1')]:
    v = I_exact(th_paper, mu)
    print(f"I(paper theta, {lab}) = {mp.nstr(v,12)}  (reference: paper C1(mu) lower bound)")
# C1(mu) polynomial at paper theta, for reference
C1 = lambda mu: paper_c[0] + paper_c[1]*mu + paper_c[2]*mu**2/2 + (paper_c[3] - cs/18)*mu**3/6
print(f"C1(1) (paper-style polynomial, paper theta) = {mp.nstr(C1(mp.mpf(1)),12)}")
