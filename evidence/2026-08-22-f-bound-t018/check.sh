#!/usr/bin/env bash
# Re-verifies the re-attribution: the binding constraint on the 0.20 bound is the
# RH height (X/2 <= 3e12), NOT the asymptotics (|f| bound).
set -euo pipefail
cd "$(dirname "$0")"

# (1) tick-90 falsification run: |f| partial-sum bound at t0=0.18 >= 0.03
val=$(grep -Eo '^[0-9]+\.[0-9]+' abeff_t018_N1261566.txt | head -1)
python3 - "$val" <<'PY'
import sys
v = float(sys.argv[1])
assert v >= 0.03, f"abeff t0=0.18 bound {v} < 0.03 (attribution would STAND)"
print(f"PASS  (1) abeff t0=0.18 partial-sum |f| bound = {v} >= 0.03 (falsification condition MET)")
PY

# (2) authoritative: Polymath15 Table 1 final |f| bound >= 0.03 in ALL 12 rows
out=$(bash ../2026-08-21-table1/check.sh 2>&1)
echo "$out" | grep -q "PASS  C4 |f| lower bound >= 0.03" || { echo "FAIL: table1 C4 not PASS"; exit 1; }
minlb=$(echo "$out" | grep -Eo 'min lb = [0-9.]+' | grep -Eo '[0-9.]+')
python3 - "$minlb" <<'PY'
import sys
m = float(sys.argv[1])
assert m >= 0.03, f"table min |f| {m} < 0.03"
print(f"PASS  (2) Table 1 final |f| bound >= 0.03 in all 12 rows (min lb = {m})")
PY

# (3) RH-height availability: row 2 available, row 3 blocked, max X = 6e12
python3 <<'PY'
X2 = 5e12 + 194858; X3 = 2e13 + 131252; H = 3e12
assert X2/2 <= H, "row 2 should be available"
assert X3/2 >  H, "row 3 should be blocked"
L2 = 0.186 + 0.16733**2/2
L3 = 0.180 + 0.14142**2/2
assert L3 < L2, "row 3 bound should beat row 2"
print(f"PASS  (3) row2 X/2={X2/2:.4g} <= 3e12 (available, Lambda={L2}); "
      f"row3 X/2={X3/2:.4g} > 3e12 (blocked, Lambda={L3:.10f} < {L2})")
print("VERDICT: RH HEIGHT (X/2) is the binding constraint, NOT the asymptotics (|f| bound)")
PY
echo "CHECK PASS: re-attribution machine-verified (ASYMPTOTICS attribution killed)"
