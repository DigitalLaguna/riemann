#!/bin/bash
# run4 wrapper (owner session 2026-08-22 ~19:55 CEST; pre-registered tick-105 log section)
# Pre-registered command: TloopSinglematv2 0 0.185 0.16733 0 runs/singlemat_X5999999999999p5_d30.txt
# Binary: /tmp/tloop (47808 bytes, built 2026-08-22 02:17 tick 71, B-002 recipe; the binary
# that produced row-2's verified winding=0 run, evidence/2026-08-22-020-run/)
cd /home/niklas/riemann/tracks/b-dbn/dbn/dbn_upper_bound/arb
export LD_LIBRARY_PATH=/tmp/flint-3.2.0/build/lib
EV=/home/niklas/riemann/evidence/2026-08-22-x6e12
echo "start $(date -u +%FT%TZ) binary=/tmp/tloop md5=$(md5sum /tmp/tloop | cut -d' ' -f1)" > $EV/tloop_x6e12_run4.status
/tmp/tloop 0 0.185 0.16733 0 runs/singlemat_X5999999999999p5_d30.txt \
  > $EV/tloop_x6e12_run4.txt 2> $EV/tloop_x6e12_run4.err
echo "exit=$? end=$(date -u +%FT%TZ)" >> $EV/tloop_x6e12_run4.status
