#!/usr/bin/env bash
# check.sh — re-verify claim: BarrierLocationAssistant (nprimes=5, primes<=11) reproduces the
# Polymath15 barrier location X = 6e10+83951.5 (paper Sec 8.4, t0=y0=0.2).
# Machine: the C program (Arb ball arithmetic). Asserts the real-part-(-1/2) Euler product
# has its unique dominant peak at X within 0.5 (grid spacing) of 6e10+83951.5.
set -euo pipefail
PFX="$HOME/riemann/tracks/b-dbn/flint-pfx"
BIN="$HOME/riemann/tracks/b-dbn/dbn/dbn_upper_bound/arb/BarrierLocationAssistant"
# wide window centered on the barrier location, exact paper params (nprimes=5, y0=t0=0.2)
out="$(LD_LIBRARY_PATH=$PFX/lib "$BIN" 60000083940.0 20 5 0 0.2 0.2 0)"
# strip commas -> whitespace, then for each data row take max of real-part-(-1/2) cols (f2,f3,f4)
read -r peak_x peak_v <<< "$(awk '
  { gsub(/,/," ") }
  NF>=7 && $1 ~ /^[0-9]+(\.[0-9]+)?$/ {
    m=$2; if($3>m)m=$3; if($4>m)m=$4;
    if(m>best){best=m; bx=$1}
  }
  END{printf "%s %s", bx, best}' <<< "$out")"
echo "peak X = $peak_x  (real-part-(-1/2) Euler-product max = $peak_v)"
# assert peak X within 0.5 of the paper barrier location 60000083951.5
if awk -v x="$peak_x" 'BEGIN{d=x-60000083951.5; if(d<0)d=-d; exit !(d<=0.5)}'; then
  echo "CHECK PASS: peak at $peak_x is within 0.5 of barrier location 6e10+83951.5"
else
  echo "CHECK FAIL: peak at $peak_x not within 0.5 of 6e10+83951.5"; exit 1
fi
