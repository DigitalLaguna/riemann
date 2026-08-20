# HANDOFF
tick: 1 | 2026-08-20T16:05:00Z | track: A (carding) | gate: all CLOSED

## State
Track A: 3/4 seeds carded (tao-2026-ant, ipam-ant, pnt-plus all PASS
card.py + gate.py). lean-zulip-pnt still missing. Track A CLOSED until it
is carded. PNT+ local clone at tracks/a-lean/pnt: lake build completed
successfully (4343 jobs, logs/2026-08-20-pnt-build.log). Open-issue
snapshot (39 issues) at lit/text/pnt-plus-issues.json.

## Last tick
Carded tao-2026-ant, ipam-ant, pnt-plus. Machine said: card.py check OK x3;
gate.py check a -> 3 PASS, lean-zulip-pnt FAIL (missing card). One dead end:
gate.py requires the location paren in main_result to START with a keyword
(Section/Theorem/...), e.g. (Section "2. Claiming a Task", CONTRIBUTING.md).

## Next action
Card lean-zulip-pnt (last Track A seed): try Zulip API without auth or a
public archive; if neither works, park it and card Track B seeds instead
(polymath15-2019 arXiv 1904.12438 is the cheapest fetch). Track A stays
CLOSED until 4/4, so no Lean work yet.

## Blocked
lean-zulip-pnt needs a Zulip fetch method (API key or archive). If parked
again, say so here with the date.

## Budget
Frontier calls used this week: 0 (of the 5 escalation triggers).
Local model: qwen3.8-27b on :8080. Weekly review due 2026-08-27.
