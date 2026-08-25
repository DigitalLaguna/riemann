#!/usr/bin/env bash
# Checker for claim #47 (m=0-term theta constraint). Re-runs verify_m0term.py
# and asserts the key machine-verified values.
set -e
cd "$(dirname "$0")"
out=$(python3 verify_m0term.py 2>&1)
echo "$out"
echo "$out" | grep -q "x_max = 1.31432746286474" || { echo "CHECK FAIL: x_max"; exit 1; }
echo "$out" | grep -q "theta_min = 0.98017549497920" || { echo "CHECK FAIL: theta_min"; exit 1; }
echo "$out" | grep -q "V2 bound at theta_min.*HOLDS" || { echo "CHECK FAIL: bound at theta_min"; exit 1; }
echo "$out" | grep -q "V2 bound at theta\* #46.*FAILS" || { echo "CHECK FAIL: bound at theta*"; exit 1; }
echo "$out" | grep -q "A0_max(theta_min) = 0.350566297741" || { echo "CHECK FAIL: A0_max"; exit 1; }
echo "$out" | grep -q "V3 all 7 constraints hold.*True" || { echo "CHECK FAIL: 7 constraints"; exit 1; }
echo "$out" | grep -q "V4 max at left endpoint theta_min? True" || { echo "CHECK FAIL: scan endpoint"; exit 1; }
echo "$out" | grep -q "V5 bracket.*True" || { echo "CHECK FAIL: bracket"; exit 1; }
echo "$out" | grep -q "OVERALL: ALL PASS" || { echo "CHECK FAIL: overall"; exit 1; }
echo "CHECK PASS"
