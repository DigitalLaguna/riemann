# HANDOFF — session 2026-08-22 20:59 CEST (owner manual, after tick 107; last frontier tick 91)
# track: B | gate: all tracks OPEN (21/21 seeds)

## State
19 claim rows: 8 NUMERIC (B: #3,4,6,7,8,9,18; E: #10), 2 FORMAL (A: #2 PNT+ local build,
#12 IK additive-API lemmas), 9 NOTE (#1 scaffold, #5 B diag, #11 B abeff semantics,
#13->#12, #14 B row-3 gate, #15 B Phase-3 audit, #16 B re-attribution, #17 B x6e12 abeff
argv, #19->#18). NEW: #18 NUMERIC — X=6e12 barrier row Lambda <= 0.19899966445
< 0.19999966445 (claim #9's X=5e12 row) — the design-doc 0.2 target is now met at two
barrier rows, each with all three legs machine-verified (check.sh pass=4 fail=0).
WEEK-2 MILESTONE (first XS Lean issue, due 09-03): MET in substance — PNT+ issue #816
claimed, 3 API lemmas on branch ik-additive-lemmas @ 0197a66, FULL lake build exit 0
(4343 jobs, lean4/mathlib v4.32.2), no new sorries. PR filing needs owner (fork).

## Last tick
tick 107 (track B, 20:41-20:51 CEST): polled run4 (alive, rect 1186->1540), extended
check.sh with leg (iii) (run4 exit/winding/abort check). Owner session (20:52-21:00):
RUN4 COMPLETED 20:48:05 CEST — exit=0, "Overall winding number: 0.000000", 1572 rects,
final t=0.17378709819414388239, 2656.9s cpu, no Abort (minmodabb >= 1.14 throughout),
status file + full output committed by tick 107 auto-commits (evidence/2026-08-22-x6e12/).
Pre-registered verdict APPLIED: NEW ROW X=6e12. check.sh re-run this session:
pass=4 fail=0 CHECK PASS. Tick 107 added+promoted #18 (promote.sh 18:50:47Z) 2 min
before this session's duplicate add -> merged #19 into #18 (A-004-class overlap:
re-read ledger after the checker, before adding). Side result: cgroup-kill diagnosis
CONFIRMED — run4 survived tick 106/107 exits while running; run2/run3 died exactly at
their launching ticks' exits (default KillMode=control-group; fix = systemd-run --user
own unit, now in run4_wrapper.sh pattern).

## Next action
(a) OWNER: one-click Fork of AlexKontorovich/PrimeNumberTheoremAnd -> then
    git push fork ik-additive-lemmas (branch @ 0197a66 in tracks/a-lean/pnt) + file PR
    (body ready: evidence/2026-08-22-pnt-ik-api/issue-816-draft.md, AI disclosure per
    PULL_REQUEST_STYLE.md) — closes the week-2 milestone fully.
(b) TRACK B (weight 40): X=6e12 row CLOSED. Next step to be decided at week-2 review
    (08-29): (i) X-sweep to 7e12 (lower Lambda further; stored sums = long pole,
    O(hours), launch pattern: isolated user unit like tloop-x6e12-run4);
    (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11, checker ready);
    (iii) row-3 t=0.18 push — BLOCKED on RH-to-1e13 source (Platt-Trudgian only 3e12).
    Until then: no new B experiments (pre-registration discipline).
(c) Tracks A/C/D/E: no in-flight work; A's PR leg is the only A-critical path.
    D (weight 15) has not started its first experiment since the gate opened.

## Blocked
- PNT+ PR filing: fork not yet created (owner one-click; rest is scripted)
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 review decision: REWEIGHT A30/B40/D15/C10/E5; condition "A claims first XS Lean
issue by 09-03" MET in substance (PR leg pending owner).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs +
decide B next step (X-sweep vs Arb port) and D's first experiment.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claims #7,#9,#18); the PR leg is the risk.
