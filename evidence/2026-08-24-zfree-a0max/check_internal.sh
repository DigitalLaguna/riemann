#!/usr/bin/env bash
# Re-verifies the A0_max INTERNAL-constraint audit (Lemma 5 internals + Lemma 6 A-range).
# Confirms the PARTIAL win 4.866889911 (claim #42) is not shrunk by any internal bound.
set -euo pipefail
cd "$(dirname "$0")"
out=$(python3 a0max_internal_audit.py)
echo "$out"
# F1: w(0) formula reproduces the paper's 5.672787598
echo "$out" | grep -q "w(0) = 5.672787599"
# F2: C(138,138) internal constraint holds at A0_max
echo "$out" | grep -q "at A0_max: LHS = 0.001103325869  RHS = 0.002799393866  holds? True"
# F3: C(138,138) binds ABOVE A0_max (does not shrink the win)
echo "$out" | grep -q "binds at A0 = 0.326015468165"
# F4: B(y) > 0 for all y (no real p-roots with u>=0)
echo "$out" | grep -q "B(y)>0 for all y? True"
# F5: eq-22 W0-term holds at A0_max
echo "$out" | grep -q "at A0_max: LHS = 0.002167743713  RHS = 5.7e+10  holds? True"
# F6: Lemma 6 A-range holds (A0_max > 1/6)
echo "$out" | grep -q "> 1/6 = 0.16666666666666666?  True"
# F7: verdict CONFIRMED, constant 4.866889911
echo "$out" | grep -q "CONFIRMED: Lemma 5 main still binds"
echo "$out" | grep -q "PARTIAL win stands: unconditional constant = 4.866889911"
echo "CHECK PASS (internal)"
