#!/usr/bin/env bash
# Checker for track D claim: Mertens record at N = 10^11.
# Re-runs the segmented exact-integer sieve
# (tracks/d-search/mertens_segmented.py 100000000000 100000000) and asserts:
#  - checks C1-C7 all PASS (C6 = M(10^11) = -87856, OEIS A084237 a(11),
#    fetched 2026-08-23; C7 = M(10^k) k<=10 vs the machine-verified 1e10 run),
#  - the re-run reproduces the recorded run's (run3.txt) record line and
#    witness line EXACTLY (determinism),
#  - F5: max |M| >= 50286 (1e10 record, claim #24),
#  - F4: witness max |M|/sqrt(x) for x >= 100 < 1.0 (Mertens conjecture
#    alive in range; if >= 1.0 this checker fails loudly — bigger claim).
set -euo pipefail
cd "$(dirname "$0")/../.."
REC=run3.txt
[ -f "evidence/2026-08-23-mertens-1e11/$REC" ] || { echo "missing $REC"; exit 1; }
out=$(python3 tracks/d-search/mertens_segmented.py 100000000000 100000000 2>/dev/null)
echo "$out" | grep -E "C1|C2|C3|C4|C5|C6|C7|max |witness|M\(10|VERDICT"
echo "$out" | grep -q "C1 M(10) = -1 (expect -1): PASS"
echo "$out" | grep -q "C2 OEIS A002321 n<=10000: 10000 values, mismatches=0: PASS"
echo "$out" | grep -q "C3 sympy independent n<=10^5: mismatches=0: PASS"
echo "$out" | grep -qE "C4 OEIS A051402 envelope: checked=[0-9]+ n-values, mismatches=0: PASS"
echo "$out" | grep -q "C5 segmented mu == full-array mu n<=10^6: PASS"
echo "$out" | grep -q "C6 M(10^11) = -87856 (expect -87856, OEIS A084237): PASS"
echo "$out" | grep -q "C7 M(10^k) k<=10 vs verified 1e10 run: mismatches=0: PASS"
echo "$out" | grep -q "M(10^11) = -87856"
echo "$out" | grep -q "VERDICT: ALL CHECKS PASS"
rec=$(grep "^max |M(x)| for x <= 100000000000:" "evidence/2026-08-23-mertens-1e11/$REC")
wit=$(grep "^witness: max |M(x)|/sqrt(x) for x >= 100:" "evidence/2026-08-23-mertens-1e11/$REC")
[ -n "$rec" ] && [ -n "$wit" ] || { echo "record/witness line missing in $REC"; exit 1; }
echo "recorded: $rec"
echo "recorded: $wit"
echo "$out" | grep -qxF "$rec" || { echo "re-run record line differs from $REC"; exit 1; }
echo "$out" | grep -qxF "$wit" || { echo "re-run witness line differs from $REC"; exit 1; }
maxabs=$(echo "$rec" | sed -E 's/.*: ([0-9]+), first at x = [0-9]+, M = -?[0-9]+/\1/')
[ "$maxabs" -ge 50286 ] || { echo "F5 violated: maxabs=$maxabs < 50286"; exit 1; }
w=$(echo "$wit" | sed -E 's/.*for x >= 100: ([0-9.]+) at x = [0-9]+ \(M = -?[0-9]+\)/\1/')
python3 -c "import sys; sys.exit(0 if float('$w') < 1.0 else 1)" \
  || { echo "F4 FIRED: witness $w >= 1.0 (Mertens conjecture dead in range)"; exit 1; }
echo "CHECK PASS: Mertens record at 10^11 ($rec; witness $w < 1.0)"
