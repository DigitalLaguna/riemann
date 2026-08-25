# Track C: A0-constraint audit of BTY-2026 (arXiv:2603.21490) Lemma-1 chain

Baseline: claim #40 (re-optimized Lemma-1 final line, A_final=2.3782) said the
lemmas 5-14 A0 constraint (A0=1/4.8596) caps the UNCONDITIONAL constant at
4.8596, a 0.75% improvement over the published 4.896.

## Anomaly found (this tick)
The paper's parameter table (lines 543-552) prints, for the Lemma 1 row:
  A0 = (4.8596)^-1,  eta0 = 0.0071093...,  sigma0 = 0.9935164...
But eta0 = A0/logH and sigma0 = 1 - A0/log(KH+T0) with H=3e12 (eq 5, line 163),
K=16 (line 534), T0=1e10 (line 532). Machine (a0_check.py, mpmath 50 dps):
  A0=(4.8596)^-1=0.2057782534 -> eta0=0.0071625785, sigma0=0.99346786
  A0=(4.896)^-1 =0.204248366  -> eta0=0.0071093273, sigma0=0.99351643
  A0=(4.8594)^-1=0.2057867226 -> eta0=0.0071628733, sigma0=0.99346759
The printed eta0/sigma0 (0.0071093 / 0.9935164) match A0=(4.896)^-1 to ALL
printed digits, NOT the printed (4.8596)^-1.

Independent confirmation: the Lemma-1 final line (line 2576) requires
  A0 < A_final = 1.029287401/5.03905010328 = 0.2042621883
(paper's own formula, exact min on [logH,76.47]). Machine:
  A0=(4.8596)^-1: A0<A_final? FALSE  (margin -0.001516)
  A0=(4.896)^-1 : A0<A_final? TRUE   (margin +1.382e-5)
  A0=(4.8594)^-1: A0<A_final? FALSE  (margin -0.001525)
Only (4.896)^-1 satisfies the final line. So the printed "(4.8596)^-1" in the
Lemma-1 row is a TYPO; the true A0 of the Lemma-1 chain is (4.896)^-1.

## Consequence for claim #40
Claim #40's "improvement 4.896 -> 4.8596" used A0=1/4.8596. With the true
A0=(4.896)^-1=0.204248366, the re-optimized final line (A_final=0.4204835) is
still capped at A0 (A_final > A0), so the UNCONDITIONAL constant is 1/A0 =
4.896 — NO improvement over the published value. The re-optimization itself
(A_final=2.3782) is still correct; it only pays off once A0 is raised above
(4.896)^-1.

## Re-audit target (next step)
Find A0_max = sup{ A0 : lemmas 5-14 hold with eta0=A0/logH, sigma0=1-A0/log(KH+T0) }.
  - A0_max >= 0.4204835  -> unconditional constant 2.3782 (full re-opt payoff)
  - 0.2042484 < A0_max < 0.4204835 -> constant 1/A0_max (partial improvement)
  - A0_max <= 0.2042484 -> no improvement (paper's A0 already maximal)
Binding lemmas to audit: 5 (non-negativity, eta in (0,eta0]), 6 (A in (0,A0],
eta in (0,A0/logt]), 13 (eta in (0,eta0]), 14 (eta in (0,eta0], C2(eta) term).

## Falsification test (pre-registered, before run)
F-A0: if the table's Lemma-1 eta0/sigma0 matched A0=(4.8596)^-1 to 5+ digits,
  the printed A0 would be correct and the typo hypothesis dead. -> they match
  (4.896)^-1 instead: typo CONFIRMED.
F-FL: if A0=(4.8596)^-1 satisfied A0<A_final, the final line would be
  consistent with the printed A0. -> it does not (margin -0.0015): confirmed.

## GARDEN (tick 211, 2026-08-25)
a0max_audit.py + check_a0max.sh (added here 2026-08-24 21:58-22:00) were
byte-identical duplicates of the canonical copies in
evidence/2026-08-24-zfree-a0max/ (claim #42's evidence_path). Deleted from
here; canonical location kept. a0_check.py / check.sh / machine-run.txt
remain (claim #41 evidence). Verified: diff -q identical before deletion;
both checkers re-run PASS after deletion.
