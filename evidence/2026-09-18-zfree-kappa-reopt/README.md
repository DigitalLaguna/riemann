# Track C: kappa_m re-optimization — reproduction gate + threshold (tick 265)

Paper: bellotti-trudgian-yang-2026 (arXiv:2603.21490 v1). Setup: the test
function f uses coefficients kappa_m (0<=m<=M, M=6, eq (18)); the Lemma-1
final line (claim #40) gives A_final, which depends on kappa_m ONLY through
kappa = sum_{0<=m<=M} kappa_m (via the corrected denominator a*kappa^2*w(0)/2,
claim #38). Effective region constant = min(A_final, A0_max); currently
A0_max = 0.392113247395366294 (claim #54) binds (A_final = 0.420483467794 > A0_max).

## Objective
Minimize A_final  <=>  maximize kappa = sum kappa_m (kappa_0 = 1 fixed).
Improvement requires A_final_reopt < A0_max = 0.392113247395366294.

## Machine (kappa-reopt.py, mpmath 60 dps) — see machine-run.txt
REPRODUCTION GATE (paper kappa_m, kappa = 433/859, line 1904):
  A_final(paper) = 0.420483467793734   target (#40) = 0.420483467794
  |diff| = 2.66e-13  -> REPRODUCED (35 iters).  [gate PASS]
THRESHOLD (A_final = A0_max):
  kappa_required = 0.521015891482995  (vs paper kappa = 0.50407450523865)
  required increase = 3.361 %
  self-consistent: A_final(kappa_required) = A0_max (|diff| < 1e-12).

## Verbatim constants used (all checked against lit/text/bellotti-trudgian-yang-2026.txt)
  a = 2919857/828465 (line 1896); kappa = 433/859 (line 1904); w(0)=5.672787598
  (line 530); K=16 (535); T0=1e10 (532); H=3e12 (163); xT=76.47 (Lemma 1 top);
  C1(x)=0.87637+0.12002x+0.01017x^2-0.00073x^3 (line 2068);
  C2(y)=13.47y-161y^2-11896y^3 (line 2527); c_mu_sharp=log(K+T0/H)=log(16+1/300).

## Falsification test (pre-registered, tick 262)
DEAD if re-optimized A_final still > A0_max = 0.392113247395366294.
This tick: gate PASS + threshold computed. NEXT: extract the paper's
constraints on kappa_m (p(x)>0 on (0,1]; B(y)>=0 for all y in R, line 696;
lemma 5-14 bounds) and solve  max kappa  s.t. constraints. If max kappa <
0.521015891482995, the idea is DEAD (record in DEAD_ENDS).

## Status
No new ledger claim yet (setup step; machine says the transcription is correct
and gives the exact threshold). Next tick: constrained optimization.
