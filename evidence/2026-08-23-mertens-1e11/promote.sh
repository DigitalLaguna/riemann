#!/usr/bin/env bash
# Promote claim #27 (Mertens record at 1e11) NOTE -> NUMERIC.
# Runs the checker (evidence/2026-08-23-mertens-1e11/check.sh), which re-runs
# the exact-integer 1e11 scan (~70 min) and asserts C1-C7 + record/witness
# determinism vs run3.txt + F4 (witness<1.0) + F5 (maxabs>=50286).
set -uo pipefail
cd /home/niklas/riemann
EV=evidence/2026-08-23-mertens-1e11
echo "promote started $(date -u +%FT%TZ) for claim #27" >> "$EV/watch.log"
bash tools/promote.sh promote 27 NUMERIC "$EV" > "$EV/promote-run.txt" 2>&1
rc=$?
echo "promote.sh rc=$rc $(date -u +%FT%TZ)" >> "$EV/watch.log"
echo "--- promote-run.txt tail ---" >> "$EV/watch.log"
tail -6 "$EV/promote-run.txt" >> "$EV/watch.log"
echo "PROMOTE DONE rc=$rc $(date -u +%FT%TZ)" >> "$EV/watch.log"
