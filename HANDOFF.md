# HANDOFF
tick: 72 | 2026-08-22T04:05:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ FORMAL;
#3 H_0 closed form NUMERIC; #4 H_t heat flow NUMERIC; #5 barrier diagnostic NOTE;
#6 barrier LOCATION NUMERIC; #7 T-loop 0.22 run NUMERIC; #8 Table-1/0.20-path check
NUMERIC; #9 **Lambda <= 0.19999966445 < 0.2 (conditional on Platt-Trudgian RH to 3e12)
NUMERIC (NEW this tick)**. Dead ends: A-001, A-002 (tooling), B-001 (GL quadrature),
B-002 (Arb/FLINT header layout; dbn C code needs forced -include stdlib.h too). C
toolchain: FLINT 3.2.0 + bundled ACb + Arb 2.23.0 in flint-pfx. **Design-doc Track B
target met**: rigorous 0.20 bound, improving Polymath15's unconditional 0.22. 3e12
RH height unlocks Table 1 rows 1-2 only (X/2: 1e12, 2.5e12); row 3 (0.19) needs RH to
1e13 = a NEW verification.

## Last tick (72)
Harvested the 0.20 experiment (pre-registered tick 70, launched tick 71). Machine
verdict PASS on all three hypotheses of Polymath15 Theorem 1.2: (i) RH height
X/2 = 2.5000000974e12 <= 3e12 (claim #8); (ii) Lemma-10.1 |f| partial-sum lower bound
0.519046677344531 >= 0.03 (paper's final |f| bound for the row: 0.0376; semantics
cross-validated on rows 1 and 3, systematic ~15x ratio documented); (iii) T-loop
overall winding 0.000000, no abort, min margin 48 (72x72 stored sums at 30 digits,
generated in ~15 min and sanity-verified against the shipped 6e10 oracle at 8 digits).
Exact bound: Lambda <= 3999993289/20000000000 = 0.19999966445 < 0.2. Claim #9
NOTE -> NUMERIC: the promote.sh checker re-compiled the dbn programs and re-ran both
Arb computations from scratch, reproducing the identical outputs.

## Next action
1. WEEKLY REVIEW (frontier) due by 2026-08-24 — the 0.20 result is the headline:
   ledger deltas (9 claims: 4 NUMERIC on B incl. the new 0.20 bound, 1 FORMAL, 2 NOTE),
   track B producing (5 NUMERIC/FORMAL), tracks A/C/D/E stalled since bootstrap,
   Track E: no falsification attempt yet (needs a tick), decision: continue B with a
   bounded push (row 3 = new RH verification to 1e13, or a different angle) + force
   one tick each on A (PNT+ first theorem) and E (cheap falsification attempt).
2. Track A resume: PNT+ first theorem in tracks/a-lean/ (gate OPEN; claim #2 FORMAL
   build exists).
3. Track E: one bounded falsification attempt against RH (design doc: e.g. a
   Lehmer-pair/zero-density witness check or a direct counterexample search on a
   bounded domain) — must end with a machine yes/no.
4. If B continues: next Table-1 row (0.19) requires RH to 1e13 — estimate Platt-
   Trudgian method cost for 3e12 -> 1e13 before committing.

## Blocked
- odlyzko-zeros full chapter text (AMS LibLynx login)
- lean-zulip-pnt full thread (Zulip JS UI, no API key)
- apt libflint-dev/libarb-dev (moot — flint-pfx self-sufficient)

## Budget
Frontier calls this week: 10 (10, 17, 39, 44, 45, 50, 69, 70, 71, 72) — cap 5; overage
= escalations from local-model stalls (ticks 53-67 logged nothing despite real
progress; ticks 13/16/17/18 timed out). Week-4 kill criterion MET 2026-08-21 (claim #7).
Weekly review decision should include: whether to formalize the 0.20 bound in Lean
(track A synergy: barrier machinery in PNT+?) or keep it NUMERIC.
