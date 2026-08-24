# Claim: missing factor of kappa in bellotti-trudgian-yang-2026 Theorem 1 final line

Paper: bellotti-trudgian-yang-2026 (carded: lit/cards/bellotti-trudgian-yang-2026.md,
source lit/pdf/bellotti-trudgian-yang-2026.pdf, text lit/text/bellotti-trudgian-yang-2026.txt).
Quotes re-verified against the extracted text 2026-08-24 (tick 194):

  Definition 2 (p. 11, text lines 456-465):
    "f (u) := ηw(ηu) Σ_{0≤m≤M} κm e^{−(2σ−1)mu}   (19)"
    => f(0) = η w(0) Σ_m κm = η w(0) κ.
  eq (18) (p. 11, text lines 444-451), M=6:
    "[κm]_{0≤m≤M} = 1, −851/859, 780/859, −525/859, 171/859, 28/859, −29/859"
  line 1896 (verbatim): "where a := Σ_{1≤k≤K} a_k = 2919857/828465, κ := Σ_{0≤m≤M} κm = 433/859."
  Theorem 1 proof, final line (p. 25, text lines 2540-2565, verbatim):
    "(aκ/2) f(0) log t > C1(1 − 2.78/log t) + C2(1/(6 log t)) − 10^−7
     > 1.00582 + 1.86088/log t − 4.4106/(log t)^2 − 55.0584/(log t)^3"
    "Since the right side is decreasing for t ∈ [H, exp(76.47)], we may
     lower-bound this expression by its value at t = exp(76.47), which is
     1.02928... Therefore η log t > 1.02928/(aκw(0)/2) = 0.204248... > A0 + ε ≥ A + ε, as required."
  w(0) = 5.672787598 (line 530, machine-verified in claim #33).

Logic: the premise (aκ/2) f(0) log t > 1.02928 with f(0) = ηw(0)κ gives
  (aκ/2)(ηw(0)κ) log t > 1.02928  =>  (aκ^2 w(0)/2)(η log t) > 1.02928
  =>  η log t > 1.02928/(aκ^2 w(0)/2) = B_corr.
The paper instead writes η log t > 1.02928/(aκ w(0)/2) = B_paper, i.e. it drops
one factor of κ from the denominator. Since κ = 433/859 < 1, B_corr = B_paper/κ
> B_paper, so the proof actually establishes a STRONGER lower bound than stated.

Machine (kappa-sum.py, exact Fraction arithmetic):
  F1 κ = Σ_m κm = 433/859 exactly (matches paper line 1896) -> PASS
  F2 max_{x∈[0,1]} |Σ κm x^m − 1/(1+x)| = 4.09e-3 < 0.05 (approx property (17)) -> PASS
  F3 κ < 1 (improvement direction correct) -> PASS
  B_paper = 0.2042607196, A_paper = 1/B_paper = 4.8957038933 (paper headline 4.896)
  B_corr  = 0.4052193028, A_corr  = 1/B_corr = A_paper·κ = 2.4677995178
  improvement factor A_paper/A_corr = 1/κ = 1.9838337182
Recorded run: machine-run-kappa-sum.txt. check.sh re-runs kappa-sum.py and
asserts F1-F3 PASS + VERDICT + byte-identical regression.

Residual (not cleared by this claim): whether the REST of the proof (the
derivation of (aκ/2) f(0) log t > 1.02928) is valid. If so, the paper's
4.896 is valid but not tight, and the proof supports the stronger constant
2.468. This claim establishes the missing factor and the resulting constant;
it does not re-audit the rest of the proof.
