# Track C attempt: re-optimize the 4.896 zero-free-region constant

Target: bellotti-trudgian-yang-2026 Theorem 1 — zeta(s) != 0 for t >= 3,
sigma > 1 - 1/(4.896 log t). The live classical zero-free-region constant
(smaller = larger region); supersedes mossinghoff-trudgian-yang-2022's 5.558691.

## Step 1 (this tick): reproduce the published constant

Final computation (paper line ~2576, proof of Lemma 15 / iteration lemma):
    eta log t > 1.02928 / (a_kappa * w(0) / 2) = 0.204248...
    => A* = 0.204248...,  1/A* = 4.896
Free parameters (stated values extracted from the paper):
    a_kappa = a * kappa
        a     = sum_{1<=k<=K} a_k     = 2919857/828465   (Lemma 12, line ~1883)
        kappa = sum_{0<=m<=M} kappa_m = 433/859          (Lemma 12, line ~1883)
    w(0)     = 5.672787598            (line 530)
    1.02928  = lower bound of C1(mu)+C2(eta) expression at t = exp(76.47)
               (line 2576; C1 from Lemma 14, C2(eta)=13.47 eta - 161 eta^2 - 11896 eta^3)

Falsification test (pre-registered, before the run):
    If 1/(1.02928/(a_kappa*w(0)/2)) computed from the paper's stated
    intermediate values does NOT give 4.896 (within rounding of the stated
    intermediates), then I misidentified the free parameters or misread the
    derivation.

Machine result (reproduce.py, exact Fraction for a_kappa, 50-dp Decimal):
    a_kappa      = 1264298081/711651435 = 1.7765692849
    a_kappa*w0/2 = 5.0390501033
    A_star       = 0.2042607196
    1/A_star     = 4.8957038933
    published    = 4.896
    diff         = -0.000296
VERDICT: reproduces to 4 significant figures (4.8957 rounds to 4.896). PASS.

## Open question (unresolved, blocks an EXACT reproduction claim)
The paper's stated 1.02928 gives 1/A* = 4.8957, but the headline 4.896 would
require a lower bound of 1.02921 (solve A* = 1/4.896). The 0.00007 gap in the
lower bound is larger than the 5-dp rounding of 1.02928 (±0.000005 -> ±0.00002
in 1/A*). Likely the paper's 1.02928 is itself a rounded display value. To
resolve: re-derive the 1.02928 bound from Lemma 14's C1/C2 at t = exp(76.47)
using the paper's exact intermediate constants. NOT yet done.

## Prior-art pre-flight (2026-08-24, tick 166)
Query: arXiv API `cat:math.NT AND all:"zero-free region"`, sortBy=submittedDate
desc, max 12. Result: HTTP 429 (rate-limited) on 5 attempts over ~60 s; no
results returned. Assessment: no KNOWN re-optimization of the 4.896 constant;
the source paper is very recent (arXiv v1, 23 Mar 2026). Not a definitive
negative (API rate-limited) — re-check when the API is available.
Source paper already carded: lit/cards/bellotti-trudgian-yang-2026.md.

## Next
Re-derive the 1.02928 lower bound (resolve the open question), then set up the
re-optimization: vary the trigonometric-polynomial coefficients a_k (Section 4)
and the smoothing parameters (Section 3) to minimize 1/A* (i.e. maximize the
zero-free region) with a modern solver, subject to the paper's constraints.

## Resolution of the open question (tick 175, 2026-08-24 ~05:55 UTC)
Machine: final-bound.py -> machine-run-final-bound.txt. F1-F5 ALL PASS.
- The stated 1.02928 = g(76.47) rounded to 5 dp, where g is the paper's
  displayed polynomial 1.00582 + 1.86088/L - 4.4106/L^2 - 55.0584/L^3
  (g(76.47) = 1.0292773953...).
- g is the exact Taylor polynomial (in 1/L) of C1(1-2.78/L) + C2(1/(6L))
  with the displayed C1/C2 coefficients, rounded to 5 dp (F5: all four
  coefficients within display-rounding tolerance).
- True expression E(76.47) = 1.0292874008 >= g(76.47) (margin 1.0e-5,
  purely display rounding of the polynomial) -> the paper's claimed
  inequality holds with the displayed coefficients (F2).
- B := 1.02928/(a*kappa*w0/2) = 0.2042607196 >= 1/4.896 = 0.2042483660
  (margin 1.235e-5) -> the headline A = 4.896 IS justified by the stated
  intermediates (F3). The README's "0.00007 gap" was a misreading: the
  paper does not need 1.02928 to round to 1.02921; it needs B >= 1/4.896.
  Derived 1/B = 4.8957038933; the headline 4.896 is the 3-dp rounding in
  the WEAKER direction (stated region slightly smaller than proved).
- g decreasing on [ln(3e12), 76.47] (min dg/dL = -0.001640) -> the
  t = exp(76.47) value is the minimum (F4).
- Residual display anomaly (resolved, quantified): the paper's "0.204248"
  for B is a misdisplay — true B from the stated intermediates is
  0.204261; the displayed 0.204248 equals the target 1/4.896 =
  0.2042484. Display-level only: the required inequality B > A holds with
  the true B (margin 1.235e-5).
Ledger: NOTE #33.

## Next
Re-optimization (the actual Track C goal): vary the trigonometric-polynomial
coefficients a_k (Section 4) and smoothing parameters (Section 3) to
minimize 1/B (maximize the zero-free region) with a modern solver, subject
to the paper's constraints. The reproduction leg is now DONE (4.896
justified; exact derived value 4.8957038933 from stated intermediates).
