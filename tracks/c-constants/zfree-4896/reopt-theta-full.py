#!/usr/bin/env python3
"""Track C re-optimization, step 2: the FULL theta objective (efficiency).

Step 1 (reopt-theta.py) showed w(0)(theta) alone is UNBOUNDED on (0, pi/2)
(diverges as theta -> pi/2), so it is not the paper's objective. The paper's
theta = 1.1338 must optimize the efficiency (p. 8):

    (a1 F(0) - a0 F(-eta))/f(0) = (c + O(eta)) (a1 W(0) - a0 W(-1))/(eta w(0))

where W is the Laplace transform of w (Definition 1), c = 1/kappa. For fixed
eta, a0, a1, c the theta-dependent part is

    E(theta) = (a1 W(0)(theta) - a0 W(-1)(theta)) / w(0)(theta)

This script computes W(0), W(-1) by numerical integration of the Definition-1
w(u) over its support [0, 2 theta cot theta], verifies the transcription by
checking w_full(0) == the closed form sec^2(theta)(theta tan theta + 3 theta
cot theta - 3), then locates the maximizer of E(theta).

Pre-registered falsification tests (tick 189, BEFORE the run):
  F1: w_full(0; 1.1338) != 5.672787598 (1e-6 rel) -> I mis-transcribed w(u).
  F2: E(1.1338) is NOT within 5% of the global max of E on [0.6, 1.5]
      -> the efficiency is not the paper's objective (or my W is wrong).
  F3: argmax E is a boundary point of [0.6, 1.5] -> the interior optimum is
      spurious; widen the range.
  F4: E is not unimodal (multiple local maxima) -> report all; grid may miss.
"""
import math
from fractions import Fraction

a0 = 1.0
a1 = float(Fraction(865534, 497079))

def w_full(u, th):
    s, c = math.sin(th), math.cos(th)
    sec2 = 1.0 / c**2
    csc2 = 1.0 / s**2
    cot = c / s
    tan = s / c
    A = sec2 * (th * cot - u / 2.0) * math.cos(u * tan)
    B = 2.0 * th * cot - u
    C = math.sin(2.0 * th - u * tan) / math.sin(2.0 * th)  # csc(2 theta)
    D = -2.0 * (1.0 + math.sin(th - u * tan) / s)
    return sec2 * (A + B + C + D)

def w0_closed(th):
    s, c = math.sin(th), math.cos(th)
    return (1.0 / c**2) * (th * s / c + 3.0 * th * c / s - 3.0)

def laplace(z, th, N=200000):
    # W(z) = integral_0^{2 th cot th} e^{-z u} w(u) du, trapezoidal
    ub = 2.0 * th * math.cos(th) / math.sin(th)
    if ub <= 0:
        return 0.0
    h = ub / N
    total = 0.5 * (math.exp(-z * 0.0) * w_full(0.0, th))
    for i in range(1, N):
        u = i * h
        total += math.exp(-z * u) * w_full(u, th)
    total += 0.5 * math.exp(-z * ub) * w_full(ub, th)
    return total * h

def E(th):
    W0 = laplace(0.0, th)
    Wm1 = laplace(-1.0, th)
    return (a1 * W0 - a0 * Wm1) / w0_closed(th)

# F1: transcription check at theta = 1.1338
thp = 1.1338
wf0 = w_full(0.0, thp)
wc0 = w0_closed(thp)
f1 = abs(wf0 - wc0) / wc0 < 1e-6
print(f"F1 check: w_full(0;1.1338)={wf0:.9f}  w0_closed={wc0:.9f}  rel={abs(wf0-wc0)/wc0:.2e}")

# scan E(theta) on [0.6, 1.5]
lo, hi, N = 0.6, 1.5, 300
ts = [lo + (hi - lo) * i / (N - 1) for i in range(N)]
Es = [E(t) for t in ts]
imax = max(range(N), key=lambda i: Es[i])
local_max = []
for i in range(1, N - 1):
    if Es[i] > Es[i-1] and Es[i] >= Es[i+1]:
        local_max.append((ts[i], Es[i]))
f3 = lo < ts[imax] < hi
f4 = len(local_max) == 1
f2 = Es[imax] > 0 and Es[ts.index(min(ts, key=lambda t: abs(t - thp)))] > 0.95 * Es[imax]

print(f"E(1.1338)        = {E(thp):.9f}")
print(f"argmax E on [0.6,1.5]: theta* = {ts[imax]:.6f}  E = {Es[imax]:.9f}")
print(f"local maxima: {len(local_max)}")
for (tt, ee) in local_max[:5]:
    print(f"   t={tt:.6f}  E={ee:.9f}")
print()
print(f"F1 w_full(0) matches closed form (1e-6 rel): {f1} -> {'PASS' if f1 else 'FAIL'}")
print(f"F2 E(1.1338) within 5% of global max: {f2} -> {'PASS' if f2 else 'FAIL'}")
print(f"F3 argmax interior of [0.6,1.5]: {f3} -> {'PASS' if f3 else 'FAIL'}")
print(f"F4 E unimodal (one local max): {f4} -> {'PASS' if f4 else 'FAIL'}")
print(f"VERDICT: {'ALL CHECKS PASS' if all([f1,f2,f3,f4]) else 'SOME CHECK FAILED'}")
