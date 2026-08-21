#!/usr/bin/env bash
# Exact compile recipe for Polymath15 TloopSinglematv2.c against the flint-pfx toolchain
# (FLINT 3.2.0 + bundled ACb + Arb 2.23.0, built by ticks 50-66).
#
# Header story (root cause of the segfault in the tick-53 binary, see DEAD_ENDS B-002):
#  - The dbn program is 2018-era code written against Arb/ACb as separate libraries
#    (acb_poly_struct: coeffs@0, length@8, alloc@16  [Arb 2.23 layout]).
#  - libflint.so.20 in flint-pfx is FLINT 3.2, whose acb_poly_struct is
#    coeffs@0, alloc@8, length@16  [FLINT layout].
#  - Compiling with the Arb 2.23 headers (include/) against the FLINT library
#    makes the inline acb_poly_zero() write `length` at offset 8, which the
#    library reads as `alloc` -> realloc(0) -> segfault in acb_poly_fit_length.
#  - Compiling with the FLINT 3.2 headers (include-v2, a symlink to
#    /tmp/flint-3.2.0/src at build time) makes the inlines match the library.
#  - The FLINT acb headers do not pull in arb_mat.h, so the program's use of
#    arb_mat_init/arb_mat_entry needs a forced include of the FLINT arb_mat.h.
set -euo pipefail
PFX=/home/niklas/riemann/tracks/b-dbn/flint-pfx
SRC=/home/niklas/riemann/tracks/b-dbn/dbn/dbn_upper_bound/arb
cd "$SRC"
# include-v2 must be a real copy of FLINT 3.2.0 src/ headers (it was a symlink to
# /tmp/flint-3.2.0/src; re-create if missing):
if [ ! -e "$PFX/include-v2/acb_types.h" ]; then
  mkdir -p "$PFX/include-v2"
  for f in /tmp/flint-3.2.0/src/*.h; do ln -s "$f" "$PFX/include-v2/"; done
  cp -rn /tmp/flint-3.2.0/src/flint "$PFX/include-v2/flint" 2>/dev/null || true
fi
gcc TloopSinglematv2.c -O2 \
  -I"$PFX/include-v2" -I"$PFX/include/flint" \
  -include arb_mat.h \
  -L"$PFX/lib" -lflint -lgmp -lmpfr -lm -o "$1"
