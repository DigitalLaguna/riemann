#!/usr/bin/env python3
"""Track C: machine-verify kappa = sum_m kappa_m = 433/859 from eq (18) of
bellotti-trudgian-yang-2026, and confirm the coefficients via the approximation
property (17): sum_m kappa_m x^m ~= 1/(1+x) uniformly for x in [0,1].

Coefficients from eq (18) (p. 11, M=6, verbatim from lit/text lines 444-451):
  [kappa_m] = 1, -851/859, 780/859, -525/859, 171/859, 28/859, -29/859

Pre-registered falsification tests (tick 194, BEFORE the run):
  F1: sum_m kappa_m != 433/859 -> I mis-parsed the eq (18) coefficients; the
      missing-factor-of-kappa hypothesis (kappa-factor.py) used the wrong kappa.
  F2: max_{x in [0,1]} |sum_m kappa_m x^m - 1/(1+x)| > 0.05 -> the coefficients
      do NOT approximate 1/(1+x), so I have the wrong coefficient set (sign error).
  F3: kappa >= 1 -> the 'improvement' A_corr = A_paper*kappa goes the wrong way.
"""
from fractions import Fraction
import math

# eq (18) coefficients, m = 0..6
km = [Fraction(1),
      Fraction(-851, 859),
      Fraction(780, 859),
      Fraction(-525, 859),
      Fraction(171, 859),
      Fraction(28, 859),
      Fraction(-29, 859)]

kappa = sum(km)
print("kappa_m =", [str(c) for c in km])
print("kappa = sum kappa_m =", kappa, "=", float(kappa))

# F1: kappa == 433/859 ?
f1 = (kappa == Fraction(433, 859))
print("F1 kappa == 433/859:", f1, "->", "PASS" if f1 else "FAIL")

# F2: approximation property (17): sum kappa_m x^m ~= 1/(1+x) on [0,1]
def poly(x):
    return sum(c * x**m for m, c in enumerate(km))
N = 20001
maxerr = 0.0
worst = 0.0
for i in range(N):
    x = i / (N - 1)
    err = abs(float(poly(x)) - 1.0 / (1.0 + x))
    if err > maxerr:
        maxerr = err
        worst = x
print(f"F2 max|sum kappa_m x^m - 1/(1+x)| on [0,1] = {maxerr:.6e} at x={worst:.4f}")
f2 = maxerr < 0.05
print("F2 approx property (err < 0.05):", f2, "->", "PASS" if f2 else "FAIL")

# F3: kappa < 1 (so A_corr = A_paper*kappa < A_paper, correct direction)
f3 = kappa < 1
print("F3 kappa < 1:", f3, "->", "PASS" if f3 else "FAIL")

# Full chain: A_paper and A_correct
a = Fraction(2919857, 828465)
w0 = Fraction(5672787598, 10**9)
g = Fraction(102928, 10**5)
B_paper = g * 2 / (a * kappa * w0)      # paper's stated lower bound on eta log t
A_paper = 1 / B_paper                   # zero-free constant = 1/B
B_corr  = g * 2 / (a * kappa**2 * w0)   # correct B (factor kappa in denominator)
A_corr  = 1 / B_corr                    # = A_paper*kappa
print(f"B_paper  = 1.02928*2/(a*kappa*w0)     = {float(B_paper):.10f}")
print(f"A_paper  = 1/B_paper                  = {float(A_paper):.10f}  (paper headline 4.896)")
print(f"B_corr   = 1.02928*2/(a*kappa^2*w0)   = {float(B_corr):.10f}")
print(f"A_corr   = 1/B_corr = A_paper*kappa   = {float(A_corr):.10f}")
print(f"improvement factor A_paper/A_corr     = {float(A_paper/A_corr):.10f} (= 1/kappa)")

verdict = "ALL CHECKS PASS" if (f1 and f2 and f3) else "SOME CHECKS FAIL"
print("VERDICT:", verdict)
