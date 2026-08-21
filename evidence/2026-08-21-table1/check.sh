#!/usr/bin/env bash
# Checker for claim #8: re-runs the Table 1 machine check (exact + integer arithmetic
# on the fetched paper text; no floating-point ball needed — all comparisons are
# against published decimal values with explicit rounding tolerance).
set -euo pipefail
EV="$(cd "$(dirname "$0")" && pwd)"
cd /home/niklas/riemann
python3 "$EV/table1_check.py"
