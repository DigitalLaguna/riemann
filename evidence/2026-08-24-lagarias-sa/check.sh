#!/usr/bin/env bash
# Re-verifies the claim: Lagarias inequality sigma(n) <= H_n + e^{H_n} log H_n
# holds for all 55 superabundant numbers n <= 1e10 listed in the OEIS A004394
# b-file (a004394.txt, fetched tick 178): 100-digit margin > 1e-80 for every
# n >= 2 (min margin at n=2, re-evaluated at 150 dps), and sigma(n) exact
# trial-division == sympy.divisor_sigma for all 55 entries.
set -euo pipefail
cd "$(dirname "$0")/../.."
out=$(python3 tracks/e-rh/lagarias_sa_check.py)
echo "$out"
echo "$out" | grep -q "VERDICT F3: NO WITNESS among 55 SA n <= 10000000000"
echo "$out" | grep -q "VERDICT F4: PASS"
echo "CHECK PASS"
