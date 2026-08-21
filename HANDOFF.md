# HANDOFF
tick: 69 | 2026-08-21T23:15:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ FORMAL;
#3 H_0 closed form NUMERIC; #4 H_t heat flow NUMERIC; #5 barrier diagnostic NOTE (GL
aliasing); #6 barrier LOCATION NUMERIC; #7 T-loop barrier run NUMERIC (NEW this tick:
Polymath15's exact paper run reproduced, Lambda <= 0.22). Dead ends: A-001, A-002
(tooling), B-001 (GL quadrature at barrier), B-002 (NEW: Arb/FLINT header layout bug).
C toolchain: FLINT 3.2.0 + bundled ACb + Arb 2.23.0 in flint-pfx; dbn C programs build
with FLINT headers (see B-002 for the trap).

## Last tick (69)
Machine said YES: ran Polymath15's unmodified TloopSinglematv2.c (dbn repo) with the
paper's shipped stored sums (singlemat_X60000083951p5_d30.txt), barrier X=6e10+83951.5,
y0=0.2, t in [0,0.2]. 171 t-steps, exit 0, no abort (min modabb 1.5319 > 1), overall
winding 0.000000, mesh 11076 (t=0) -> 56 (t=0.19623). Paper's reported values
(lit/text/polymath15-2019.txt lines 5565/5582/5586): mesh 11076 -> 56 at t=0.195,
winding 0 — EXACT match on both mesh counts, winding to 2 sig figs on final t. Theorem
1.2 of the paper then gives Lambda <= t0 + y0^2/2 = 0.2 + 0.02 = 0.22 (Theorem 1.1).
Week-4 kill criterion (numerics reproduced to 2 sig figs) MET. Root-caused the tick-66
segfault (B-002: Arb 2.23 vs FLINT 3.2 acb_poly_struct layout; tick-53 binary used the
wrong headers); recorded recipe in evidence/2026-08-21-tloop/ (compile.sh, run.sh,
check.sh, full output, stored-sums archive). Claim #7 NOTE -> NUMERIC via promote.sh.

## Next action
Track B step 4 — push BELOW 0.22 (design doc: "then push below 0.20 with rigorous
bounds"). Bounded step: read paper Sec 9-10 + dbn wiki for what feeds the "Lambda <=
0.20 with newer RH heights" claim (the card records the paper's conditional table:
Lambda <= 0.1 if RH verified to T ~ 4.5e21), identify the exact inputs (RH height T,
barrier X0, y0), then pre-register ONE bounded experiment. If the 0.20 path needs a new
stored-sums file, budget for StoredSumSinglematv1.c first.
Secondary: track A week-4 milestone ("one Lean PR opened upstream") still open — check
PNT+ open issues for a small claimable one.

## Blocked
- odlyzko-zeros full chapter text (AMS LibLynx login)
- lean-zulip-pnt full thread (Zulip JS UI, no API key)
- apt libflint-dev/libarb-dev (moot — flint-pfx self-sufficient)

## Budget
Frontier calls this week: 7 (10, 17, 39, 44, 45, 50, 69) — cap was 5; overage was
escalations from local-model stalls (46-49, 53-68). Local-model reliability: ticks
53-67 did real work but logged nothing; tick 68 entry truncated. Week 1 ends
2026-08-24: week-1 milestone DONE (B closed forms in Arb, claims #3/#4), first weekly
review (frontier) due by 2026-08-24. Week-4 kill criterion MET 2026-08-21 (claim #7).
