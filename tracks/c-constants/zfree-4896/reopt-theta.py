#!/usr/bin/env python3
"""Track C re-optimization, step 1: vary theta (the smoothing parameter).

Paper: bellotti-trudgian-yang-2026 (arXiv 2603.21490), Theorem 1:
  zeta != 0 for sigma > 1 - 1/(4.896 log t), t >= 3.

Final constant (derived, claim #33): C* = (a*kappa*w(0)/2) / g(76.47),
  a     = sum_{k>=1} a_k = 2919857/828465   (Kadiri [10, Table 5], rationalized)
  kappa = sum_m kappa_m = 433/859           (discrete-approx coefficients (18))
  w(0)  = sec^2(theta)*(theta*tan(theta) + 3*theta*cot(theta) - 3)
         = 5.672787598 at the paper's theta = 1.1338
  g(76.47) = 1.02928  (min of the RHS polynomial on [ln(3e12), 76.47], claim #33)

The paper fixes theta = 1.1338 "determined via numerical experimentation"
(p. 8, after Definition 1). This script asks: is theta = 1.1338 actually the
maximizer of w(0) (the only theta-dependent factor in C* if a, kappa, g are
held fixed)? If w(0) is maximized elsewhere, C* could be smaller.

FIRST-ORDER caveat (documented, not hidden): C1 and C2 (hence g(76.47)) also
depend on theta through w(0), S1, S2, (2 sigma - 1) (Lemma 14, eq (41)).
Holding g fixed isolates the DIRECT theta -> w(0) effect only. A full
re-optimization must re-derive C1, C2 at the new theta (follow-up step).

Pre-registered falsification tests (tick 189, BEFORE the run):
  F1: w(0)(1.1338) != 5.672787598 (5 dp) -> I misread the w(0) formula.
  F2: C*(1.1338) != 4.8957 (4 dp) -> my C* formula / inputs are wrong.
  F3: argmax w(0) over [0.5, 1.6] is NOT in (0, pi/2) or is a boundary point
      -> the interior optimum is spurious (check the range).
  F4: w(0) is NOT unimodal on [0.5, 1.6] (multiple local maxima) -> a grid
      search could miss the global max; report all local maxima.
"""
import math
from fractions import Fraction

a = Fraction(2919857, 828465)
kappa = Fraction(433, 859)
g76 = 1.02928          # claim #33: g(76.47), the min of the RHS polynomial
theta_paper = 1.1338
w0_paper = 5.672787598

def w0(theta):
    s, c = math.sin(theta), math.cos(theta)
    return (1.0 / c**2) * (theta * s / c + 3.0 * theta * c / s - 3.0)

def Cstar(theta):
    return (float(a) * float(kappa) * w0(theta) / 2.0) / g76

# --- F1: reproduce the paper's w(0) at theta = 1.1338 ---
w0p = w0(theta_paper)
f1 = abs(w0p - w0_paper) < 5e-8

# --- F2: reproduce the derived constant C* = 4.8957 at theta = 1.1338 ---
Cp = Cstar(theta_paper)
f2 = abs(Cp - 4.8957) < 5e-5

# --- grid search for argmax w(0) on [0.5, 1.6] ---
N = 200001
lo, hi = 0.5, 1.6
best_t, best_w = None, -1.0
prev_slope = None
local_max = []
for i in range(N):
    t = lo + (hi - lo) * i / (N - 1)
    w = w0(t)
    if w > best_w:
        best_w, best_t = w, t
# detect local maxima (sign change of discrete derivative)
ts = [lo + (hi - lo) * i / (N - 1) for i in range(N)]
ws = [w0(t) for t in ts]
for i in range(1, N - 1):
    if ws[i] > ws[i-1] and ws[i] >= ws[i+1]:
        local_max.append((ts[i], ws[i]))

f3 = 0.5 < best_t < 1.6 and best_t < math.pi / 2
# F4: unimodal = exactly one local maximum
f4 = len(local_max) == 1

# refine argmax with golden-section on the bracket around the grid max
import math as _m
def golden_max(f, a_, b_, iters=200):
    gr = (_m.sqrt(5.0) - 1.0) / 2.0
    c_ = b_ - gr * (b_ - a_)
    d_ = a_ + gr * (b_ - a_)
    fc, fd = f(c_), f(d_)
    for _ in range(iters):
        if fc < fd:
            a_, c_, fc = c_, d_, fd
            d_ = a_ + gr * (b_ - a_); fd = f(d_)
        else:
            b_, d_, fd = d_, c_, fc
            c_ = b_ - gr * (b_ - a_); fc = f(c_)
    return 0.5 * (a_ + b_)

# bracket the grid max within +/- 0.01
br = 0.01
a_b, b_b = max(lo, best_t - br), min(hi, best_t + br)
t_star = golden_max(w0, a_b, b_b)
w_star = w0(t_star)
C_star = Cstar(t_star)

print(f"theta_paper      = {theta_paper}")
print(f"w0(theta_paper)  = {w0p:.9f}   (paper: {w0_paper})")
print(f"C*(theta_paper)  = {Cp:.6f}   (claim #33 derived: 4.8957)")
print()
print(f"argmax w0 on [0.5,1.6] (grid+golden): theta* = {t_star:.9f}")
print(f"w0(theta*)        = {w_star:.9f}")
print(f"C*(theta*)        = {C_star:.6f}")
print(f"delta C*          = {C_star - Cp:.6f}  (negative = improvement)")
print(f"local maxima found: {len(local_max)}")
for (tt, ww) in local_max[:5]:
    print(f"   t={tt:.6f}  w0={ww:.9f}")
print()
print(f"F1 w0(1.1338) matches paper (5e-8): {f1} -> {'PASS' if f1 else 'FAIL'}")
print(f"F2 C*(1.1338) matches 4.8957 (5e-5): {f2} -> {'PASS' if f2 else 'FAIL'}")
print(f"F3 argmax interior of (0.5,1.6) and < pi/2: {f3} -> {'PASS' if f3 else 'FAIL'}")
print(f"F4 w0 unimodal (one local max): {f4} -> {'PASS' if f4 else 'FAIL'}")
print(f"VERDICT: {'ALL CHECKS PASS' if all([f1,f2,f3,f4]) else 'SOME CHECK FAILED'}")
