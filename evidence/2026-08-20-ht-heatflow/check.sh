#!/usr/bin/env bash
# Claim: track B heat flow H_t(35+10i), t in {0,1,100,1000}, rigorous Arb.
# Re-runs tracks/b-dbn/ht_quadrature.py and asserts:
#  - GL moment test passes (nodes/weights verified against exact acb targets)
#  - F1: t=0 quadrature vs claim #3 closed form >= 25 digits
#  - F2: each t>0 vs independent 80-digit mpmath quadrature >= 20 digits
#  - F3: relative ball radius < 1e-25 (explicit Arb error bound)
#  - F4: values finite (not NaN)
set -euo pipefail
cd "$(dirname "$0")/../.."
out=$(python3 tracks/b-dbn/ht_quadrature.py)
echo "$out" | grep -q "moment test n=32: True"
echo "$out" | grep -q "F1: YES"
[ "$(echo "$out" | grep -c 'F2: YES   F3: YES')" = "3" ]
[ "$(echo "$out" | grep -c 'F4 finite and heat-scale (not NaN/O(1)): True')" = "3" ]
echo "CHECK OK"
