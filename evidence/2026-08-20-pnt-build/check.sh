#!/usr/bin/env bash
# Re-verifies: PNT+ at commit 7715064f690d0689f30889846f4e2c5e7ec0c47e builds locally with toolchain v4.32.2.
# Machine = the Lean 4 compiler (lake build), which is up-to-date-aware.
set -euo pipefail
cd /home/niklas/riemann/tracks/a-lean/pnt
export PATH="$HOME/.elan/bin:$PATH"
[ "$(git rev-parse HEAD)" = "7715064f690d0689f30889846f4e2c5e7ec0c47e" ] || { echo "PNT+ moved off commit 7715064f690d0689f30889846f4e2c5e7ec0c47e"; exit 1; }
lake build
echo "PNT+ builds: 1 prior success(es) on record; this run exit 0"
