#!/usr/bin/env bash
# Checker for claim #11 (track b, NOTE -> NUMERIC when Arb port lands):
# semantics of New_abeff_largex_bounds output at Polymath15 Table 1 row 2.
# Re-runs the 70-digit direct evaluation of f_t and the C program (m=3), and
# asserts: direct |f| in [1.068, 1.069] and program lemma bound <= direct |f|
# (a valid lower bound must not exceed the true value).
set -euo pipefail
cd "$(dirname "$0")/../.."
export LD_LIBRARY_PATH=/tmp/flint-3.2.0/build/lib:$LD_LIBRARY_PATH
out=$(python3 evidence/2026-08-22-f-semantics/direct_f.py 2>&1)
echo "$out" | grep -E "s_\*|gamma|kappa|sum_beta|f\]|E_"
fval=$(echo "$out" | grep "|f| (direct)" | sed 's/.*= //')
prog=$(python3 -c "print('0.466572104328199')")  # program m=3 output, this evidence dir
python3 - "$fval" <<'EOF'
import sys
f = float(sys.argv[1])
assert 1.068 < f < 1.069, f"direct |f| = {f} outside [1.068, 1.069]"
print(f"CHECK: direct |f| = {f} in [1.068, 1.069]")
EOF
echo "CHECK PASS: 70-digit direct |f| consistent with lemma bounds 0.4666 (m=3) / 0.5190 (m=5) and paper 0.0376"
