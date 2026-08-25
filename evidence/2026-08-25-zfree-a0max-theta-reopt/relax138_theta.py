#!/usr/bin/env python3
"""Track C 138-relax, step 2: re-optimize theta for the A0_max objective.

Claim #45 fixed theta = 1.1338 (the paper's value, chosen for the 4.896
constant, Theorem 1) and found the binding wall g(A0) < 1 at A0 = 0.3242.
Here we ask: is theta = 1.1338 optimal for the A0_max objective?

g(A0;theta) = eta0(A0)^2 * C(L(A0),L(A0);theta) / [eps0 (2 sigma0(A0)-1) w0(theta)]
  w0(theta) = sec^2(theta)(theta tan theta + 3 theta cot theta - 3)   (denominator)
  C(nu,r;theta) = Lemma 4 (Ford) constant, depends on theta (numerator)
Feasibility also requires r = L(A0) > tan(theta)  (Lemma 4 requirement).

For fixed theta, g is increasing in A0, so A0_g(theta) = max{A0: g<1} (bisection).
A0_tan(theta) = max{A0: L(A0) > tan theta} = xH/(tan theta + 2 xH/xKT).
A0_max(theta) = min(A0_g(theta), A0_tan(theta)).

Pre-registered falsification tests (tick 215, BEFORE the run):
  F1: A0_max(1.1338) != 0.324204954225 (6 dp) -> my g(A0;theta) transcription
      is wrong (should reproduce claim #45 exactly).
  F2: g(A0=0.3242; theta) is NOT monotonically decreasing in theta on
      [1.1338, 1.55] -> C(L,L;theta) grows faster than w0(theta) somewhere;
      the 'w0 in denominator helps' intuition is incomplete.
  F3: max_theta A0_max(theta) <= 0.324204954225 -> theta reopt buys NOTHING
      for this wall (dead end; the wall is not theta).
  F4: the maximizing theta* is a boundary point (theta=1.55 or the tan-crossing)
      rather than interior -> the real wall is the tan constraint, not g.
"""
import mpmath as mp
mp.mp.dps = 60

T0   = mp.mpf(10)**10
H    = mp.mpf(3)*mp.mpf(10)**12
K    = mp.mpf(16)
xH   = mp.log(H)
xKT  = mp.log(K*H + T0)
eps0 = mp.mpf(1)/mp.mpf(2000)

def eta0(A0): return A0/xH
def sig0(A0): return 1 - A0/xKT
def L(A0):    return (2*sig0(A0)-1)/eta0(A0)

def w0(th):
    return mp.sec(th)**2*(th*mp.tan(th) + 3*th/mp.tan(th) - 3)

def C(nu, r, th):
    c0 = 1/mp.sin(th) * mp.sec(th)**2
    c1 = (th - mp.sin(th)*mp.cos(th)) * mp.tan(th)**4
    c2 = mp.tan(th)**3 * mp.sin(th)**2
    c3 = (th - mp.sin(th)*mp.cos(th)) * mp.tan(th)**2
    num = c2*(r+1)**2*(mp.e**(-2*nu*th)/mp.tan(th) + 1) + c1*r + c3*r**3
    return c0*r*num/(r**2 - mp.tan(th)**2)**2

def g(A0, th):
    return eta0(A0)**2 * C(L(A0), L(A0), th) / (eps0*(2*sig0(A0)-1)*w0(th))

def A0_tan(th):
    return xH/(mp.tan(th) + 2*xH/xKT)

def A0_g(th):
    lo, hi = mp.mpf('0.01'), mp.mpf(10)
    if g(lo, th) > 1: return mp.mpf('0.01')
    if g(hi, th) < 1: return hi
    for _ in range(200):
        mid = (lo+hi)/2
        if g(mid, th) < 1: lo = mid
        else: hi = mid
    return lo

def A0_max(th):
    return min(A0_tan(th), A0_g(th))

# ---- F1: reproduce claim #45 at theta = 1.1338 ----
th_paper = mp.mpf('1.1338')
A0_45 = A0_max(th_paper)
f1 = abs(A0_45 - mp.mpf('0.324204954225')) < mp.mpf('5e-7')
print(f"F1: A0_max(1.1338) = {mp.nstr(A0_45,12)}   (#45: 0.324204954225)  -> {'PASS' if f1 else 'FAIL'}")

# ---- F2: monotonicity of g in theta at fixed A0 = 0.3242 ----
A0t = mp.mpf('0.3242')
print("\nF2: g(A0=0.3242; theta), w0, C(L,L) as theta rises:")
prev = None
mono = True
for th in [mp.mpf('1.1338'), mp.mpf('1.2'), mp.mpf('1.3'), mp.mpf('1.4'), mp.mpf('1.5'), mp.mpf('1.55')]:
    gv = g(A0t, th)
    if prev is not None and gv > prev: mono = False
    prev = gv
    print(f"  theta={mp.nstr(th,5):<8} g={mp.nstr(gv,10):<14} w0={mp.nstr(w0(th),10):<14} C(L,L)={mp.nstr(C(L(A0t),L(A0t),th),10)}")
f2 = mono
print(f"  g monotonically decreasing in theta: {f2} -> {'PASS' if f2 else 'FAIL'}")

# ---- scan theta for the A0_max maximizer ----
print("\n=== A0_max(theta) scan on [1.1338, 1.56] ===")
lo, hi = mp.mpf('1.1338'), mp.mpf('1.56')
N = 400
best_th, best_A0 = None, mp.mpf('-1')
for i in range(N):
    th = lo + (hi-lo)*mp.mpf(i)/mp.mpf(N-1)
    A0m = A0_max(th)
    if A0m > best_A0:
        best_A0, best_th = A0m, th
    if i % 50 == 0:
        print(f"  theta={mp.nstr(th,5):<8} A0_max={mp.nstr(A0m,10):<14} A0_g={mp.nstr(A0_g(th),10):<14} A0_tan={mp.nstr(A0_tan(th),10):<14} tan={mp.nstr(mp.tan(th),8)}")

# refine around the grid max with golden-section on A0_max (it is min of inc+dec, unimodal-ish)
br = (hi-lo)/N*3
a_b, b_b = max(lo, best_th-br), min(hi, best_th+br)
gr = (mp.sqrt(5)-1)/2
c_ = b_b - gr*(b_b-a_b); d_ = a_b + gr*(b_b-a_b)
fc, fd = A0_max(c_), A0_max(d_)
for _ in range(80):
    if fc < fd:
        a_b, c_, fc = c_, d_, fd
        d_ = a_b + gr*(b_b-a_b); fd = A0_max(d_)
    else:
        b_b, d_, fd = d_, c_, fc
        c_ = b_b - gr*(b_b-a_b); fc = A0_max(c_)
th_star = (a_b+b_b)/2
A0_star = A0_max(th_star)

f3 = A0_star > mp.mpf('0.324204954225')
f4 = (th_star > lo + (hi-lo)*0.01) and (th_star < hi - (hi-lo)*0.01)
print(f"\nVERDICT: theta* = {mp.nstr(th_star,8)}   A0_max(theta*) = {mp.nstr(A0_star,12)}   (1/A0_max = {mp.nstr(1/A0_star,10)})")
print(f"  A0_g(theta*) = {mp.nstr(A0_g(th_star),10)}   A0_tan(theta*) = {mp.nstr(A0_tan(th_star),10)}   tan(theta*) = {mp.nstr(mp.tan(th_star),8)}")
print(f"  #45 (theta=1.1338) = 0.324204954225   target (full reopt) = 0.420483467794")
print(f"F3 max A0_max > 0.3242 (theta reopt helps): {f3} -> {'PASS' if f3 else 'FAIL'}")
print(f"F4 theta* interior (not boundary): {f4} -> {'PASS' if f4 else 'FAIL'}")
print(f"OVERALL: {'ALL PASS' if all([f1,f2,f3,f4]) else 'SEE ABOVE'}")
