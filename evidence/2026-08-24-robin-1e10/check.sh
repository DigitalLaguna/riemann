#!/usr/bin/env bash
# Machine check for claim: Track D Robin-criterion SA-scan extended to 1e10.
# Re-runs the experiment and verifies the key machine-verified values.
set -euo pipefail
cd "$(dirname "$0")/../.."
OUT=$(python3 tracks/d-search/robin_sa_1e10.py 2>&1)
RC=$?
echo "$OUT"
echo "---- check ----"
fail=0
[ "$RC" -eq 0 ] || { echo "FAIL: script exit $RC"; fail=1; }
echo "$OUT" | grep -q "VERDICT: ALL CHECKS PASS" || { echo "FAIL: no ALL CHECKS PASS"; fail=1; }
echo "$OUT" | grep -q "F1 sigma(SA in \[1e9,1e10\]) == sympy divisor_sigma: checked=7 mismatches=0: PASS" || { echo "FAIL: F1"; fail=1; }
echo "$OUT" | grep -q "F2 regression (1e8,1e9\] SA max: n=367567200 display=0.968152104902" || { echo "FAIL: F2 regression"; fail=1; }
echo "$OUT" | grep -q "F3 witness R(n)>=1 among SA in \[1e9,1e10\]: hits=0" || { echo "FAIL: F3 witness"; fail=1; }
echo "$OUT" | grep -q "max R = 0.9736697983827134 at n = 6983776800" || { echo "FAIL: near-miss value"; fail=1; }
if [ "$fail" -eq 0 ]; then echo "CHECK PASS: Robin SA-scan to 1e10 (no witness in [1e9,1e10]; near-miss max R=0.9736697983827134 at n=6983776800)"; else echo "CHECK FAILURE"; fi
exit $fail
