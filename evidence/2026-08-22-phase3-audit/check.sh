#!/usr/bin/env bash
# Checker for the Phase-3 dominant-error-term audit (tick 88).
# Re-runs the exact-rational per-term budget and asserts the pre-registered
# hit criterion: one term >= 2x the sum of the others.
set -euo pipefail
cd "$(dirname "$0")"
python3 audit.py > machine-run.txt 2>&1
# assert the key machine outputs
grep -q "bound         = 3999993289/20000000000 = 0.19999966445" machine-run.txt
grep -q "ratio t0 / (y0^2/2)        = 13.2860x" machine-run.txt
grep -q "HIT = True" machine-run.txt
grep -q "dominant / sum-of-others = 13.2860x  (need >= 2x)" machine-run.txt
grep -q "BINDING COMPONENT: ASYMPTOTICS" machine-run.txt
echo "CHECK PASS: per-term budget machine-computed; ASYMPTOTICS binding (13.286x >= 2x)"
