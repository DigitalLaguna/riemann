# Track B — falsification test for the Phase-3 "ASYMPTOTICS binding" attribution (tick 91)

## What this is

The Phase-3 dominant-error-term audit (NOTE #15, evidence/2026-08-22-phase3-audit/)
attributed the 0.20 bound (claim #9, Lambda <= 0.19999966445) to the ASYMPTOTICS
(the |f| lower bound, hypothesis ii of Theorem 1.2), and directed B to "put compute
on the asymptotics". Tick 89 pre-registered a falsification test for that
attribution; tick 90 (local) ran it. This package records the result and the
re-attribution.

## Pre-registered falsification test (tick 89 log, verbatim)

  OUTCOME THAT KILLS "improve the |f| bound to lower t0": a re-run of
  New_abeff_largex_bounds at a LOWER t0 (e.g. t0 = 0.18) with the CURRENT
  asymptotics still gives |f| >= 0.03, meaning the |f| bound was NOT actually the
  binding constraint on t0 (the 0.186 choice was for the <0.2 target, not the |f|
  floor) — in which case the audit's attribution is wrong and B must re-attribute.

## The run (tick 90, local)

  $ /tmp/abeff 0.18 0.1 1261566 1261566 5 15
    (binary: New_abeff_largex_bounds.c, B-002 recipe; args t y N1 N2 m d)
  -> abeff_t018_N1261566.txt:
       Lower Lemma bound for t=0.2, y=0.1 in the range [N1=1261566,N2=1261566]
       using 5 primes:
       0.532101858344813
  (program prints t,y rounded to 1 dp; inputs were t=0.18, y=0.1.)
  0.532101858344813 >= 0.03  =>  the falsification condition is MET.

  NOTE: the program's "Lower Lemma bound" is the lower bound on the asymptotic
  PARTIAL SUM (Lemma 10.1), ~15x the paper's FINAL |f| bound (see NOTE #11). The
  final |f| bound = partial sum - rigorously bounded O-terms. So the partial-sum
  value 0.532 is an UPPER envelope; the authoritative final |f| values are the
  paper's Table 1 column (machine-checked in claim #8).

## The authoritative check (claim #8, Polymath15 Table 1, Sec 10)

  C4: |f| lower bound >= 0.03 in ALL 12 rows; min lb = 0.0305.
  In particular the t0=0.180 row (X=2e13+131252, y0=0.14142, N0=1261566) has
  final |f| bound = 0.0349 >= 0.03. So the |f| bound is NOT the constraint that
  prevents using t0=0.18 (or any lower t0 row).

## Re-attribution (machine-verified)

  The 0.20 bound uses Table 1 row 2 (X=5e12+194858, t0=0.186, y0=0.16733,
  N0=630783). The next row, row 3 (X=2e13+131252, t0=0.180, y0=0.14142,
  N0=1261566), would give Lambda <= 0.180 + 0.14142^2/2 = 0.1899998082 < 0.19999966445.
  But row 3 needs RH verified to X/2 = 1.0000000065626e13, which EXCEEDS the
  available Platt-Trudgian height 3e12. Row 2 needs only X/2 = 2.500000097429e12
  <= 3e12. Max X allowed by Platt-Trudgian: X <= 6e12.

  => The binding constraint on improving the 0.20 bound is the RH HEIGHT (X/2 <=
     3e12), NOT the asymptotics (|f| bound). The Phase-3 audit's "ASYMPTOTICS
     binding" attribution is WRONG (its own margin table had RH height 20.00%
     TIGHTER than asymptotics 25.33%, but it dismissed RH height as "external").

## Consequence (new compute target for B)

  Since Lambda is strictly decreasing in X (claim #8 C7) and the table jumps from
  X=5e12 (row 2, Lambda=0.19999966445) to X=2e13 (row 3, Lambda=0.19), there
  SHOULD be a row with X in (5e12, 6e12] (so X/2 <= 3e12, available) giving
  Lambda < 0.19999966445. The table has no such row (the authors' X grid skips
  it). NEXT: run the 0.20-push pipeline (stored sums + T-loop + |f| bound) at a
  new X in (5e12, 6e12] to find it. Pre-registered in the tick 91 log.
