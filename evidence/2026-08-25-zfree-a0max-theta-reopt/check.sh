#!/usr/bin/env bash
# Re-verifies the theta reopt for the A0_max objective: the paper's fixed
# theta=1.1338 (chosen for the 4.896 constant) is NOT optimal for A0_max.
# Re-optimizing theta gives A0_max = 0.396708119308 at theta* = 0.057151961
# (constant 2.520744979), up from 0.324204954225 (theta=1.1338, claim #45).
# All 7 constraints of the #44/#45 set hold at (A0_max*, theta*). PARTIAL win:
# does not reach the full reopt target 0.420483467794 (constant 2.378214785, #40).
set -euo pipefail
cd "$(dirname "$0")"
out=$(python3 relax138_theta_verify.py)
echo "$out"
# F1: reproduces claim #45 at theta=1.1338
echo "$out" | grep -q "F1: A0_max(1.1338)=0.324204954225"
# F2: all 7 constraints hold at (A0_max*, theta*)
echo "$out" | grep -q "F2 all 7 constraints hold at (A0\*,theta\*): True"
# F3: partial win 0.3242 < A0_max* < 0.4205
echo "$out" | grep -q "F3 0.3242 < A0_max\* < 0.4205 (partial win): True"
# key values
echo "$out" | grep -q "A0_max\* = 0.396708119308"
echo "$out" | grep -q "1/A0_max\* = 2.520744979"
echo "$out" | grep -q "theta\* = 0.057151961"
echo "CHECK PASS"
