#!/usr/bin/env bash
# Checker for the claim: "C3c (Lemma 14) holds rigorously for the corrected
# kappa_m re-optimization (kappa_6 += K, K = 0.0382944246562725)."
# Paper: bellotti-trudgian-yang-2026 (arXiv:2603.21490 v1).
#
# Re-compiles c3c_lemma14_arb.c from source (Arb 512-bit ball arithmetic,
# flint-pfx toolchain) and re-runs it, asserting:
#   1. run exits 0
#   2. all 6 checks print PASS (C1 w0>0, C2 M1>0, C3 R(u0)>0, C4 R'(u0)>0,
#      C5 mu0>1/13, C6 M1*u_max>w0)
#   3. VERDICT line prints YES
#
# Math: D_mod = D_paper + K*B6 with D_paper >= 0 (published Lemma 14), so
# C3c holds iff B6 > 0 on the domain; steps (1)-(7) in the source header
# reduce B6 > 0 to the 6 exact checks.
set -euo pipefail
EV="$(cd "$(dirname "$0")" && pwd)"
PFX=/home/niklas/riemann/tracks/b-dbn/flint-pfx
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# 1) compile from source
gcc "$EV/c3c_lemma14_arb.c" -O2 \
  -I"$PFX/include-v2" -I"$PFX/include/flint" \
  -include arb_mat.h \
  -L"$PFX/lib" -lflint -lgmp -lmpfr -lm -o "$WORK/c3c" \
  || { echo "FAIL: compile failed"; exit 1; }

# 2) run
RC=0
LD_LIBRARY_PATH="$PFX/lib" "$WORK/c3c" > "$WORK/out.txt" 2>&1 || RC=$?
[ "$RC" -eq 0 ] || { echo "FAIL: run exited $RC"; cat "$WORK/out.txt"; exit 1; }

# 3) assertions
NFAIL=$(grep -c ": FAIL" "$WORK/out.txt" || true)
[ "$NFAIL" = "0" ] || { echo "FAIL: $NFAIL check(s) printed FAIL"; cat "$WORK/out.txt"; exit 1; }
grep -q "VERDICT: C3c (Lemma 14) holds rigorously for corrected kappa ? YES" "$WORK/out.txt" \
  || { echo "FAIL: VERDICT is not YES"; cat "$WORK/out.txt"; exit 1; }
echo "PASS: C3c (Lemma 14) holds rigorously for corrected kappa (Arb 512-bit; all 6 checks PASS)"
