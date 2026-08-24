#!/usr/bin/env bash
# Checker for the full Robin scan [1e9,1e10) (robin_full_scan.py, launched
# tick 169 as robin-full-1e10.service). The run is self-checking (F1 sieve vs
# sympy, F2 witness, F3a/F3b consistency); this checker verifies the run
# completed and all self-checks passed.
set -u
RUN=evidence/2026-08-24-robin-full-1e10/run.txt
fail=0
grep -q "range \[1000000000,10000000001)  subseg width 100000000" "$RUN" || { echo "CHECK FAIL: missing range header"; fail=1; }
grep -q "F1 cross-check: checked=[0-9]* mismatches=0: PASS" "$RUN" || { echo "CHECK FAIL: F1"; fail=1; }
grep -q "F2 witness R(n)>=1 in \[1000000000,10000000001): none" "$RUN" || { echo "CHECK FAIL: F2 (witness HIT => RH FALSE)"; fail=1; }
grep -q "F3a consistency: full-scan max R .* >= SA max (50-digit) .*: PASS" "$RUN" || { echo "CHECK FAIL: F3a"; fail=1; }
grep -q "F3b regression: 12-sig-digit display of full-scan max == SA_REF 0.973669798383: PASS" "$RUN" || { echo "CHECK FAIL: F3b"; fail=1; }
grep -q "VERDICT: ALL CHECKS PASS" "$RUN" || { echo "CHECK FAIL: verdict"; fail=1; }
grep -q "ROBIN-FULL-1e10 DONE rc=0" "$RUN" || { echo "CHECK FAIL: done rc"; fail=1; }
if [ "$fail" -eq 0 ]; then echo "CHECK PASS: Robin full scan [1e9,1e10)"; else echo "CHECK FAIL"; fi
exit "$fail"
