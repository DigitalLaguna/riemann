#!/usr/bin/env bash
# Checker for track D claim: Mertens record at N = 10^9.
# Re-runs the exact-integer sieve (tracks/d-search/mertens_extremal.py 1000000000)
# and asserts the four cross-verification checks (C1-C4) plus the recorded record
# values and the literature cross-check M(10^9) = -222 (OEIS A084237 a(9),
# fetched 2026-08-23, see oeis-a084237-m10n.txt).
set -euo pipefail
cd "$(dirname "$0")/../.."
out=$(python3 tracks/d-search/mertens_extremal.py 1000000000 2>&1)
echo "$out" | grep -E "C1|C2|C3|C4|max |M\(10|VERDICT"
echo "$out" | grep -q "C1 M(10) = -1 (expect -1): PASS"
echo "$out" | grep -q "C2 OEIS A002321 n<=10000: 10000 values, mismatches=0: PASS"
echo "$out" | grep -q "C3 sympy independent n<=10^5: mismatches=0: PASS"
echo "$out" | grep -q "C4 OEIS A051402 envelope: checked=10000 n-values, mismatches=0: PASS"
echo "$out" | grep -q "max |M(x)| for x <= 1000000000: 10246, first at x = 903087703, M = 10246"
echo "$out" | grep -q "M(10^9) = -222"
echo "$out" | grep -q "VERDICT: ALL CHECKS PASS"
echo "CHECK PASS: Mertens record at 10^9 (max |M| = 10246, first at x = 903087703; M(10^9) = -222 = OEIS A084237 a(9))"
