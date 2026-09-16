#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Checker for the pinned A0_max claim (supersedes #51).
# Re-bisects the crossing (30 dps, 46 iters, width 6.3e-16) and verifies the
# H>=0 endpoint (hi, A0_g(hi)) at 50/100 dps + all 7 constraints. Exits 0 iff all hold.
python3 check_theta_cross_pin.py
