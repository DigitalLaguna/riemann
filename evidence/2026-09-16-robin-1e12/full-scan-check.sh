#!/usr/bin/env bash
# Checker for the Robin-criterion FULL scan over [1e11,1e12) (robin_full_scan.py
# with subseg checkpoint, relaunched tick 246 as robin-full-1e12.service,
# output full-run-resume.txt). The scan is the machine verification (exact
# int64 sigma, F1 sympy cross-check, 50-digit mpmath R); this checker asserts
# the stored output is complete and consistent, and independently re-verifies
# the reported argmax with sympy exact sigma at 50 dps.
set -u
cd "$(dirname "$0")/../.."
RUN=evidence/2026-09-16-robin-1e12/full-run-resume.txt
fail=0
grep -q "range \[100000000000,1000000000001)  subseg width 100000000" "$RUN" || { echo "CHECK FAIL: missing range header"; fail=1; }
[ "$(grep -c '^subseg' "$RUN")" -eq 1000 ] || { echo "CHECK FAIL: expected 1000 subseg lines, got $(grep -c '^subseg' "$RUN")"; fail=1; }
grep -q "F1 cross-check: checked=[0-9]* mismatches=0: PASS" "$RUN" || { echo "CHECK FAIL: F1"; fail=1; }
grep -q "F2 witness R(n)>=1 in \[100000000000,1000000000001): none (max R < 1)" "$RUN" || { echo "CHECK FAIL: F2 (witness HIT => RH FALSE)"; fail=1; }
grep -q "F3a consistency: .*: PASS" "$RUN" || { echo "CHECK FAIL: F3a"; fail=1; }
grep -q "F3b regression: 12-sig-digit display of full-scan max == SA_REF 0.975505922736: PASS" "$RUN" || { echo "CHECK FAIL: F3b"; fail=1; }
grep -q "VERDICT: ALL CHECKS PASS" "$RUN" || { echo "CHECK FAIL: verdict"; fail=1; }
python3 - << 'PYEOF' || fail=1
import json, re
import mpmath as mp, sympy
mp.mp.dps = 50
EG = mp.e ** mp.mpf("0.57721566490153286060651209008240243104215933593992")
run = open("evidence/2026-09-16-robin-1e12/full-run-resume.txt").read()
m = re.search(r"FULL SCAN \[100000000000,1000000000001\): max R = (\S+) at n = (\d+) \(sigma=(\d+)\)", run)
assert m, "missing FULL SCAN line"
R_rep, n, sg_rep = m.group(1), int(m.group(2)), int(m.group(3))
sg = int(sympy.divisor_sigma(n))
assert sg == sg_rep, f"sigma mismatch: sympy={sg} run={sg_rep}"
R = mp.mpf(sg) / (EG * mp.mpf(n) * mp.log(mp.log(mp.mpf(n))))
assert mp.nstr(R, 16) == R_rep, f"R mismatch: mpmath={mp.nstr(R, 16)} run={R_rep}"
assert R < 1, "witness R>=1 => RH FALSE"
ck = json.load(open("evidence/2026-09-16-robin-1e12/ckpt-1e12.json"))
assert ck["n_sub"] == 1000, f"ckpt n_sub={ck['n_sub']} != 1000"
print("spot-check: argmax n=%d sigma=%d R=%s (sympy exact, 50 dps) matches run; ckpt n_sub=1000" % (n, sg, R_rep))
PYEOF
if [ "$fail" -eq 0 ]; then echo "CHECK PASS: Robin FULL scan [1e11,1e12) verified"; else echo "CHECK FAIL"; fi
exit "$fail"
