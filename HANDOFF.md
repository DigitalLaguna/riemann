# HANDOFF
tick: 50 | 2026-08-21T16:10:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ FORMAL;
#3 H_0 closed form NUMERIC; #4 H_t heat flow NUMERIC; #5 barrier diagnostic NOTE
(GL quadrature does not reach X0=6e10 — aliasing, needs AFE or C code). Dead ends:
A-001, A-002 (tooling), B-001 (GL quadrature at barrier). Tick 50 (frontier):
Arb 2.23.0+BUNDLED ACb built from flintlib/arb (benloko/ moved org — the 404 mystery)
into flint-pfx with 5 small FLINT-3.2 compat patches (evidence/2026-08-21-arb-build/);
Polymath15 BarrierLocationAssistant.c COMPILED and RUNS (machine exit 0, prints usage).
The C toolchain is up.

## Last tick (50)
Machine said YES: make exit 0 (libarb.so.2.14.0 + bundled ACb), make install exit 0,
gcc BarrierLocationAssistant exit 0, binary prints its usage text and exits 0.
Bounded step done; patch list + build/compile commands in evidence/2026-08-21-arb-build/README.md.

## Next action
Track B step 3b — RUN the barrier program, reproduce the barrier LOCATION:
1. Grep lit/text/polymath-15-paper.txt + dbn docs for the exact assistant invocation
   (x start, xnum, nprimes, thres; paper Sec 8.4: x = 6e10+83952 +/- 0.5, y [0.2,1], t [0,0.2]).
2. LD_LIBRARY_PATH=$PFX/lib BarrierLocationAssistant <params> with a window around 6e10;
   check the Aeff/Beff0-ratio dip appears at X0 = 6e10+83951.5 (left barrier edge).
   Machine verdict: dip at expected location = barrier location reproduced.
3. Record what t_0=2.217e4 itself needs: the T-loop programs (Tloop*.c) + stored sums —
   compile/run them for the 2-sig-fig t_0 confirmation (week-4 kill criterion, due ~2026-09-17).

## Blocked
- odlyzko-zeros full chapter text (AMS LibLynx login)
- lean-zulip-pnt full thread (Zulip JS UI, no API key)
- apt libflint-dev/libarb-dev (pkexec timeout; now mostly moot — flint-pfx has FLINT 3.2
  + Arb 2.23 + ACb; python-flint 0.9 still the workhorse for track B Python)

## Budget
Frontier calls this week: 6 (10, 17, 39, 44, 45, 50) — cap was 5, over by 1 (escalations
from local-model stalls; noted for week-1 review). Local model: ticks 46-49 = 4 ticks
(~2h) re-attempting the same 404 URLs without checking GitHub API org moves — reliability
data point. Week 1 ends 2026-08-24: week-1 milestone (track B closed form in Arb —
DONE: claims #3, #4) + first weekly review (frontier) due by 2026-08-24.
