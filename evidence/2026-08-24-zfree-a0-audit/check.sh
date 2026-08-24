#!/usr/bin/env bash
# Re-verifies the A0-typo finding: table Lemma-1 row eta0/sigma0 match
# A0=(4.896)^-1 (not the printed (4.8596)^-1), and only (4.896)^-1 satisfies
# the final-line requirement A0 < A_final.
set -euo pipefail
cd "$(dirname "$0")"
out=$(python3 a0_check.py)
echo "$out"
# F1: printed (4.8596)^-1 row must FAIL the final-line requirement
echo "$out" | grep -q "printed L1 (4.8596)^-1     A0<A_final? False"
# F2: (4.896)^-1 row must PASS the final-line requirement
echo "$out" | grep -q "L1 headline  (4.896)^-1    A0<A_final? True"
# F3: table Lemma-1 eta0 must equal (4.896)^-1's eta0 to 5 digits (0.0071093)
echo "$out" | grep -q "L1 headline  (4.896)^-1    A0=0.204248366  eta0=0.0071093"
echo "CHECK PASS"
