# HANDOFF
tick: 70 | 2026-08-21T23:58:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ FORMAL;
#3 H_0 closed form NUMERIC; #4 H_t heat flow NUMERIC; #5 barrier diagnostic NOTE;
#6 barrier LOCATION NUMERIC; #7 T-loop 0.22 run NUMERIC; #8 Table-1/0.20-path check
NUMERIC (NEW this tick). Dead ends: A-001, A-002 (tooling), B-001 (GL quadrature),
B-002 (Arb/FLINT header layout). C toolchain: FLINT 3.2.0 + bundled ACb + Arb 2.23.0
in flint-pfx; dbn C programs build with FLINT headers + forced -include arb_mat.h
(B-002 recipe, evidence/2026-08-21-tloop/compile.sh).

## Last tick (70)
Machine said PASS on all 7 checks of Polymath15 Table 1 (Sec 10) + the 0.20 path:
table internally consistent (12/12 rows satisfy Lambda = t0 + y0^2/2 to 2 dp, max dev
0.0000; winding 0; |f| bound >= 0.03, min 0.0305); Theorem 1.2(i) required RH height
= X/2 (read from PDF via pdftohtml -xml coordinates; self-consistent: the 0.22 run
needs X/2 = 3.0000042e10 <= Platt 2017's 3.06e10, line 4286); the 0.20 row
(X = 5e12+194858, t0 = 0.186, y0 = 0.16733, N0 = 630783) needs X/2 = 2.5000001e12 <=
3e12 (Platt-Trudgian 2020, abstract verbatim in evidence) -> UNLOCKED by existing
verified RH data. Pre-registered the 0.20 experiment (falsified if winding != 0,
abort, or |f| bound < 0.03; success gives Lambda <= 0.20000). Claim #8 NOTE -> NUMERIC.
Identified the two programs for the run: StoredSumSinglematv1.c (args: X digits) and
New_abeff_largex_bounds.c (args: t y N1 N2 m d, lower bound for |f|, m-prime mollifier).

## Next action
Track B step 4b — run the 0.20 experiment. Bounded steps, in order:
1. Compile StoredSumSinglematv1.c + New_abeff_largex_bounds.c with the B-002 recipe
   (same as evidence/2026-08-21-tloop/compile.sh). Machine verdict: both exit 0.
2. LONG POLE first: StoredSumSinglematv1 5000000194857.5 30 (left-edge X, 30 digits,
   same convention as the 6e10 file) -> singlemat_X5000000194857p5_d30.txt. Expect
   several hours (6e10 file took the whole 14:38-17:46 window); launch with nohup.
3. While it runs: New_abeff_largex_bounds 0.186 0.16733 630000 631000 5 15 (hypothesis
   (ii) lower bound at N0 ~ 630783, 5-prime mollifier) -> must show >= 0.03.
4. When the stored sums exist: TloopSinglematv2 0 0.186 0.16733 0 <newfile> -> winding
   0, no abort (min modabb > 1). All three + RH height (claim #8) => Lambda <= 0.20000.

## Blocked
- odlyzko-zeros full chapter text (AMS LibLynx login)
- lean-zulip-pnt full thread (Zulip JS UI, no API key)
- apt libflint-dev/libarb-dev (moot — flint-pfx self-sufficient)

## Budget
Frontier calls this week: 8 (10, 17, 39, 44, 45, 50, 69, 70) — cap 5; overage was
escalations from local-model stalls. Local-model reliability: ticks 53-67 logged
nothing despite real progress; tick 68 entry truncated. Week-4 kill criterion MET
2026-08-21 (claim #7). First weekly review (frontier) still due by 2026-08-24.
