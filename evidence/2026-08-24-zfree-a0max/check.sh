#!/usr/bin/env bash
# Re-verifies the A0_max audit: Lemma 5's constraint (2*sigma0-1)/eta0 > 138
# binds at A0 = 0.205470026688, giving a partial win 4.896 -> 4.8669.
set -euo pipefail
cd "$(dirname "$0")"
out=$(python3 a0max_audit.py)
echo "$out"
# F1: Lemma 5 constraint binds at A0 = 0.205470026688
echo "$out" | grep -q "A0 = 0.205470026688"
# F2: Lemma 5 does NOT hold at the target A0 = 0.4204835
echo "$out" | grep -q "Lemma 5 holds? False"
# F3: Lemma 14 x1 holds at the target A0
echo "$out" | grep -q "Lemma 14 x1 holds? True"
# F4: Lemma 13 holds at the target A0
echo "$out" | grep -q "Lemma 13 holds? True"
# F5: verdict is PARTIAL win with constant 4.866889911
echo "$out" | grep -q "PARTIAL win: constant = 4.866889911"
echo "CHECK PASS"
