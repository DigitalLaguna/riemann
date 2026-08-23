#!/usr/bin/env bash
# Machine check for claim: Track D Robin-criterion FULL scan over [1e8,1e9] (all n).
# Re-runs the experiment and verifies the key machine-verified values.
set -euo pipefail
cd "$(dirname "$0")/../.."
OUT=$(python3 tracks/d-search/robin_full_scan.py 2>&1)
RC=$?
echo "$OUT"
echo "---- check ----"
fail=0
[ "$RC" -eq 0 ] || { echo "FAIL: script exit $RC"; fail=1; }
echo "$OUT" | grep -q "VERDICT: ALL CHECKS PASS" || { echo "FAIL: no ALL CHECKS PASS"; fail=1; }
echo "$OUT" | grep -q "FULL SCAN \[100000000,1000000001): max R = 0.9681521049018093 at n = 367567200 (sigma=1889879040)" || { echo "FAIL: max R value"; fail=1; }
echo "$OUT" | grep -q "F1 cross-check: checked=33 mismatches=0: PASS" || { echo "FAIL: F1"; fail=1; }
echo "$OUT" | grep -q "F2 witness R(n)>=1 in \[100000000,1000000001): none (max R < 1)" || { echo "FAIL: F2"; fail=1; }
echo "$OUT" | grep -q "F3a consistency: full-scan max R 0.9681521049018093 >= SA max (50-digit) 0.9681521049018093: PASS" || { echo "FAIL: F3a"; fail=1; }
echo "$OUT" | grep -q "F3b regression: 12-sig-digit display of full-scan max == claim #23 display 0.968152104902: PASS" || { echo "FAIL: F3b"; fail=1; }
if [ "$fail" -eq 0 ]; then echo "CHECK PASS: Robin full scan [1e8,1e9] (max R=0.9681521049018093 at n=367567200, CA; no witness R>=1)"; else echo "CHECK FAILURE"; fi
exit $fail
