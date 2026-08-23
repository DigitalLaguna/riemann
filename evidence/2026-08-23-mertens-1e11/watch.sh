#!/usr/bin/env bash
# Watcher for mertens 1e11 attempt 3 (pid 700783; output in systemd journal).
# Sequence: wait for the run to exit -> capture journal output (clean) to
# run3.txt -> run check.sh (re-runs the exact-integer scan, asserts C1-C7,
# record/witness determinism vs run3.txt, F4 witness<1.0, F5 maxabs>=50286)
# -> log check.sh's output to check-run.txt. All timestamps UTC.
set -uo pipefail
EV=evidence/2026-08-23-mertens-1e11
PID=700783
cd "$(dirname "$0")/../.."
echo "watcher started $(date -u +%FT%TZ) waiting for pid $PID" >> "$EV/watch.log"
while kill -0 "$PID" 2>/dev/null; do sleep 30; done
echo "pid $PID exited $(date -u +%FT%TZ)" >> "$EV/watch.log"
journalctl _PID=$PID --output=cat --no-pager > "$EV/run3.txt" 2>>"$EV/watch.log"
echo "captured run3.txt ($(wc -l < "$EV/run3.txt") lines) $(date -u +%FT%TZ)" >> "$EV/watch.log"
echo "--- run3.txt tail ---" >> "$EV/watch.log"
tail -6 "$EV/run3.txt" >> "$EV/watch.log"
bash "$EV/check.sh" > "$EV/check-run.txt" 2>&1
rc=$?
echo "check.sh rc=$rc $(date -u +%FT%TZ)" >> "$EV/watch.log"
echo "--- check-run.txt tail ---" >> "$EV/watch.log"
tail -8 "$EV/check-run.txt" >> "$EV/watch.log"
echo "WATCHER DONE rc=$rc $(date -u +%FT%TZ)" >> "$EV/watch.log"
