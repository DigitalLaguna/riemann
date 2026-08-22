# HANDOFF
tick: 71 | 2026-08-22T00:07:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ FORMAL;
#3 H_0 closed form NUMERIC; #4 H_t heat flow NUMERIC; #5 barrier diagnostic NOTE;
#6 barrier LOCATION NUMERIC; #7 T-loop 0.22 run NUMERIC; #8 Table-1/0.20-path check
NUMERIC. Dead ends: A-001, A-002 (tooling), B-001 (GL quadrature), B-002 (Arb/FLINT
header layout; recipe now + forced -include stdlib.h for 2018 dbn code). C toolchain:
FLINT 3.2.0 + bundled ACb + Arb 2.23.0 in flint-pfx. 0.20 EXPERIMENT RUNNING (launched
this tick): two nohup jobs — stored sums for X=5e12 (PID 513995, long pole, several
hours) and the Lemma-10.1 |f| lower bound at N0=630783 (PID 514062). Full launch record:
evidence/2026-08-22-020-run/README.md.

## Last tick (71)
Compiled the 0.20 toolchain (StoredSumSinglematv1.c, New_abeff_largex_bounds.c) with
the B-002 recipe + forced -include stdlib.h (2018 code needed transitive stdlib for
EXIT_SUCCESS). Machine verdict YES: both exit 0; StoredSumSinglematv1 sanity-run at
6e10/8 digits matched the shipped 30-digit oracle to 8 digits (39x39 matrix, N
auto-selected); abeff smoke run exit 0. Launched both 0.20 jobs (nohup, output paths
in evidence/2026-08-22-020-run/README.md). Pre-registered verdict rule: 0.20 FALSIFIED
if winding != 0, T-loop aborts, or |f| bound at N0 < 0.03 (paper: 0.0376).

## Next action
Track B step 4c — harvest the 0.20 experiment results (check in this order each tick):
1. /tmp/abeff_020_N630783.txt — if finished: PASS if the Lemma bound >= 0.03.
2. runs/singlemat_X5000000194857p5_d30.txt — if header written ("5000000194857.5, N, N, 30"):
   compile TloopSinglematv2 (same recipe), run "0 0.186 0.16733 0 <file>" from the arb dir;
   PASS if winding 0 + no abort.
3. Both PASS => new claim (Lambda <= 0.20000 via promote.sh); append results to
   evidence/2026-08-22-020-run/README.md. Any FAIL => dead end + record actuals.
If both jobs still running, fall back to track A (PNT+ first theorem) or E (falsification
attempt) to keep the 24/7 mix — B is at most 50% of ticks.

## Blocked
- odlyzko-zeros full chapter text (AMS LibLynx login)
- lean-zulip-pnt full thread (Zulip JS UI, no API key)
- apt libflint-dev/libarb-dev (moot — flint-pfx self-sufficient)

## Budget
Frontier calls this week: 9 (10, 17, 39, 44, 45, 50, 69, 70, 71) — cap 5; overage =
escalations from local-model stalls (ticks 53-67 logged nothing despite real progress).
Week-4 kill criterion MET 2026-08-21 (claim #7). First weekly review (frontier) due
2026-08-24: ledger deltas by status, track B producing / others stalled, one decision,
Track E attempt + where it died, gardening.
