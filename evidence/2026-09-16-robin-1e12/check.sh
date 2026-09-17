#!/usr/bin/env bash
# Checker for the Robin-criterion SA-scan over (1e11,1e12] (robin_sa_1e12.py,
# run tick 243, output sa-scan.txt). Re-runs the scan fresh (machine
# verification: exact-integer sigma via trial division cross-checked against
# sympy divisor_sigma; R(n) at 60 dps mpmath) and asserts:
#   F1  sigma cross-check 5/5 PASS
#   F2  regression (1e10,1e11] SA max 0.97201588698 at n=13967553600 (claim #43)
#   F3  no witness R(n)>=1 among SA in (1e11,1e12]
#   F3b 12-sig-digit SA max display 0.975505922736
#   VERDICT ALL CHECKS PASS
#   consistency: fresh run output == stored sa-scan.txt
set -u
cd "$(dirname "$0")/../.."
OUT=evidence/2026-09-16-robin-1e12/sa-scan-recheck.txt
fail=0
python3 tracks/d-search/robin_sa_1e12.py > "$OUT" 2>&1 || { echo "CHECK FAIL: re-run rc=$?"; exit 1; }
grep -q "F1 sigma(SA in (1e11,1e12]) == sympy divisor_sigma: checked=5 mismatches=0: PASS" "$OUT" || { echo "CHECK FAIL: F1"; fail=1; }
grep -q "F2 regression (1e10,1e11] SA max: n=13967553600 display=0.97201588698.*: PASS" "$OUT" || { echo "CHECK FAIL: F2"; fail=1; }
grep -q "F3 witness R(n)>=1 among SA in (1e11,1e12]: hits=0: PASS (no RH witness in (1e11,1e12])" "$OUT" || { echo "CHECK FAIL: F3 (witness HIT => RH FALSE)"; fail=1; }
grep -q "SA near-miss (1e11,1e12]: max R = 0.9755059227362326 at n = 160626866400 (sigma=907141939200)" "$OUT" || { echo "CHECK FAIL: near-miss value"; fail=1; }
grep -q "F3b reference for full scan: 12-sig-digit display = 0.975505922736" "$OUT" || { echo "CHECK FAIL: F3b"; fail=1; }
grep -q "VERDICT: ALL CHECKS PASS" "$OUT" || { echo "CHECK FAIL: verdict"; fail=1; }
if ! diff -q "$OUT" evidence/2026-09-16-robin-1e12/sa-scan.txt >/dev/null; then echo "CHECK FAIL: fresh run != stored sa-scan.txt"; fail=1; fi
if [ "$fail" -eq 0 ]; then echo "CHECK PASS: Robin SA-scan (1e11,1e12] re-verified"; else echo "CHECK FAIL"; fi
exit "$fail"
