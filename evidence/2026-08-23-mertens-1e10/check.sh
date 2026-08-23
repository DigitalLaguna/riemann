#!/usr/bin/env bash
# Checker for track D claim: Mertens record at N = 10^10.
# Re-runs the exact-integer sieve (tracks/d-search/mertens_extremal.py 10000000000)
# and asserts the five cross-verification checks (C1-C5) plus the recorded record
# values and the literature cross-checks M(10^10) = -33722 (OEIS A084237 a(10))
# and M(10^9) = -222 (A084237 a(9)); fetched file
# evidence/2026-08-23-mertens-1e9/oeis-a084237-m10n.txt (2026-08-23).
set -euo pipefail
cd "$(dirname "$0")/../.."
out=$(python3 tracks/d-search/mertens_extremal.py 10000000000 2>&1)
echo "$out" | grep -E "C1|C2|C3|C4|C5|max |M\(10|VERDICT"
echo "$out" | grep -q "C1 M(10) = -1 (expect -1): PASS"
echo "$out" | grep -q "C2 OEIS A002321 n<=10000: 10000 values, mismatches=0: PASS"
echo "$out" | grep -q "C3 sympy independent n<=10^5: mismatches=0: PASS"
echo "$out" | grep -q "C4 OEIS A051402 envelope: checked=10000 n-values, mismatches=0: PASS"
echo "$out" | grep -q "C5 large-prime batching: 220098288 primes p>5000000000 flipped 1->-1: PASS"
echo "$out" | grep -q "max |M(x)| for x <= 10000000000: 50286, first at x = 7766842813, M = 50286"
echo "$out" | grep -q "M(10^9) = -222"
echo "$out" | grep -q "M(10^10) = -33722"
echo "$out" | grep -q "VERDICT: ALL CHECKS PASS"
echo "CHECK PASS: Mertens record at 10^10 (max |M| = 50286, first at x = 7766842813; M(10^10) = -33722 = OEIS A084237 a(10))"
