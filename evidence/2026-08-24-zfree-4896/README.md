# Claim #33 evidence: 4.896 headline justified by stated intermediates

Paper: bellotti-trudgian-yang-2026 (carded: lit/cards/bellotti-trudgian-yang-2026.md,
source lit/pdf/bellotti-trudgian-yang-2026.pdf). Quotes re-verified against the PDF
2026-08-24 (tick 175, pdftotext -layout):

  p. 25: "(a*kappa/2) f(0) log t > C1(1 - 2.78/log t) + C2(1/(6 log t))
         - 1e-7 > 1.00582 + 1.86088/log t - 4.4106/(log t)^2
         - 55.0584/(log t)^3"; "Since the right side is decreasing for
         t in [H, exp(76.47)], we may lower-bound this expression by its
         value at t = exp(76.47), which is 1.02928... Therefore
         eta log t > 1.02928/(a*kappa*w(0)/2) = 0.204248... > A0 + eps
         >= A + eps, as required."
  p. 20 (Lemma 14): "C1(x) := 0.87637 + 0.12002x + 0.01017x^2 - 0.00073x^3"
  p. 25: "C2(eta) := 13.47 eta - 161 eta^2 - 11896 eta^3"
  line 163: "H := 3*10^12"
  Lemma 12: a = 2919857/828465, kappa = 433/859 (exact)
  line 530: w(0) = 5.672787598
  Theorem 1 (line 101): zeta != 0 for sigma > 1 - 1/(4.896 log t), 3 <= t <= exp(76.47)

Logic: proof by contradiction assumes a zero with eta log t < A := 1/4.896
and shows eta log t > B := 1.02928/(a*kappa*w(0)/2); the theorem holds iff B >= A.

Machine: final-bound.py (50-dp Decimal, exact Fraction a*kappa) ->
machine-run-final-bound.txt (recorded run, tick 175). F1-F5 ALL PASS:
  F1 g(76.47)=1.0292773953... rounds to 1.02928 (stated value = displayed
     polynomial g evaluated at L=76.47)
  F2 E(76.47)=1.0292874008 >= g(76.47) (margin 1.0e-5)
  F3 B=0.2042607196 >= 1/4.896=0.2042483660 (margin 1.235e-5) -> headline
     4.896 justified; derived 1/B=4.8957038933, 4.896 is 3-dp rounding in
     the weaker direction
  F4 dg/dL < 0 on [ln(3e12), 76.47] (min -0.001640) -> t=exp(76.47) is the
     minimum, as the paper claims
  F5 Taylor coeffs of E(L)+1e-7 match the paper's polynomial within
     display-rounding tolerance
Residual display anomaly (resolved): paper's "0.204248" for B is a
misdisplay (true B=0.204261; displayed value equals target 1/4.896).

check.sh: re-runs final-bound.py; asserts F1-F5 PASS, VERDICT, and
byte-identical output vs machine-run-final-bound.txt.
