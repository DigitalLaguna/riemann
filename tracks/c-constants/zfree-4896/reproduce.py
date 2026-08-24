# Reproduce the 4.896 zero-free-region constant of bellotti-trudgian-yang-2026
# (Theorem 1: zeta(s) != 0 for t>=3, sigma > 1 - 1/(4.896 log t)).
# Final computation (paper line ~2576):
#   eta log t > 1.02928 / (a_kappa * w(0) / 2) = 0.204248...
#   => A* = 0.204248..., 1/A* = 4.896
# Free parameters (stated values from the paper):
#   a_kappa = a*kappa, a = sum_{1<=k<=K} a_k = 2919857/828465 (Lemma 12)
#             kappa = sum_{0<=m<=M} kappa_m = 433/859 (Lemma 12)
#   w(0) = 5.672787598 (line 530)
#   1.02928 = lower bound of C1(mu)+C2(eta) expression at t=exp(76.47) (line 2576)
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 50

a = Fraction(2919857, 828465)
kappa = Fraction(433, 859)
a_kappa = a * kappa
w0 = Decimal("5.672787598")
lower = Decimal("1.02928")

ak_dec = Decimal(a_kappa.numerator) / Decimal(a_kappa.denominator)
denom = ak_dec * w0 / 2
A_star = lower / denom
result = 1 / A_star

print(f"a       = {a} = {float(a):.10f}")
print(f"kappa   = {kappa} = {float(kappa):.10f}")
print(f"a_kappa = {a_kappa} = {float(a_kappa):.10f}")
print(f"w0      = {w0}")
print(f"lower   = {lower}")
print(f"a_kappa*w0/2 = {denom}")
print(f"A_star  = {A_star}")
print(f"1/A_star = {result}")
print(f"published 4.896; diff = {result - Decimal('4.896')}")
