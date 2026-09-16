# Downstream propagation of the pinned A0_max (track C, BTY-2026)

Combines #40 (re-optimized Lemma-1 final line, A_final = 0.420483467794) and
#54 (pinned A0_max = 0.392113247395366294) to give the effective
zero-free-region constant for the ANT network.

Logic (evidence/2026-08-24-zfree-reopt/README.md, "A0 CONSTRAINT"):
  lemmas 5-14 are stated with eta <= A0/log t, so the region constant must
  satisfy A <= A0. Effective constant = min(A_final, A0).
  A_final = re-optimized Lemma-1 lower bound on eta*log t (#40).
  A0      = max A0 such that lemmas 5-14 hold (#54, pinned).

Machine (downstream.py, mpmath 50 dps) -> machine-run.txt:
  A_final > A0_max  =>  A0_max binds
  effective = A0_max = 0.392113247395366294
  headline  = 1/A0_max = 2.55028364035787
  improvement over paper (A0_max / (1/4.8596)) = 1.90551x

This is the constant to report to the ANT network (owner action, handoff (d)).
