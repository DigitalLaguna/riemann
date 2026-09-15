# Checker for claim: A0_max >= 0.392113247328 (track C, BTY-2026 exact m=0 term).
# Self-contained: re-runs the 3x3-probe bisection to recover the full-precision
# crossing theta_cross, then verifies at (A0=A0_g(theta_cross), theta_cross):
#   (a) fine 7x9 grid exact fulltotal >= 0 (50 dps)
#   (b) 100-dps corner spot >= 0
#   (c) all 7 constraints of the #44/#45/#46 set hold (50 dps)
# Exits 0 iff all hold. Mirrors theta_cross.py (tick 230) exactly.
import mpmath as mp
import sys, time

T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12; K = mp.mpf(16)
xH = mp.log(H); xKT = mp.log(K*H + T0); eps0 = mp.mpf(1)/mp.mpf(2000)
theta_min = mp.mpf('0.980175494979204')
theta_star = mp.mpf('0.057151961')

def eta0(A0): return A0/xH
def sig0(A0): return 1 - A0/xKT
def L(A0): return (2*sig0(A0)-1)/eta0(A0)
def w0(th): return mp.sec(th)**2*(th*mp.tan(th) + 3*th/mp.tan(th) - 3)
def C(nu, r, th):
    c0 = 1/mp.sin(th)*mp.sec(th)**2
    c1 = (th - mp.sin(th)*mp.cos(th))*mp.tan(th)**4
    c2 = mp.tan(th)**3*mp.sin(th)**2
    c3 = (th - mp.sin(th)*mp.cos(th))*mp.tan(th)**2
    num = c2*(r+1)**2*(mp.e**(-2*nu*th)/mp.tan(th) + 1) + c1*r + c3*r**3
    return c0*r*num/(r**2 - mp.tan(th)**2)**2
def g(A0, th):
    return eta0(A0)**2*C(L(A0), L(A0), th)/(eps0*(2*sig0(A0)-1)*w0(th))
def A0_g(th):
    lo, hi = mp.mpf('0.001'), mp.mpf(10)
    if g(lo, th) > 1: return mp.mpf('0.001')
    if g(hi, th) < 1: return hi
    for _ in range(170):
        mid = (lo+hi)/2
        if g(mid, th) < 1: lo = mid
        else: hi = mid
    return lo

kap = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
       mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
a0 = mp.mpf(1); a1 = mp.mpf(865534)/mp.mpf(497079)

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

def fulltotal(th, A0, nmu=7, neta=9):
    sigma0 = 1 - A0/xKT; e0 = A0/xH; mu0 = (1-sigma0)/e0
    best = None; bestpt = None
    for i in range(nmu):
        mu = mu0 + (1-mu0)*mp.mpf(i)/mp.mpf(nmu-1)
        for j in range(neta):
            v = LHS(mu, e0*mp.mpf(j+1)/mp.mpf(neta), th, A0)
            if best is None or v < best: best, bestpt = v, (mu, e0*mp.mpf(j+1)/mp.mpf(neta))
    return best, bestpt

def probe(th, A0):
    sigma0 = 1 - A0/xKT; e0 = A0/xH; mu0 = (1-sigma0)/e0
    best = None; bestpt = None
    for mu in [mu0, (mu0+1)/2, 1]:
        for eta in [e0/9, e0/3, e0]:
            v = LHS(mu, eta, th, A0)
            if best is None or v < best: best, bestpt = v, (mu, eta)
    return best, bestpt

t0 = time.time()
# --- recover full-precision crossing: same bracket + bisection as theta_cross.py ---
mp.mp.dps = 30
span = mp.mpf('0.5') - theta_star
lo = theta_star + span*mp.mpf(7)/mp.mpf(10)   # th_7 = 0.3671455883...
hi = theta_star + span*mp.mpf(8)/mp.mpf(10)   # th_8 = 0.4114303922...
for _ in range(20):
    mid = (lo+hi)/2
    v, _ = probe(mid, A0_g(mid))
    if v < 0: lo = mid
    else: hi = mid
theta_cross = (lo+hi)/2
A0v = A0_g(theta_cross)
print(f"theta_cross={mp.nstr(theta_cross,20)}  A0=A0_g={mp.nstr(A0v,16)}  "
      f"1/A0={mp.nstr(1/A0v,12)}")

# --- fine 7x9 verification at 50 dps ---
mp.mp.dps = 50
vf, ptf = fulltotal(theta_cross, A0v)
ok_grid = vf >= 0
print(f"fine 7x9 (50dps) min fulltotal = {mp.nstr(vf,12)} at mu={mp.nstr(ptf[0],6)} "
      f"eta={mp.nstr(ptf[1],6)} -> {'PASS' if ok_grid else 'FAIL'}")

# --- 100-dps corner spot ---
mp.mp.dps = 100
e0h = A0v/xH; mu0h = (1-(1-A0v/xKT))/e0h
spot = LHS(mp.mpf(1), e0h/mp.mpf(9), theta_cross, A0v)
ok_spot = spot >= 0
print(f"100dps corner (mu=1, eta=eta0/9) LHS = {mp.nstr(spot,12)} -> {'PASS' if ok_spot else 'FAIL'}")

# --- 7 constraints at 50 dps ---
mp.mp.dps = 50
A0 = A0v; th = theta_cross
g1 = g(A0, th)
lhs2 = eta0(A0)**2*C(138, 138, th); rhs2 = eps0*(2*sig0(A0)-1)*w0(th)
rT = T0/eta0(A0)
lhs4 = eta0(A0)**2*(C(-1, rT, th) + C(0, rT, th)); rhs4 = mp.mpf('5.7')*T0
mu0c = (1-sig0(A0))/eta0(A0) - mp.mpf('1e-10')
x1 = (2*sig0(A0)-1) - mu0c*eta0(A0)
lhs7 = 51*eta0(A0)**2/H**2
c1 = g1 <= 1 + mp.mpf('1e-9')
c2 = lhs2 < rhs2
c4 = lhs4 < rhs4
c5 = A0 > 1/mp.mpf(6)
c6 = x1 > 0
c7 = lhs7 < mp.mpf('5e-13')
allc = c1 and c2 and c4 and c5 and c6 and c7
print(f"constraints: g<=1 {c1}  C138 {c2}  eq22 {c4}  A0>1/6 {c5}  x1>0 {c6}  lem13 {c7}")
ok = ok_grid and ok_spot and allc
print(f"CHECK A0_max>=0.392113247328 (A0={mp.nstr(A0v,12)}): "
      f"{'PASS' if ok else 'FAIL'}")
print(f"elapsed {time.time()-t0:.1f}s")
sys.exit(0 if ok else 1)
