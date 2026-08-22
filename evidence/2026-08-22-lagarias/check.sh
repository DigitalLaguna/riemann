#!/usr/bin/env bash
# Checker for claim #10 (track e, NUMERIC): Lagarias inequality holds for all
# n in [1, 10^6]. Re-runs the exact computation and asserts the machine verdict
# and the minimum margin (reproducibility: two independent runs agreed to 50 digits).
set -euo pipefail
cd "$(dirname "$0")/../.."
out=$(python3 tracks/e-rh/lagarias_check.py 1000000 2>&1)
echo "$out" | grep -E "sieve|scan|min margin|VERDICT"
echo "$out" | grep -q "VERDICT: NO COUNTEREXAMPLE in \[1,1000000\]"
echo "$out" | grep -q "min margin (n>=2): 0.3171685434118021783180761906577313314269920015416883884949297863249837122715354412219748081124551881"
echo "CHECK PASS: Lagarias inequality holds for all 1 <= n <= 10^6 (min margin at n=2 reproduced)"
