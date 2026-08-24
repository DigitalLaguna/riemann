#!/usr/bin/env python3
"""Track C: verify the missing-factor-of-kappa hypothesis in the final line of
bellotti-trudgian-yang-2026 (arXiv 2603.21490), Theorem 1 proof.

Paper's final chain (p. 25, verbatim from lit/text, lines 2551-2577):
  (a*kappa/2) f(0) log t > 1.00582 + 1.86088/log t - 4.4106/(log t)^2
                          - 55.0584/(log t)^3
  ... lower-bound by its value at t = exp(76.47), which is 1.02928 ...
  Therefore eta log t > 1.02928/(a*kappa*w(0)/2) = 0.204248 ...

Definition 2 (p. 11, verbatim, lines 452-459):
  f(u) := eta*w(eta*u) * sum_{0<=m<=M} kappa_m * exp(-(2sigma-1)*m*u)
  => f(0) = eta*w(0)*sum_m kappa_m = eta*w(0)*kappa,  kappa := sum_m kappa_m = 433/859.

So (a*kappa/2)*f(0)*log t = (a*kappa/2)*(eta*w(0)*kappa)*log t
                          = (a*kappa^2*w(0)/2) * (eta*log t).
Hence the CORRECT final line is
  eta log t > 1.02928/(a*kappa^2*w(0)/2) = B_paper/kappa,
and the zero-free-region constant is A_correct = 1/B_correct = A_paper*kappa.

Pre-registered falsification tests (tick 188 log, BEFORE the run):
  F1: B_paper = 1.02928/(a*kappa*w(0)/2) does NOT equal 0.2042607196 (the
      recorded machine-run value from final-bound.py) -> I misread the paper's
      parameters (a, kappa, w(0)) or the formula.
  F2: kappa = 1 (i.e. sum_m kappa_m = 1) -> there is no factor-of-kappa issue;
      the paper's final line is correct as written.
  F3: A_correct = A_paper*kappa is NOT < A_paper (i.e. kappa > 1) -> the
      'improvement' goes the wrong way; re-examine the direction.
"""
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 60

# exact parameters (from the paper, carded + machine-verified in claim #33)
a     = Fraction(2919857, 828465)   # sum_{k>=1} a_k (Kadiri [10, Table 5], rationalized)
kappa = Fraction(433, 859)          # sum_{m=0..M} kappa_m (eq (18))
w0    = Decimal("5.672787598")      # w(0) at the paper's theta = 1.1.1338 (line 530)
g     = Decimal("1.02928")          # min of RHS polynomial on [ln(3e12),76.47] (claim #33)

def D(x):
    if isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    return Decimal(x)

# --- the paper's (displayed) final line ---
den_paper  = D(a) * D(kappa) * w0 / 2          # a*kappa*w(0)/2
B_paper    = g / den_paper                     # eta log t > B_paper
A_paper    = 1 / B_paper                       # zero-free-region constant (derived)

# --- the corrected final line (one more factor of kappa) ---
den_corr   = D(a) * D(kappa)**2 * w0 / 2       # a*kappa^2*w(0)/2
B_corr     = g / den_corr                      # = B_paper/kappa
A_corr     = 1 / B_corr                        # = A_paper*kappa

# --- F1: reproduce the recorded machine-run value ---
recorded_B = Decimal("0.20426071956102531158405521177218295730322414643655")
f1 = abs(B_paper - recorded_B) < Decimal("1e-30")

# --- F2: kappa != 1 (factor-of-kappa issue exists) ---
f2 = kappa != 1

# --- F3: A_correct < A_paper (improvement goes the right way) ---
f3 = A_corr < A_paper

print(f"a            = {a} = {D(a):.12f}")
print(f"kappa        = {kappa} = {D(kappa):.12f}")
print(f"w(0)         = {w0}")
print(f"g(76.47)     = {g}")
print()
print(f"den_paper a*kappa*w0/2      = {den_paper}")
print(f"B_paper  = g/den_paper      = {B_paper}")
print(f"recorded (final-bound.py)   = {recorded_B}")
print(f"A_paper  = 1/B_paper        = {A_paper}")
print(f"  (paper Theorem 1 headline = 4.896; 1/4.896 = {1/D('4.896')})")
print()
print(f"den_corr  a*kappa^2*w0/2    = {den_corr}")
print(f"B_corr   = g/den_corr       = {B_corr}")
print(f"B_corr   = B_paper/kappa    = {B_paper/D(kappa)}")
print(f"A_corr   = 1/B_corr         = {A_corr}")
print(f"A_corr   = A_paper*kappa    = {A_paper*D(kappa)}")
print()
print(f"improvement factor (A_paper/A_corr) = kappa = {D(kappa):.12f}")
print()
print(f"F1 B_paper matches recorded 0.2042607196: {f1} -> {'PASS' if f1 else 'FAIL'}")
print(f"F2 kappa != 1 (factor issue exists):      {f2} -> {'PASS' if f2 else 'FAIL'}")
print(f"F3 A_corr < A_paper (right direction):    {f3} -> {'PASS' if f3 else 'FAIL'}")
print(f"VERDICT: {'ALL CHECKS PASS' if all([f1,f2,f3]) else 'SOME CHECK FAILED'}")
