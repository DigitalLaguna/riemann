#!/usr/bin/env bash
# Checker for claim #33 (track C): the 4.896 zero-free-region headline of
# bellotti-trudgian-yang-2026 Theorem 1 (zeta != 0 for sigma > 1 - 1/(4.896 log t),
# 3 <= t <= exp(76.47)) is justified by the paper's stated intermediates
# (1.02928 at t=exp(76.47); a=2919857/828465, kappa=433/859, w(0)=5.672787598).
# Re-runs the 50-dp Decimal derivation (tracks/c-constants/zfree-4896/final-bound.py)
# and asserts F1-F5 PASS + VERDICT + byte-identical regression vs recorded run.
set -euo pipefail
cd "$(dirname "$0")/../.."
EV="$(cd "$(dirname "$0")" && pwd)"
OUT="$(python3 tracks/c-constants/zfree-4896/final-bound.py)"
for f in F1 F2 F3 F4 F5; do
  printf '%s\n' "$OUT" | grep -q "^$f .* -> PASS" || { echo "CHECK FAIL: $f not PASS"; exit 1; }
done
printf '%s\n' "$OUT" | grep -q "^VERDICT: ALL CHECKS PASS$" || { echo "CHECK FAIL: verdict"; exit 1; }
printf '%s\n' "$OUT" | diff - "$EV/machine-run-final-bound.txt" >/dev/null \
  || { echo "CHECK FAIL: rerun differs from recorded run"; exit 1; }
echo "CHECK PASS"
