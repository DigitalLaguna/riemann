#!/usr/bin/env bash
# Checker for track D claim: Mertens record at N = 10^12.
# Re-runs the segmented exact-integer sieve
# (tracks/d-search/mertens_segmented.py 1000000000000 100000000) and asserts:
#  - checks C1-C7 all PASS (C6 = M(10^12) = 62366, OEIS A084237 a(12),
#    fetched 2026-08-23; C7 = M(10^k) k<12 vs the machine-verified 1e11 run),
#  - the re-run reproduces the recorded run's (run.txt) record line and
#    witness line EXACTLY (determinism),
#  - F4: max |M| >= 94909 (1e11 record, claim #27),
#  - F3: witness max |M|/sqrt(x) for x >= 100 < 1.0 (Mertens conjecture
#    alive in range; if >= 1.0 this checker fails loudly — bigger claim),
#  - F5: witness < 0.585768 (Kuznetsov 2011 global extreme, arXiv:1108.0135),
#  - M(10^12) = 62366 present in the fetched OEIS A084237 file.
set -euo pipefail
cd "$(dirname "$0")/../.."
REC=run.txt
[ -f "evidence/2026-08-24-mertens-1e12/$REC" ] || { echo "missing $REC"; exit 1; }
out=$(python3 tracks/d-search/mertens_segmented.py 1000000000000 100000000 2>/dev/null)
echo "$out" | grep -E "C1|C2|C3|C4|C5|C6|C7|max |witness|M\(10|VERDICT"
echo "$out" | grep -q "C1 M(10) = -1 (expect -1): PASS"
echo "$out" | grep -q "C2 OEIS A002321 n<=10000: 10000 values, mismatches=0: PASS"
echo "$out" | grep -q "C3 sympy independent n<=10^5: mismatches=0: PASS"
echo "$out" | grep -qE "C4 OEIS A051402 envelope: checked=[0-9]+ n-values, mismatches=0: PASS"
echo "$out" | grep -q "C5 segmented mu == full-array mu n<=10^6: PASS"
echo "$out" | grep -q "C6 M(10^12) = 62366 (expect 62366, OEIS A084237): PASS"
echo "$out" | grep -q "C7 M(10^k) k<12 vs verified runs/OEIS: mismatches=0: PASS"
echo "$out" | grep -q "M(10^12) = 62366"
echo "$out" | grep -q "VERDICT: ALL CHECKS PASS"
rec=$(grep "^max |M(x)| for x <= 1000000000000:" "evidence/2026-08-24-mertens-1e12/$REC")
wit=$(grep "^witness: max |M(x)|/sqrt(x) for x >= 100:" "evidence/2026-08-24-mertens-1e12/$REC")
[ -n "$rec" ] && [ -n "$wit" ] || { echo "record/witness line missing in $REC"; exit 1; }
echo "recorded: $rec"
echo "recorded: $wit"
echo "$out" | grep -qxF "$rec" || { echo "re-run record line differs from $REC"; exit 1; }
echo "$out" | grep -qxF "$wit" || { echo "re-run witness line differs from $REC"; exit 1; }
maxabs=$(echo "$rec" | sed -E 's/.*: ([0-9]+), first at x = [0-9]+, M = -?[0-9]+/\1/')
[ "$maxabs" -ge 94909 ] || { echo "F4 violated: maxabs=$maxabs < 94909 (1e11 record)"; exit 1; }
w=$(echo "$wit" | sed -E 's/.*for x >= 100: ([0-9.]+) at x = [0-9]+ \(M = -?[0-9]+\)/\1/')
python3 -c "import sys; sys.exit(0 if float('$w') < 1.0 else 1)" \
  || { echo "F3 FIRED: witness $w >= 1.0 (Mertens conjecture dead in range)"; exit 1; }
python3 -c "import sys; sys.exit(0 if float('$w') < 0.585768 else 1)" \
  || { echo "F5 FIRED: witness $w >= 0.585768 (exceeds Kuznetsov global extreme)"; exit 1; }
grep -q "62366" evidence/2026-08-23-mertens-1e9/oeis-a084237-m10n.txt \
  || { echo "OEIS A084237 file missing 62366"; exit 1; }
echo "CHECK PASS: Mertens record at 10^12 ($rec; witness $w < 1.0)"
