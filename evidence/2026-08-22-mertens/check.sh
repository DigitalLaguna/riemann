#!/usr/bin/env bash
# Checker for claim #20 (track d, NUMERIC): Mertens record at N = 10^8.
# Re-runs the exact-integer sieve (tracks/d-search/mertens_extremal.py) and
# asserts the four cross-verification checks (C1-C4) and the recorded record
# values. Machine = direct evaluation of witnesses (exact integer arithmetic,
# cross-verified against OEIS A002321, independent sympy trial division, and
# the OEIS A051402 first-attainment envelope).
set -euo pipefail
cd "$(dirname "$0")/../.."
out=$(python3 tracks/d-search/mertens_extremal.py 2>&1)
echo "$out" | grep -E "C1|C2|C3|C4|max |M\(10|VERDICT"
echo "$out" | grep -q "C1 M(10) = -1 (expect -1): PASS"
echo "$out" | grep -q "C2 OEIS A002321 n<=10000: 10000 values, mismatches=0: PASS"
echo "$out" | grep -q "C3 sympy independent n<=10^5: mismatches=0: PASS"
echo "$out" | grep -q "C4 OEIS A051402 envelope: checked=3448 n-values, mismatches=0: PASS"
echo "$out" | grep -q "max |M(x)| for x <= 100000000: 3448, first at x = 76015339, M = -3448"
echo "$out" | grep -q "M(10^8) = 1928"
echo "$out" | grep -q "VERDICT: ALL CHECKS PASS"
echo "CHECK PASS: Mertens record at 10^8 reproduced (max |M| = 3448, first at x = 76015339)"
