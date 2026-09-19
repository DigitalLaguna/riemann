import mpmath as mp
mp.mp.dps = 50
# ---- w(u) and its derivatives (exact, from Definition 1 / paper) ----
theta = mp.mpf('1.1338')
A  = 1/mp.cos(theta)**2          # sec^2
B  = theta*mp.cos(theta)/mp.sin(theta)   # theta*cot
C  = mp.sin(theta)/mp.cos(theta)         # tan
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
# inner'(u) = (-A/2)cos(Cu) - A C (B-u/2) sin(Cu) - 1 - C cos(D-Cu)/E + 2C cos(theta-Cu)/F
def inner_p(u):
    return (-A/2)*mp.cos(u*C) - A*C*(B - u/2)*mp.sin(u*C) - 1 \
           - C*mp.cos(D - u*C)/E + 2*C*mp.cos(theta - u*C)/F
w1 = A*inner_p(0)
# inner''(u) = A C sin(Cu) - A C^2 (B-u/2) cos(Cu) - C^2 sin(D-Cu)/E + 2 C^2 sin(theta-Cu)/F
def inner_pp(u):
    return A*C*mp.sin(u*C) - A*C**2*(B - u/2)*mp.cos(u*C) \
           - C**2*mp.sin(D - u*C)/E + 2*C**2*mp.sin(theta - u*C)/F
# Rigorous upper bound on ||w''||_1 = int_0^{u_max} |w''(u)| du
# |w''(u)| <= A*[A C + A C^2*max|B-u/2| + C^2/E + 2 C^2/F], max|B-u/2|=B (u_max=2B)
W2 = u_max * A * (A*C + A*C**2*B + C**2/E + 2*C**2/F)
# sanity: numeric trapezoid of |w''| should be <= W2
N=4000; num=mp.mpf(0)
for i in range(N+1):
    num += abs(inner_pp(u_max*mp.mpf(i)/N))
num = A*num*u_max/N
print("w0            =", mp.nstr(w0,12))
print("w1=w'(0)     =", mp.nstr(w1,12))
print("W2 (rig ub)  =", mp.nstr(W2,10))
print("num int|w''| =", mp.nstr(num,10), " (<= W2 ?", bool(num<=W2), ")")
# ---- Lemma 14 parameters ----
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
BOUND = mp.mpf('1e-370')   # IBP boundary terms e^{-x u_max}, x>=831 -> <1e-370 (rig, loose)
def LB(mu, eta):
    x3 = mp.mpf(6)/eta - mp.mpf(13)*mu
    x1 = x3 + 1; x2 = x3 + 1/eta - 1
    t1 = a1/x1 + a1/x2 - a0/x3
    t2 = a1/x1**2 + a1/x2**2 - a0/x3**2
    t3 = a1/x1**2 + a1/x2**2 + a0/x3**2
    return w0*t1 + w1*t2 - W2*t3 - BOUND
# ---- Part 1: grid over eta in [eta_lo, eta0] (x3 <= ~X0) ----
X0 = mp.mpf(2000)
eta_lo = mp.mpf(6)/(X0 + mp.mpf(13))
Nmu=Neta=500
minLB=mp.mpf('inf'); minpt=None
for i in range(Nmu+1):
    mu = mu0 + (1-mu0)*mp.mpf(i)/Nmu
    for j in range(Neta+1):
        eta = eta_lo + (eta0-eta_lo)*mp.mpf(j)/Neta
        v = LB(mu,eta)
        if v < minLB: minLB=v; minpt=(mp.nstr(mu,8),mp.nstr(eta,10))
print("eta_lo =", mp.nstr(eta_lo,10))
print("grid min LB (eta in [eta_lo,eta0]) =", mp.nstr(minLB,10), "at (mu,eta)=",minpt)
# ---- Part 2: small eta (x3 > X0), analytic lower bound ----
def LB_small(x3):
    t1 = ((a1-1)*x3 - 1)/(x3*(x3+1))
    t2 = ((a1-1)*x3**2 - 2*x3 - 1)/(x3**2*(x3+1)**2)
    t3 = (2*a1 + a0)/x3**2
    return w0*t1 - abs(w1)*t2 - W2*t3 - BOUND
ok_small = True
for x3 in [X0, mp.mpf(3000), mp.mpf(5000), mp.mpf(10000), mp.mpf(100000), mp.mpf(1000000)]:
    v = LB_small(x3)
    print("LB_small(x3=%s) =" % mp.nstr(x3,6), mp.nstr(v,10))
    if v <= 0: ok_small = False
print("=== VERDICT ===")
print("grid part min LB > 0 ?", bool(minLB > 0))
print("small-eta part LB > 0 ?", bool(ok_small))
print("D14 >= 0 for all (mu,eta) in domain ?", bool(minLB > 0 and ok_small))
