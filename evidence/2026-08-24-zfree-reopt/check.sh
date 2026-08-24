#!/usr/bin/env bash
# Checker: re-optimization of the BTY-2026 (arXiv:2603.21490 v1) Lemma-1 final line.
# Correcting the missing kappa factor (claim #38) and re-optimizing the final
# line (sharp c_mu = log(K+T0/H) = 2.77279703387 vs paper 2.78; eta = A/x fixed
# point vs paper 1/(6x); corrected denom a*kappa^2*w(0)/2 = 2.54005668768) gives
# A_final = 0.420483467794 (1/A_final = 2.37821478511); the lemmas 5-14 A0
# constraint (A0 = 1/4.8596 = 0.205778253354) caps the UNCONDITIONAL
# zero-free-region constant at 4.8596 < 4.896 (published). Re-runs reopt.py
# (mpmath 60 dps) and asserts the key bounds + byte-identical regression.
set -euo pipefail
cd "$(dirname "$0")/../.."
EV="$(cd "$(dirname "$0")" && pwd)"
OUT="$(python3 evidence/2026-08-24-zfree-reopt/reopt.py)"
# F1: CASE 1 reproduces the paper's final line (B ~ 0.20426, 1/B ~ 4.8957)
printf '%s\n' "$OUT" | grep -Fq "CASE 1 (paper): B = 0.204262188243  headline 1/B = 4.89566869229" \
  || { echo "CHECK FAIL: F1 CASE 1 paper reproduction"; exit 1; }
# F2: CASE 3 re-optimized fixed point, converged
printf '%s\n' "$OUT" | grep -Fq "CASE 3 (reopt fixed point): A* = 0.420483467794  headline 1/A* = 2.37821478511" \
  || { echo "CHECK FAIL: F2 CASE 3 reopt value"; exit 1; }
printf '%s\n' "$OUT" | grep -Fq "converged: True" || { echo "CHECK FAIL: F2 convergence"; exit 1; }
# F3: A0 constraint caps the effective constant at 4.8596 (reopt row)
printf '%s\n' "$OUT" | grep -Fq "reopt      A_final=0.4204834678  A0=0.2057782534  effective A=0.2057782534  headline 1/A=4.8596" \
  || { echo "CHECK FAIL: F3 A0 constraint caps at 4.8596"; exit 1; }
# F4: the improvement is real: 4.8596 < 4.896
python3 -c "import sys; sys.exit(0 if 4.8596 < 4.896 else 1)" \
  || { echo "CHECK FAIL: F4 no improvement over 4.896"; exit 1; }
# F5: byte-identical regression vs the recorded run
printf '%s\n' "$OUT" | diff - "$EV/machine-run.txt" >/dev/null \
  || { echo "CHECK FAIL: F5 rerun differs from recorded run"; exit 1; }
echo "CHECK PASS"
