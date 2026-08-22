# Track B — 0.20 experiment (hypothesis iii: |f| lower bound at N0)

Pre-registered in tick 70 (see logs/2026-08-21.tick.log, "pre-registered next
experiment (0.20 push)"). Inputs from Polymath15 Table 1 row 2 (lit/text/
polymath15-2019.txt lines 7233-7305): X = 5e12+194858, t0 = 0.186, y0 = 0.16733,
N0 = 630783, target |f| >= 0.03 (paper's own listed bound for this row: 0.0376).

## What was run (this step)
- Program: New_abeff_largex_bounds.c (unmodified 2018 dbn source), args
  `0.186 0.16733 630783 630783 5 15` (t y N1 N2 m d). m=5 = 5-prime Euler
  mollifier {2,3,5,7,11}; d=15 = display digits (working prec = d*3.32+30 ~ 79 bits).
  N1=N2=630783 = single point x=N0, the exact quantity the paper's table lists.
- Compiled by the tick-70 agent with the B-002 recipe (FLINT 3.2 headers
  include-v2 + forced -include arb_mat.h, same as evidence/2026-08-21-tloop/
  compile.sh but source = New_abeff_largex_bounds.c), binary at /tmp/abeff.
- Wall 353.6 s, single core.

## Machine output (verbatim) — abeff_020_N630783.txt
    Lower Lemma bound for t=0.2, y=0.2 in the range [N1=630783,N2=630783] using 5 primes:

    0.519046677344531

    cpu/wall(s): 353.599 353.637

Note: the program prints t,y at 1 sig fig (arb_printn(t,1,...)); actual args were
0.186 / 0.16733.

## Verdict
|f_{t0}(x+iy0)| lower bound at x=N0=630783 = 0.519046677344531 >= 0.03  =>  PASS
(hypothesis (iii) of Theorem 1.2 for the 0.20 row). The paper's listed 0.0376 is
their cruder bound for the same point; our 5-prime-mollifier Arb bound is 13.8x
sharper. Both clear the 0.03 target, so the discrepancy is mollifier/sharpness,
not a contradiction.

## Still running (long pole)
- StoredSumSinglematv1 (unmodified), args `5000000194857.5 30` (left-edge X, 30
  digits, same convention as the shipped 6e10 file), binary /tmp/storedsum,
  PID 513995, output -> runs/singlemat_X5000000194857p5_d30.txt. The 6e10 file
  took ~3 h; expect hours. When done: TloopSinglematv2 0 0.186 0.16733 0
  runs/singlemat_X5000000194857p5_d30.txt -> winding 0, no abort (minmodabb > 1).
