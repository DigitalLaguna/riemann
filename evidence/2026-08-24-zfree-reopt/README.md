# Track C: re-optimization of the BTY-2026 (arXiv:2603.21490) Lemma-1 final line

Paper: bellotti-trudgian-yang-2026 (carded lit/cards/bellotti-trudgian-yang-2026.md,
text lit/text/bellotti-trudgian-yang-2026.txt). Theorem 1: zeta != 0 for
sigma > 1 - 1/(4.896 log t), t >= 3 (line 98). Lemma 1 covers 3 <= t <= exp(76.47).

## What the final line does (verbatim structure, lines 2525-2577)
  (a kappa/2) f(0) log t >= C1(mu) + C2(eta) - 1e-7          (Lemma 14)
  C1(x) = 0.87637 + 0.12002 x + 0.01017 x^2 - 0.00073 x^3   (line 2068)
  C2(y) = 13.47 y - 161 y^2 - 11896 y^3                      (line 2527)
  mu > 1 - 2.78/log t,  eta > 1/(6 log t)                    (lines 2530-2540)
  => (a kappa/2) f(0) log t > C1(1-2.78/log t) + C2(1/(6 log t)) - 1e-7
     > 1.00582 + 1.86088/log t - 4.4106/(log t)^2 - 55.0584/(log t)^3
  RHS decreasing on [H, exp(76.47)] => min at t=exp(76.47) = 1.02928...
  => eta log t > 1.02928/(a kappa w(0)/2) = 0.204248...      (line 2576, MISSING one kappa)

## Free parameters in the final line and their sharp values
  c_mu : paper 2.78  ->  sharp log(K + T0/H) = log(16 + 1/300) = 2.77279703387
         (from mu = log t / log(Kt+T0) >= 1 - log(K+T0/H)/log t; K=16 line 535,
          T0=1e10 line 532, H=3e12 line 163)
  c_eta: paper 6 (eta > 1/(6 log t), "in light of A > 1/6")
         ->  sharp eta > A/log t directly from assumption (43) A <= eta log t
         (line 2357). This is a FIXED POINT in A: A = [C1(1-c_mu/x)+C2(A/x)-1e-7]/denom.
  denom: paper (a kappa w(0)/2) = 5.03905010328  ->  corrected (a kappa^2 w(0)/2)
         = 2.54005668768  (claim #38, missing factor of kappa; a=2919857/828465,
         kappa=433/859 line 1896, w(0)=5.672787598 line 530).

## Machine (reopt.py, mpmath 60 dps) — see machine-run.txt
  CASE 1 (paper: c_mu=2.78, eta=1/(6x), denom_paper):
      B = 0.204262188243, headline 1/B = 4.89566869229  (~ paper 4.896)
      [reproduces the paper; 1.5e-6 gap vs README #38's 0.2042607196 is the
       paper's 5-digit truncation 1.02928 of the exact 1.029287401]
  CASE 2 (corrected kappa^2, no fixed point):
      B = 0.405222216399, headline 1/B = 2.46778177388  (= claim #38's 2.4678)
  CASE 3 (RE-OPTIMIZED: sharp c_mu, sharp eta=A/x fixed point, corrected kappa^2):
      A* = 0.420483467794, headline 1/A* = 2.37821478511  (converged, 32 iters)
      numerator decreasing on [log H, 76.47] => min at x=76.47 (verified, 201 pts)
  A0 CONSTRAINT (table line 545: Lemma 1 A0 = (4.8596)^-1 = 0.205778253354):
      lemmas 5-14 are stated with eta <= A0/log t, so the region constant must
      satisfy A <= A0. Effective constant = min(A_final, A0):
        paper     A_final=0.2042622 < A0  => effective 4.8957 (paper's 4.896)
        corrected A_final=0.4052222 > A0  => effective 4.8596 (A0 binds)
        reopt     A_final=0.4204835 > A0  => effective 4.8596 (A0 binds)
  Provenance of A0=4.8596: NOT Lemma-1's own paper-formula fixed point
      (that is 4.8657, both c_mu=2.78 and sharp); it matches Lemma 2's constant
      4.8594 (line 146) within 0.0002 => A0 is derived from Lemma 2, rounded up.

## Result
Re-optimizing the final line widens the zero-free region from 4.896 to
A_final = 2.3782 (2.058x), but the lemmas' A0 constraint caps the UNCONDITIONAL
constant at 4.8596. Immediate gain: 4.896 -> 4.8596 (0.75%). Path to 2.3782:
re-audit lemmas 5-14 to raise A0 from 0.2057782 to 0.4204835 (i.e. extend the
eta-range from A0/log t to A*/log t).

## Falsification tests (pre-registered)
  F1: if CASE 1 does not reproduce B_paper ~ 0.20426 (within 1e-5), the C1/C2/
      denom transcription is wrong and the whole re-opt is void.  -> PASS (1.5e-6)
  F2: if A_final <= A0, then A0 is NOT binding and re-opt gives > 4.8596 directly.
      -> A_final = 0.42048 > A0 = 0.20578, so A0 IS binding (hypothesis confirmed)
  F3: if the numerator is not decreasing on [log H, 76.47], the min is not at xT
      and the fixed point at xT is wrong.  -> PASS (decreasing, 201-pt check)
