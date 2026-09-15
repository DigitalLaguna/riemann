#!/usr/bin/env python3
"""Theta-cross A0_max with the EXACT m=0 term (track C, BTY-2026 follow-up to #49).

Setup (#44/#45/#46/#47): under the 7-constraint set, A0_max(theta) =
min(A0_tan(theta), A0_g(theta)); #47 added theta >= theta_min (m=0 Taylor
bound e^x-(1+x+x^2/2+x^3/6) < x^4/18 valid only on [0, 2*theta*cot(theta)]
subset of [0, x_max]). This script replaces the Taylor bound by the exact
m=0 term: new constraint fulltotal(theta, A0) = min LHS >= 0 (exact W
quadrature, no Taylor bound).

Hypothesis: A0_g decreases 0.3967 (theta*=0.0572) -> 0.3506 (theta_min=0.9802)
while the exact full total at A0=A0_g(theta) increases in theta (exact m=0
term crosses 0 near theta~0.4-0.5, #48/#49). New A0_max = A0_g(theta_cross)
where the grid-min full total crosses 0.

Grids: F1/F2/final use the 7x9 grid (mu in [mu0,1], eta in {eta0/9..eta0})
as in #49; scan/bisect use a 3x3 corner probe (mu in {mu0,(mu0+1)/2,1},
eta in {eta0/9,eta0/3,eta0}) — the observed minimum sits at the corner
(mu=1, eta=eta0/9) (#49). If the final 7x9 min at the bisected point is < 0,
refine with 7x9 bisection steps.

F-tests pre-registered 2026-09-15T22:50Z in logs/2026-09-15.tick.log:
  F1 fulltotal(theta*, A0_g(theta*)) < 0 (reproduces #49)
  F2 fulltotal(theta_min, A0_g(theta_min)) >= 0 (crossing exists)
  F3 theta_cross interior, A0_max_new > 0.350566297741
  F4 all 7 constraints + fine fulltotal >= 0 at (A0_max_new, theta_cross)
"""
import mpmath as mp
import time

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
def A0_tan(th): return xH/(mp.tan(th) + 2*xH/xKT)
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

t_start = time.time()
print(f"start {time.strftime('%FT%TZ', time.gmtime())}")

# ---- F1: reproduce #49 at theta* (7x9 grid, 30 dps) ----
mp.mp.dps = 30
A0s = A0_g(theta_star)
v1, pt1 = fulltotal(theta_star, A0s)
f1 = v1 < 0
print(f"F1: A0_g(theta*)={mp.nstr(A0s,12)}  fulltotal(theta*,A0_g)={mp.nstr(v1,12)} "
      f"at mu={mp.nstr(pt1[0],6)} eta={mp.nstr(pt1[1],6)}  -> {'PASS (negative, reproduces #49)' if f1 else 'FAIL'}")

# ---- F2: at theta_min (7x9 grid, 30 dps) ----
A0m = A0_g(theta_min)
v2, pt2 = fulltotal(theta_min, A0m)
f2 = v2 >= 0
print(f"F2: A0_g(theta_min)={mp.nstr(A0m,12)}  fulltotal(theta_min,A0_g)={mp.nstr(v2,12)} "
      f"at mu={mp.nstr(pt2[0],6)} eta={mp.nstr(pt2[1],6)}  -> {'PASS (nonnegative, crossing exists)' if f2 else 'FAIL (dead end)'}")

# ---- Phase 1: coarse scan [theta*, 0.5], 3x3 probe, 30 dps ----
# (probe at theta=0.5 already showed H=+0.0008012579354 > 0, tick 230 timing run)
N = 11
print("\n=== coarse scan H(theta)=fulltotal(theta,A0_g(theta)), 3x3 probe, 30 dps ===")
brackets = []
prev_v = None; prev_th = None
for i in range(N):
    th = theta_star + (mp.mpf('0.5') - theta_star)*mp.mpf(i)/mp.mpf(N-1)
    A0 = A0_g(th)
    v, pt = probe(th, A0)
    print(f"  theta={mp.nstr(th,6):<10} A0_g={mp.nstr(A0,10):<14} H={mp.nstr(v,10):<14} "
          f"at mu={mp.nstr(pt[0],5)} eta={mp.nstr(pt[1],6)}")
    if prev_v is not None and prev_v < 0 <= v:
        brackets.append((prev_th, th))
    prev_v, prev_th = v, th
print(f"brackets (H<0 -> H>=0): {[(mp.nstr(a,6), mp.nstr(b,6)) for a,b in brackets]}")

if not brackets:
    print("VERDICT: no sign change on [theta*, 0.5] -> F2/F3 fail, dead end")
    raise SystemExit(1)

# ---- Phase 2: bisect the FIRST (lowest-theta) bracket, 3x3 probe, 30 dps ----
lo, hi = brackets[0]
for it in range(20):
    mid = (lo+hi)/2
    v, _ = probe(mid, A0_g(mid))
    if v < 0: lo = mid
    else: hi = mid
theta_cross = (lo+hi)/2
A0_new = A0_g(theta_cross)
print(f"\nbisected (3x3 probe): theta_cross={mp.nstr(theta_cross,10)}  "
      f"A0_max_new={mp.nstr(A0_new,12)}  (1/A0_max_new={mp.nstr(1/A0_new,10)})")

# ---- Phase 3: fine 7x9 check at the bisected point; refine if negative ----
vf, ptf = fulltotal(theta_cross, A0_new)
refine = 0
while vf < 0 and refine < 5:
    refine += 1
    lo2, hi2 = theta_cross, hi
    for _ in range(4):
        mid = (lo2+hi2)/2
        v, _ = fulltotal(mid, A0_g(mid))
        if v < 0: lo2 = mid
        else: hi2 = mid
    theta_cross = (lo2+hi2)/2
    A0_new = A0_g(theta_cross)
    vf, ptf = fulltotal(theta_cross, A0_new)
    print(f"  refine {refine}: theta_cross={mp.nstr(theta_cross,10)} A0={mp.nstr(A0_new,12)} "
          f"7x9 min={mp.nstr(vf,12)}")
f3 = (theta_cross > theta_star) and (theta_cross < theta_min) and (A0_new > mp.mpf('0.350566297741'))
print(f"F3: interior crossing and A0_max_new > 0.350566297741 (#47): {f3} -> {'PASS' if f3 else 'FAIL'}")

# ---- Phase 4: fine verification, 50 dps ----
mp.mp.dps = 50
A0v = A0_g(theta_cross)
vf50, ptf50 = fulltotal(theta_cross, A0v)
print(f"\n=== FINE verify (50 dps, 7x9) at (A0_g(theta_cross), theta_cross) ===")
print(f"A0={mp.nstr(A0v,12)}  fulltotal={mp.nstr(vf50,12)} at mu={mp.nstr(ptf50[0],6)} eta={mp.nstr(ptf50[1],6)}")

# 100-dps spot check: 3x3 corner
mp.mp.dps = 100
A0h = A0_g(theta_cross)
e0h = A0h/xH; mu0h = (1-(1-A0h/xKT))/e0h
spot = []
for mu in [mu0h, (mu0h+1)/2, 1]:
    for j in [1, 3, 9]:
        spot.append((mu, e0h*mp.mpf(j)/mp.mpf(9), LHS(mu, e0h*mp.mpf(j)/mp.mpf(9), theta_cross, A0h)))
for mu, eta, v in spot:
    print(f"  100dps mu={mp.nstr(mu,6)} eta={mp.nstr(eta,6)}: LHS={mp.nstr(v,12)}")
spotmin = min(v for _, _, v in spot)

# 7 constraints at (A0v, theta_cross), 50 dps
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
print("\n=== 7 constraints at (A0_max_new, theta_cross) ===")
print(f"[1] g = {mp.nstr(g1,10)} <= 1? {c1}")
print(f"[2] C(138,138) LHS={mp.nstr(lhs2,10)} RHS={mp.nstr(rhs2,10)} ratio={mp.nstr(lhs2/rhs2,6)} < 1? {c2}")
print(f"[3] B(y)>0: A0-independent (verified #44)  True")
print(f"[4] eq22 W0-term LHS={mp.nstr(lhs4,10)} RHS={mp.nstr(rhs4,10)} ratio={mp.nstr(lhs4/rhs4,6)} < 1? {c4}")
print(f"[5] Lemma6 A0={mp.nstr(A0,10)} > 1/6? {c5}")
print(f"[6] Lemma14 x1(m=1) = {mp.nstr(x1,10)} > 0? {c6}")
print(f"[7] Lemma13 51*eta0^2/H^2 = {mp.nstr(lhs7,4)} < 5e-13? {c7}")
allc = c1 and c2 and c4 and c5 and c6 and c7
f4 = allc and (vf50 >= 0) and (spotmin >= 0)
print(f"\nF4: all 7 constraints + fine fulltotal>=0 + 100dps spot>=0: {f4} -> {'PASS' if f4 else 'FAIL'}")

print(f"\nVERDICT: theta_cross={mp.nstr(theta_cross,10)}  A0_max_new={mp.nstr(A0_new,12)}  "
      f"constant 1/A0_max_new={mp.nstr(1/A0_new,10)}")
print(f"  #47: 0.350566297741 (2.852527486)   #46 infeasible: 0.396708119308 (2.520744979)")
print(f"  full reopt target #40: 0.420483467794 (2.378214785)")
print(f"OVERALL: {'ALL PASS' if all([f1, f2, f3, f4]) else 'SEE ABOVE'}")
print(f"elapsed {time.time()-t_start:.1f}s")
