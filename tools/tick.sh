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
rc=$?

# Backup push (added 2026-08-23, owner-approved): remote origin =
# git@github.com:DigitalLaguna/riemann.git (SSH). Non-fatal: a failed push
# must not fail the tick; failures are logged and retried next tick.
if git remote get-url origin >/dev/null 2>&1; then
  if git push -q origin main >> logs/push.log 2>&1; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) push ok $(git rev-parse --short HEAD)" >> logs/push.log
  else
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) push FAILED (see logs/push.log)" >> logs/ticks.log
  fi
fi
exit $rc
