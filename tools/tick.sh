#!/usr/bin/env bash
# tick.sh — one bounded tick of the Riemann research operator.
# Fired by the systemd user timer riemann-tick.timer every 30 minutes.
# A tick is one bounded unit of work that commits its own result; state
# lives in git and the ledger, never in the agent's context.
set -uo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.elan/bin:$PATH"

LOCK=ledger/.tick.lock
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) previous tick still running; skipping" >> logs/ticks.log
  exit 0
fi

python3 tools/agent_tick.py
