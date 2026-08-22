#!/bin/bash
# Track B 0.20-push pipeline at X=6e12 (tick 94). Detached jobs.
# Params: X_left=5999999999999.5, t0=0.185, y0=0.16733, N=690988
# Lambda = t0 + y0^2/2 = 0.19899966445 < 0.19999966445 (target)
export LD_LIBRARY_PATH=/tmp/flint-3.2.0/build/lib
ARB=tracks/b-dbn/dbn/dbn_upper_bound/arb
EV=evidence/2026-08-22-x6e12
cd ~/riemann

# Job 1: stored sums (LONG POLE ~15 min)
setsid nohup /tmp/storedsum 5999999999999.5 30 \
  > $ARB/runs/singlemat_X5999999999999p5_d30.txt 2> $EV/storedsum.err &
echo "storedsum PID $!" > $EV/pids.txt

# Job 2: abeff |f| bound (~6 min), independent of job 1
setsid nohup /tmp/abeff 0.185 0.16733 690988 690988 5 15 \
  > $EV/abeff_x6e12.txt 2> $EV/abeff_x6e12.err &
echo "abeff PID $!" >> $EV/pids.txt
echo "launched $(date -u +%FT%TZ)" >> $EV/pids.txt
