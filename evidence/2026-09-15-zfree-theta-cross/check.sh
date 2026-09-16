#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Checker for #51 (rigorous A0_max >= 0.39211324739496) and #50 (>= 0.392113247328).
# Re-bisects the crossing (30 dps, 30 iters) and verifies the H>=0 endpoint
# (hi, A0_g(hi)) at 50/100 dps + all 7 constraints. Exits 0 iff all hold.
python3 check_theta_cross_fine.py
