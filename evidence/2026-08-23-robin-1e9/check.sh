#!/usr/bin/env bash
# Machine check for claim: Track D Robin-criterion SA-scan extended to 1e9.
# Re-runs the experiment and verifies the key machine-verified values.
set -euo pipefail
cd "$(dirname "$0")/../.."
OUT=$(python3 tracks/d-search/robin_sa_1e9.py 2>&1)
RC=$?
echo "$OUT"
echo "---- check ----"
fail=0
[ "$RC" -eq 0 ] || { echo "FAIL: script exit $RC"; fail=1; }
echo "$OUT" | grep -q "VERDICT: ALL CHECKS PASS" || { echo "FAIL: no ALL CHECKS PASS"; fail=1; }
echo "$OUT" | grep -q "F1 sigma(new SA in (1e8,1e9]) == sympy divisor_sigma: checked=6 mismatches=0: PASS" || { echo "FAIL: F1"; fail=1; }
echo "$OUT" | grep -q "F2 R(10080) = 0.985818611972329" || { echo "FAIL: F2 regression"; fail=1; }
echo "$OUT" | grep -q "F3 witness R(n)>=1 among SA in \[5041,1e9\]: hits=0" || { echo "FAIL: F3 witness"; fail=1; }
echo "$OUT" | grep -q "max R(n) over SA in \[5041,1e9\] = 0.985818611972329 at n = 10080" || { echo "FAIL: near-miss value"; fail=1; }
if [ "$fail" -eq 0 ]; then echo "CHECK PASS: Robin SA-scan to 1e9 (no witness <=1e9; near-miss max R=0.985818611972329 at n=10080)"; else echo "CHECK FAILURE"; fi
exit $fail
