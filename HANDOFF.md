# HANDOFF
tick: 52 | 2026-08-21T17:10:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ FORMAL;
#3 H_0 closed form NUMERIC; #4 H_t heat flow NUMERIC; #5 barrier diagnostic NOTE
(GL quadrature does not reach X0=6e10 — aliasing, needs AFE or C code); #6 barrier
LOCATION NUMERIC (NEW this tick). Dead ends: A-001, A-002 (tooling), B-001 (GL quadrature
at barrier). C toolchain up (tick 50): Arb 2.23.0+BUNDLED ACb in flint-pfx,
BarrierLocationAssistant.c compiled and runs.

## Last tick (52)
Machine said YES: ran BarrierLocationAssistant with the EXACT paper params (nprimes=5 =
primes<=11, y0=t0=0.2, paper Sec 8.4 line 150: "t0=0.2, X=6e10+83952-0.5, y0=0.2"). The
real-part-(-1/2) Euler product has a single dominant peak at X=6e10+83951.5 (value 26.21,
symmetric at X=6e10+83952.5), unique in [6e10+83940.5,6e10+83960.5] (next 9.03, <1 two steps
away). check.sh PASS (peak within 0.5 of 6e10+83951.5). Claim #6 NOTE -> NUMERIC.
NOTE: tick 51 had already run the program (3 output files) but never recorded the verdict;
this tick closed that. tick 51's thres0_window.txt used a different nprimes (col2=53.63 vs
26.21 here) — nprimes scales magnitude, not peak location.

## Next action
Track B step 3c — t_0=2.217e4 (the actual bound input) comes from the T-loop programs, NOT
the barrier-location assistant. Bounded step:
1. Read TloopSinglematv2.c main() (and TloopDualmatv2.c / TloopthreadedV4.c) to find the
   invocation + the stored-sum input files it reads ("Processing the barrier for X=...").
2. Check whether the stored sums are SHIPPED in the dbn repo or must be computed first
   (StoredSumSinglematv1.c / StoredSumsDualmatv1.c / StoredSumsThreaded.c).
3. Compile+run for the 2-sig-fig t_0=2.2e4 confirmation (week-4 kill criterion, due ~2026-09-17).
All numerics in Arb ball arithmetic (the C programs already are).

## Blocked
- odlyzko-zeros full chapter text (AMS LibLynx login)
- lean-zulip-pnt full thread (Zulip JS UI, no API key)
- apt libflint-dev/libarb-dev (mostly moot — flint-pfx has FLINT 3.2 + Arb 2.23 + ACb;
  python-flint 0.9 still the workhorse for track B Python)

## Budget
Frontier calls this week: 6 (10, 17, 39, 44, 45, 50) — cap was 5, over by 1 (escalations from
local-model stalls; noted for week-1 review). Local model: ticks 46-49 = 4 ticks (~2h)
re-attempting the same 404 URLs without checking GitHub API org moves — reliability data point.
Week 1 ends 2026-08-24: week-1 milestone (track B closed form in Arb — DONE: claims #3, #4)
+ first weekly review (frontier) due by 2026-08-24.
