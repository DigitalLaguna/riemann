#!/usr/bin/env bash
# Claim: closed-form H_0(z) for track B (Arb, rigorous balls).
# Re-runs both machine checks:
#  1) real axis: 14 points vs Polymath15 output/numbers/sample_output_Ht_real.txt
#  2) complex z=35+10i vs independent 70-digit mpmath term-by-term quadrature
set -euo pipefail
cd "$(dirname "$0")/../.."
out1=$(python3 tracks/b-dbn/ht_closed_form.py)
echo "$out1" | grep -q "ALL MATCH to 8 digits: True"
out2=$(python3 tracks/b-dbn/ht_closed_form_v2.py)
echo "$out2" | grep -q "real digits match: True"
echo "$out2" | grep -q "imag digits match: True"
# explicit error bound: Arb ball radius < 1e-30
rad=$(echo "$out2" | head -2 | grep -o 'rad = [0-9.e+-]*' | awk '{print $3}')
python3 -c "import sys; sys.exit(0 if float('$rad') < 1e-30 else 1)"
echo "CHECK OK"
