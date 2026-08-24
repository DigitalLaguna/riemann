#!/usr/bin/env python3
"""Resolve the open question of claim #29 (tick 175).

Question: the stated 1.02928 (p. 25) gives 1/A* = 4.8957, but the headline
Theorem 1 constant is 4.896. Is the headline justified by the stated
intermediate values, or is there an unexplained gap?

Paper facts (fetched, quoted verbatim in README):
  p. 25: (a*kappa/2) f(0) log t > C1(1 - 2.78/log t) + C2(1/(6 log t)) - 1e-7
         > 1.00582 + 1.86088/L - 4.4106/L^2 - 55.0584/L^3,  L := log t
         "Since the right side is decreasing for t in [H, exp(76.47)], we may
          lower-bound this expression by its value at t = exp(76.47), which
          is 1.02928... Therefore eta log t > 1.02928/(a*kappa*w(0)/2) =
          0.204248... > A0 + eps >= A + eps, as required."
  p. 20 (Lemma 14): C1(x) := 0.87637 + 0.12002x + 0.01017x^2 - 0.00073x^3
  p. 25: C2(eta) := 13.47 eta - 161 eta^2 - 11896 eta^3
  p. 6 (line 163): H := 3e12
  Lemma 12: a = 2919857/828465, kappa = 433/859 (exact)
  line 530: w(0) = 5.672787598
  Theorem 1 (line 101): zeta != 0 for sigma > 1 - 1/(4.896 log t),
                        3 <= t <= exp(76.47)

Logic: the proof by contradiction assumes a zero with eta log t < A
(A := 1/4.896) and shows eta log t > B := 1.02928/(a*kappa*w0/2).
The theorem holds iff B >= A.

Pre-registered falsification tests (tick 175, BEFORE the run):
  F1: g(76.47) (paper's displayed polynomial) does NOT round to 1.02928 at
      5 dp -> I misread the polynomial or the evaluation point.
  F2: E(76.47) < g(76.47), E = C1(1-2.78/L)+C2(1/(6L))-1e-7 with displayed
      C1/C2 -> the paper's claimed inequality fails with displayed
      coefficients -> I misread C1/C2 or their arguments.
  F3: B < 1/4.896 -> the stated 1.02928 does NOT justify the headline ->
      the open question stays open (a real mismatch, constraint 7).
  F4: dg/dL >= 0 somewhere in [ln(3e12), 76.47] -> the paper's "decreasing"
      claim is false -> the t=exp(76.47) value is not the minimum.
  F5: Taylor coefficients of E(L)+1e-7 in powers of 1/L deviate from the
      paper's polynomial (1.00582, 1.86088, -4.4106, -55.0584) beyond
      display-rounding tolerance -> I misread the formula.
"""
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 50

L = Decimal("76.47")
LH = (Decimal(3) * Decimal(10) ** 12).ln()   # ln(3e12), H := 3e12

a = Fraction(2919857, 828465)
kappa = Fraction(433, 859)
ak = (Decimal(a.numerator) * Decimal(kappa.numerator)
      / (Decimal(a.denominator) * Decimal(kappa.denominator)))
w0 = Decimal("5.672787598")
denom = ak * w0 / 2

P0, P1, P2, P3 = (Decimal("0.87637"), Decimal("0.12002"),
                  Decimal("0.01017"), Decimal("-0.00073"))
Q1, Q2, Q3 = Decimal("13.47"), Decimal("161"), Decimal("11896")
A278 = Decimal("2.78")

def C1(x):
    return P0 + P1 * x + P2 * x * x + P3 * x * x * x

def C2(e):
    return Q1 * e - Q2 * e * e - Q3 * e * e * e

def E(Lv):   # true expression with displayed C1/C2
    return C1(1 - A278 / Lv) + C2(Decimal(1) / (Decimal(6) * Lv)) - Decimal("1e-7")

def g(Lv):   # paper's displayed lower-bound polynomial (p. 25)
    return (Decimal("1.00582") + Decimal("1.86088") / Lv
            - Decimal("4.4106") / (Lv * Lv)
            - Decimal("55.0584") / (Lv * Lv * Lv))

def dg(Lv):  # d/dL of g
    return (-Decimal("1.86088") / (Lv * Lv) + Decimal("8.8212") / (Lv ** 3)
            + Decimal("165.1752") / (Lv ** 4))

# --- Taylor coefficients of E(L) + 1e-7 in powers of 1/L (exact algebra) ---
t0 = P0 + P1 + P2 + P3
t1 = -P1 * A278 - 2 * P2 * A278 - 3 * P3 * A278
t2 = P2 * A278 ** 2 + 3 * P3 * A278 ** 2
t3 = -P3 * A278 ** 3
u1 = Q1 / 6
u2 = -Q2 / 36
u3 = -Q3 / 216
T = (t0, t1 + u1, t2 + u2, t3 + u3)
paper = (Decimal("1.00582"), Decimal("1.86088"), Decimal("-4.4106"),
         Decimal("-55.0584"))
# display-rounding tolerances: C1 coeffs +/-5e-6 (x<=1, a=2.78), C2 coeffs
# 13.47 +/-0.005, 161 +/-0.5, 11896 +/-0.5
tol = (Decimal("0.00002"),
       Decimal("0.000005") * A278 * 6 + Decimal("0.005") / 6,
       Decimal("0.000005") * A278 ** 2 * 4 + Decimal("0.5") / 36,
       Decimal("0.000005") * A278 ** 3 * 2 + Decimal("0.5") / 216)

g76 = g(L)
E76 = E(L)
B = Decimal("1.02928") / denom
A_head = Decimal(1) / Decimal("4.896")

# F4: min of dg/dL on [ln(3e12), 76.47], step 0.01
min_dg, x = None, LH
while x <= L:
    v = dg(x)
    if min_dg is None or v < min_dg:
        min_dg = v
    x += Decimal("0.01")

q5 = g76.quantize(Decimal("0.00001"))
f1 = q5 == Decimal("1.02928")
f2 = E76 >= g76
f3 = B >= A_head
f4 = min_dg < 0
f5 = all(abs(T[i] - paper[i]) <= tol[i] for i in range(4))

print(f"ln(3e12)        = {LH}")
print(f"a*kappa*w0/2    = {denom}")
print(f"g(76.47)        = {g76}")
print(f"E(76.47)        = {E76}")
print(f"E - g           = {E76 - g76}")
print(f"B = 1.02928/den = {B}")
print(f"1/4.896         = {A_head}")
print(f"B - 1/4.896     = {B - A_head}")
print(f"1/B             = {Decimal(1) / B}")
print(f"paper display   = 0.204248 (for B); B - display = {B - Decimal('0.204248')}")
print(f"min dg/dL on [ln(3e12),76.47] = {min_dg}")
print(f"Taylor T        = {T}")
print(f"paper poly      = {paper}")
print(f"Taylor diffs    = {tuple(abs(T[i]-paper[i]) for i in range(4))}")
print(f"tolerances      = {tol}")
print()
print(f"F1 g(76.47) rounds to 1.02928: {q5} -> {'PASS' if f1 else 'FAIL'}")
print(f"F2 E(76.47) >= g(76.47):       {f2} -> {'PASS' if f2 else 'FAIL'}")
print(f"F3 B >= 1/4.896:               {f3} -> {'PASS' if f3 else 'FAIL'}")
print(f"F4 dg/dL < 0 on whole range:   {f4} -> {'PASS' if f4 else 'FAIL'}")
print(f"F5 Taylor within tolerance:    {f5} -> {'PASS' if f5 else 'FAIL'}")
print(f"VERDICT: {'ALL CHECKS PASS' if all([f1,f2,f3,f4,f5]) else 'SOME CHECK FAILED'}")
