#!/usr/bin/env bash
# Checker for the A0_max INTERNAL-constraint audit (claim: Lemma 5 proof internals
# + Lemma 6 A-range all hold at A0_max = 0.205470026688, claim #42).
# Re-runs the canonical audit script (single copy, in zfree-a0max) and asserts:
#  - w(0) reproduces the paper's 5.672787598,
#  - eta0^2*C(138,138) < eps0*(2*sigma0-1)*w(0) at A0_max (binds at 0.3260 > A0_max),
#  - B(y) > 0 for all y (p has no real root with u >= 0),
#  - eq-22 W0-term eta0^2*(C(-1,T0/eta0)+C(0,T0/eta0)) < 5.7*T0 at A0_max,
#  - Lemma 6 A-range: A0_max > 1/6,
#  - VERDICT: PARTIAL win constant 4.866889911 stands.
set -euo pipefail
cd "$(dirname "$0")/../.."
out=$(python3 evidence/2026-08-24-zfree-a0max/a0max_internal_audit.py)
echo "$out"
echo "$out" | grep -q "w(0) = 5.672787599"
echo "$out" | grep -q "at A0_max: LHS = 0.001103325869  RHS = 0.002799393866  holds? True"
echo "$out" | grep -q "binds at A0 = 0.326015468165"
echo "$out" | grep -q "B(y)>0 for all y? True"
echo "$out" | grep -q "at A0_max: LHS = 0.002167743713  RHS = 5.7e+10  holds? True"
echo "$out" | grep -q "> 1/6 = 0.16666666666666666?  True"
echo "$out" | grep -q "CONFIRMED: Lemma 5 main still binds"
echo "$out" | grep -q "PARTIAL win stands: unconditional constant = 4.866889911"
echo "CHECK PASS (a0max internal)"
