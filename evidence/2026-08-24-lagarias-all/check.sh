#!/usr/bin/env bash
# Re-verifies claim #36: Lagarias inequality sigma(n) <= H_n + e^{H_n} log H_n
# holds for ALL 1 <= n <= 1e10. Re-runs every leg of the machine chain and
# greps each verdict. Runtime dominated by F2b (~30-40 min, exact-Fraction
# Q-smooth DFS) + F1c (~5 min, 1e10-gap EM scan); the rest are seconds.
set -euo pipefail
cd "$(dirname "$0")/../.."

run() { python3 "tracks/e-rh/$1"; }

echo "### F1a (B_n increasing, n<=55, 100-digit exact-H)"
out=$(run lagarias_f1a.py);  echo "$out";  echo "$out" | grep -q "VERDICT F1a: PASS"
echo "### F1b (B_n increasing to 1e7)"
out=$(run lagarias_f1b.py);  echo "$out";  echo "$out" | grep -q "VERDICT F1b: PASS"
echo "### F1c (B_n increasing to 1e10)"
out=$(run lagarias_f1c.py);  echo "$out";  echo "$out" | grep -q "VERDICT F1c: PASS"
echo "### F2c (b-file == record-holders, n<=10810800, exact)"
out=$(run lagarias_f2c.py);  echo "$out";  echo "$out" | grep -q "VERDICT F2c: PASS"
echo "### F2b (no record-holder in (10810800,1e10], exact) [SLOW ~30-40 min]"
out=$(run lagarias_f2b.py);  echo "$out";  echo "$out" | grep -q "VERDICT F2b: PASS"
echo "### F3+F4 (Lagarias on 55 SA n<=1e10; sigma cross-check)"
out=$(run lagarias_sa_check.py); echo "$out"
echo "$out" | grep -q "VERDICT F3: NO WITNESS"
echo "$out" | grep -q "VERDICT F4: PASS"
echo "CHECK PASS"
