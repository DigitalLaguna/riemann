#!/usr/bin/env bash
# Re-verifies the 138-relaxation: BTY Lemma 5's |z|>=138 requirement is NOT the
# true binding constraint; applying Lemma 4 with nu=r=L=(2sigma0-1)/eta0 (optimal,
# per 2D scan) gives A0_max = 0.324204954225 (constant 3.084468596), improving
# on claim #42's 4.866889911. All other constraints (#42/#44) hold at A0_max.
set -euo pipefail
cd "$(dirname "$0")"
out=$(python3 relax138_verify.py)
echo "$out"
# F1: new A0_max = 0.324204954225
echo "$out" | grep -q "NEW A0_max = 0.324204954225"
# F2: constant = 3.084468596
echo "$out" | grep -q "constant = 1/A0_max = 3.084468596"
# F3: all non-binding constraints hold
echo "$out" | grep -q "all non-binding constraints hold at A0_new? True"
# F4: old paper 138 wall constant 4.866889911 (sanity, from #42)
echo "$out" | grep -q "4.866889911"
# F5: relaxed Lemma5 is the binding constraint (g=1 at A0_new)
echo "$out" | grep -q "relaxed Lemma5 g(A0_new) = 1.0"
echo "CHECK PASS"
