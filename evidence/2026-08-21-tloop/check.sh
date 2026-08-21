#!/usr/bin/env bash
# Checker for the claim: "Polymath15 T-loop barrier verification reproduced."
# Re-compiles TloopSinglematv2.c from source (dbn repo, unmodified 2018 code),
# re-runs the barrier with the paper's shipped stored sums, and asserts:
#   1. run exits 0 (no abort: minmodabb stayed >= 1 for all t in [0, 0.2])
#   2. overall winding number = 0        (paper: line 5586 of lit/text/polymath15-2019.txt)
#   3. mesh at t=0 is 11076              (paper: line 5582, "ranging from 11076 at t = 0")
#   4. final mesh is 56 at t >= 0.19     (paper: line 5582, "to 56 at t = 0.195")
#   5. min minmodabb over all rectangles > 1 (rigorous barrier condition, Theorem 1.2)
# Exit 0 = claim holds.
set -euo pipefail
EV="$(cd "$(dirname "$0")" && pwd)"
PFX=/home/niklas/riemann/tracks/b-dbn/flint-pfx
SRC=/home/niklas/riemann/tracks/b-dbn/dbn/dbn_upper_bound/arb
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

# 0) stored sums present (either local repo copy or the archived copy)
SS="$SRC/runs/singlemat_X60000083951p5_d30.txt"
[ -f "$SS" ] || SS="$EV/stored-sums.txt"
[ -f "$SS" ] || { echo "FAIL: stored-sums file missing"; exit 1; }

# 1) compile from source
"$EV/compile.sh" "$WORK/tloop"

# 2) run the barrier
cd "$SRC"
LD_LIBRARY_PATH="$PFX/lib" "$WORK/tloop" 0 0.2 0.2 0 "$SS" > "$WORK/out.txt" 2>&1
RC=$?
[ "$RC" -eq 0 ] || { echo "FAIL: run exited $RC"; tail -5 "$WORK/out.txt"; exit 1; }

# 3) assertions
grep -q "^Overall winding number: 0\.000000" "$WORK/out.txt" \
  || { echo "FAIL: overall winding number != 0"; exit 1; }

FIRST=$(grep "^Rectangle(1)" "$WORK/out.txt" | head -1)
echo "$FIRST" | grep -q ", 11076$" \
  || { echo "FAIL: mesh at t=0 != 11076 (got: $FIRST)"; exit 1; }

LAST=$(grep "^Rectangle" "$WORK/out.txt" | tail -1)
echo "$LAST" | grep -qE ", 56$" \
  || { echo "FAIL: final mesh != 56 (got: $LAST)"; exit 1; }
TEND=$(echo "$LAST" | cut -d' ' -f3 | cut -d',' -f1)
awk "BEGIN{exit !($TEND >= 0.19)}" \
  || { echo "FAIL: final t $TEND < 0.19 (paper: 0.195)"; exit 1; }

MIN=$(awk -F',' '/^Rectangle/ {v=$5+0; if (min=="" || v<min) min=v} END{print min}' "$WORK/out.txt")
awk "BEGIN{exit !($MIN > 1.0)}" \
  || { echo "FAIL: min modabb $MIN <= 1 (barrier not verified)"; exit 1; }

N=$(grep -c "^Rectangle" "$WORK/out.txt")
echo "PASS: t-loop barrier run reproduced: $N rectangles, t=0..$TEND, winding 0, mesh 11076->56, min modabb $MIN > 1"
echo "PASS: implies Lambda <= t0 + y0^2/2 = 0.2 + 0.02 = 0.22 (paper Theorem 1.1, line 100)"
