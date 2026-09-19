#!/usr/bin/env bash
# Checker for the claim: "C1 (Lemma 3) holds rigorously for the corrected
# kappa_m re-optimization: p(x) = sum_{m=0}^6 kappa_m x^m > 0 for all x in
# (0,1], kappa_6 = -29/859 + 0.0382944246562725."
# Paper: bellotti-trudgian-yang-2026 (arXiv:2603.21490 v1), Lemma 3.
#
# Re-compiles c1_p_positive_arb.c from source (Arb 512-bit ball arithmetic,
# flint-pfx toolchain) and re-runs it, asserting:
#   1. run exits 0
#   2. no subinterval prints "NOT > 0"
#   3. VERDICT line prints YES
set -euo pipefail
EV="$(cd "$(dirname "$0")" && pwd)"
PFX=/home/niklas/riemann/tracks/b-dbn/flint-pfx
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# 1) compile from source
gcc "$EV/c1_p_positive_arb.c" -O2 \
  -I"$PFX/include-v2" -I"$PFX/include/flint" -I"$PFX/include" \
  -include arb_mat.h \
  -L"$PFX/lib" -lflint -lgmp -lmpfr -lm -o "$WORK/c1" \
  || { echo "FAIL: compile failed"; exit 1; }

# 2) run
RC=0
LD_LIBRARY_PATH="$PFX/lib" "$WORK/c1" > "$WORK/out.txt" 2>&1 || RC=$?
[ "$RC" -eq 0 ] || { echo "FAIL: run exited $RC"; cat "$WORK/out.txt"; exit 1; }

# 3) assertions
NFAIL=$(grep -c "NOT > 0" "$WORK/out.txt" || true)
[ "$NFAIL" = "0" ] || { echo "FAIL: $NFAIL subinterval(s) not > 0"; cat "$WORK/out.txt"; exit 1; }
grep -q "VERDICT: C1 (Lemma 3) p(x)>0 on (0,1] for corrected kappa ? YES" "$WORK/out.txt" \
  || { echo "FAIL: VERDICT is not YES"; cat "$WORK/out.txt"; exit 1; }
echo "PASS: C1 (Lemma 3) p(x)>0 on (0,1] for corrected kappa (Arb 512-bit; all 256 subintervals > 0)"
