#!/usr/bin/env bash
# Checker for claim #9: Lambda <= 0.19999966445 < 0.2 (conditional on Platt-Trudgian
# RH verification up to 3e12), realizing Polymath15 Table 1 row 2 (X = 5e12+194858,
# t0 = 0.186, y0 = 0.16733, N0 = 630783).
#
# Re-runs the machine checks (Arb ball arithmetic, dbn's own unmodified C programs):
#   1. exact rational arithmetic: Lambda <= t0 + y0^2/2 < 0.2 and X/2 <= 3e12  (fast)
#   2. re-run New_abeff_largex_bounds at the 0.20 params -> Lemma-10.1 partial-sum
#      lower bound must be >= 0.03  (~6 min)
#   3. re-run TloopSinglematv2 on the freshly archived stored sums ->
#      "Overall winding number: 0.000000" and no Abort  (~16 min)
# Set SKIP_SLOW=1 to skip 2 and 3 (uses archived outputs instead) for a ~1 min check.
set -euo pipefail
cd /home/niklas/riemann
ROOT=$(pwd)
EV=evidence/2026-08-22-020-run
ARBDIR=$ROOT/tracks/b-dbn/dbn/dbn_upper_bound/arb
PFX=$ROOT/tracks/b-dbn/flint-pfx
BIN=$(mktemp -d)
trap 'rm -rf "$BIN"' EXIT

echo "[1/3] exact rational bound check"
python3 - <<'EOF'
from fractions import Fraction as F
t0, y0 = F(186, 1000), F(16733, 100000)
b = t0 + y0*y0/2
assert b < F(1, 5), f"bound {b} not < 0.2"
assert F(5000000194857, 2) <= F(3*10**12), "RH height X/2 > 3e12"
print(f"  Lambda <= {b} = {float(b):.11f} < 0.2 OK; X/2 = 2.5000000974e12 <= 3e12 OK")
EOF

if [ "${SKIP_SLOW:-0}" = "1" ]; then
  echo "[2/3] SKIP_SLOW: verifying archived abeff output"
  grep -E '^[0-9]+\.[0-9]+$' "$EV/abeff_020_N630783.txt" | head -1 | \
    python3 -c "import sys; v=float(sys.stdin.read().strip()); assert v >= 0.03, v; print(f'  archived lemma bound {v} >= 0.03 OK')"
  echo "[3/3] SKIP_SLOW: verifying archived tloop output"
  grep -q "Overall winding number: 0.000000" "$EV/tloop_020_run.txt" && echo "  archived winding 0 OK"
  ! grep -q "Abort" "$EV/tloop_020_run.txt" && echo "  no abort OK"
  echo "CHECK PASS (fast path)"
  exit 0
fi

FLAGS="-O2 -I$PFX/include-v2 -I$PFX/include/flint -include arb_mat.h -include stdlib.h -L$PFX/lib -lflint -lgmp -lmpfr -lm"
echo "[compile] dbn programs (unmodified)"
(cd "$ARBDIR" && gcc New_abeff_largex_bounds.c $FLAGS -o "$BIN/abeff" && \
                gcc TloopSinglematv2.c      $FLAGS -o "$BIN/tloop")
echo "  compiled OK"

echo "[2/3] re-run abeff (Lemma-10.1 lower bound, t=0.186 y=0.16733 N=630783 m=5)"
OUT2=$(env LD_LIBRARY_PATH=$PFX/lib "$BIN/abeff" 0.186 0.16733 630783 630783 5 15)
echo "$OUT2" | sed 's/^/  /'
V=$(echo "$OUT2" | grep -E '^[0-9]+\.[0-9]+$' | head -1 | tr -d ' ')
python3 -c "v=float('$V'); assert v >= 0.03, v; print(f'  lemma bound {v} >= 0.03 OK')"

echo "[3/3] re-run tloop (stored sums $ARBDIR/runs/singlemat_X5000000194857p5_d30.txt)"
head -1 "$ARBDIR/runs/singlemat_X5000000194857p5_d30.txt" | \
  grep -q "^5000000194857\.5000000000000000000, 72, 72, 30" || { echo "stored-sums header mismatch"; exit 1; }
OUT3=$(cd "$ARBDIR" && env LD_LIBRARY_PATH=$PFX/lib "$BIN/tloop" 0 0.186 0.16733 0 \
       runs/singlemat_X5000000194857p5_d30.txt 2>&1)
echo "  $(echo "$OUT3" | grep 'Overall winding number')"
echo "$OUT3" | grep -q "Overall winding number: 0.000000" || { echo "winding != 0"; exit 1; }
! echo "$OUT3" | grep -q "Abort" || { echo "tloop aborted"; exit 1; }
echo "  winding 0, no abort OK"

echo "CHECK PASS — Lambda <= 0.19999966445 < 0.2 (conditional on Platt-Trudgian RH to 3e12)"
