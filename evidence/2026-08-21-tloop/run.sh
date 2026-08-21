#!/usr/bin/env bash
# Exact run command: Polymath15 T-loop barrier verification for the paper's barrier
# (X = 6e10+83951.5, y0 = 0.2, t in [0, 0.2]), using the paper's shipped stored sums.
# Usage: ./run.sh <binary> <output_file>
set -euo pipefail
PFX=/home/niklas/riemann/tracks/b-dbn/flint-pfx
BIN="${1:?binary}"
OUT="${2:?output file}"
cd /home/niklas/riemann/tracks/b-dbn/dbn/dbn_upper_bound/arb
# argv: ts te y0 Prt singlematfile  (source: TloopSinglematv2.c main, line 1071+)
LD_LIBRARY_PATH="$PFX/lib" "$BIN" 0 0.2 0.2 0 runs/singlemat_X60000083951p5_d30.txt > "$OUT"
