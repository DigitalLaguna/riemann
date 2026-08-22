# Weekly review — 2026-08-22 (frontier, week 1, early)

## Ledger deltas (since bootstrap 2026-08-20; no prior review)

Total 11 claims: **NUMERIC 7, FORMAL 1, NOTE 3**.
- Track B: 8 claims — 6 NUMERIC (#3 H_0 closed form, #4 heat flow, #6 barrier location,
  #7 T-loop 0.22, #8 Table 1 + 0.20 path, #9 **Lambda <= 0.19999966445 < 0.2**), 2 NOTE (#5 GL
  diagnostic, #11 f-semantics resolved this review).
- Track A: 1 FORMAL (#2 PNT+ local build). Track E: 1 NUMERIC (#10 Lagarias to 1e6, this
  review). Scaffold: 1 NOTE (#1).
- Delta this tick: +2 claims (#10 NUMERIC, #11 NOTE); #10 checker ran 3 independent scans.

## Producing vs stalled

- **B — producing hard.** Design-doc Phase 1 (reproduce Polymath15) met AND beaten: Phase 2
  already delivered (0.22 -> 0.19999966445, claim #9; week-4 kill criterion met early).
- **A — stalled 2 days** (last activity 2026-08-20 22:06: PNT+ build). Zero Lean theorems
  attempted. Week-2 milestone ("first XS Lean issue claimed") at risk; week-4 ("one Lean PR
  upstream") needs a start by ~week 3.
- **C — stalled** (no claims, gate open, no work). **D — stalled** (spec says "always
  running on spare cores"; it has never run). **E — first attempt done** (below).
- Weight audit vs design doc (A 40 / B 30 / C 15 / D 10 / E 5): the last ~28 ticks were
  almost all B; A has had ~1 tick in 2 days despite the 40% weight. Weights are not being
  executed; the local model drifts to momentum.

## Track E — the attempt and where it died

Attempt (week 1): Lagarias Problem E bounded falsification, N = 1e6 (pre-registered tick 78,
run tick 78, reproducibility re-run tick 79, frontier-claimed this review as #10).
Result: **no counterexample** (min margin 0.3172 at n=2; extends the paper's own check at
5040). Where it died: **it did not die** — expected negative result; the obstruction map is
empty. Note: the attempt was executed by the local model, not the frontier (spec says
frontier); also it is witness-hunting in spirit (track D). Next lever logged: restrict to
superabundant numbers (arXiv:2602.15905) to push N past 1e6 cheaply.

## Decision (one, concrete)

**REWEIGHT: A 40 -> 30, B 30 -> 40, D 10 -> 15, C 15 -> 10, E 5 unchanged.** Rationale:
weight follows verified output (B just produced the project's headline result); D gets +5 to
actually start its "always running" background search (a machine, not a model, should do it);
C's re-optimization needs B/A constants as input first. Conditions: (i) track A must claim
its first XS Lean issue by the week-2 checkpoint (2026-09-03) or A drops to 20 with the 10
points going to B; (ii) if B's row-3 attempt (t=0.18, needs RH to 1e13) stalls >1 week, revert
to A 40 / B 30. No track killed this week.

## Gardening

- Added: evidence/2026-08-22-lagarias/, evidence/2026-08-22-f-semantics/ (each with
  verbatim machine output + re-verifying check.sh); DEAD_ENDS +A-003 (tick-79 PNG-as-text
  crash, same class as A-002); this review.
- Deleted: none. Merged: none. Compressed: ticks 74-79 already single-line in ticks.log.
- Risk noted (not fixed): FLINT/Arb toolchain lives in /tmp/flint-3.2.0 — a /tmp cleanup
  kills the track B toolchain; move to a persistent prefix is a bounded next tick.
- Local-model reliability (week 1): of ticks 60-79, ~8 produced no work (steps=0/timeout/
  crash); ticks 66-68 spent 3 ticks on one compile line. Frontier used 7 times.

## Milestone check (week 1, early — all green)

Scaffold running, ledger live, PNT+ builds locally, HANDOFF/DEAD_ENDS live: YES (all since
2026-08-20). "All tracks CLOSED, agent is reading": EXCEEDED (all 5 gates OPEN, 9 claims
before this review). Week-2 watch item: first XS Lean issue (track A).
