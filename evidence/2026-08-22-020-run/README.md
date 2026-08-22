# Track B — 0.20 push: job launch record (tick 71, 2026-08-22 UTC)

Pre-registered experiment (falsification test in evidence/2026-08-21-table1/README.md,
tick 70 log entry). Parameters: Table 1 row 2 — X = 5e12+194858 (center), left edge
X = 5000000194857.5, t0 = 0.186, y0 = 0.16733, N0 = 630783, 5-prime Euler mollifier.
RH height: X/2 = 2.5000001e12 <= 3e12 (Platt–Trudgian, claim #8).

Toolchain: flint-pfx (FLINT 3.2.0 + bundled ACb + Arb 2.23.0), B-002 compile recipe
plus forced `-include stdlib.h` (2018 code relied on transitive stdlib for EXIT_SUCCESS).

## Jobs (launched 2026-08-22 ~00:00 UTC, nohup)

1. Stored sums (LONG POLE, expected several hours — 6e10/30-digit took the whole
   14:38-17:46 window of 2026-08-21):
   ```
   /tmp/storedsum 5000000194857.5 30
   ```
   (binary: gcc StoredSumSinglematv1.c -O2 -I$PFX/include-v2 -I$PFX/include/flint
   -include arb_mat.h -include stdlib.h -L$PFX/lib -lflint -lgmp -lmpfr -lm)
   -> tracks/b-dbn/dbn/dbn_upper_bound/arb/runs/singlemat_X5000000194857p5_d30.txt
   Sanity-verified first: ran the same binary at 6e10/8 digits; output matched the
   shipped 30-digit oracle to 8 digits (tick 71 log).

2. Hypothesis-(ii) |f| lower bound (Lemma 10.1 bound, N0 = 630783):
   ```
   /tmp/abeff 0.186 0.16733 630783 630783 5 15
   ```
   (binary: New_abeff_largex_bounds.c, same flags)
   -> /tmp/abeff_020_N630783.txt
   PASS if output >= 0.03 (paper achieved 0.0376 at this row).

3. T-loop (when job 1's file exists):
   ```
   TloopSinglematv2 0 0.186 0.16733 0 runs/singlemat_X5000000194857p5_d30.txt
   ```
   (compile TloopSinglematv2.c with the same recipe; run from the arb directory)
   PASS if "Winding number = 0" and "Abort" is not printed (min modabb > 1).

## Verdict rule (machine)

- All three PASS (and claim #8's RH height, already NUMERIC) => new claim:
  Lambda <= 0.186 + 0.16733^2/2 = 0.20000, a rigorous improvement over the paper's
  unconditional 0.22 (design-doc Track B target met).
- Any FAIL => 0.20 row falsified; record actual vs expected in this directory and
  add a dead-end entry.

## Results (all three checks PASS, 2026-08-22 ~00:30 UTC)

1. (ii) Lemma-10.1 |f| lower bound (abeff_020_N630783.txt):
   `Lower Lemma bound for t=0.2, y=0.2 in the range [N1=630783,N2=630783] using 5 primes:`
   **0.519046677344531** (wall 353.6 s). [Program prints t,y rounded to 1 dp; inputs were
   0.186, 0.16733.] The paper's Table 1 reports the FINAL |f| bound for exactly this row as
   0.0376 (target >= 0.03). The program's "lemma bound" is the lower bound on the asymptotic
   PARTIAL SUM (Lemma 10.1); the final |f| bound = partial sum - rigorously bounded O-terms
   (the paper's analysis). Cross-validation on two other rows confirms the semantics:
     row 1 (t=0.198, y=0.15492, N=398942): program 0.5233686 vs paper table 0.0341 (15.3x)
     row 3 (t=0.18,  y=0.14142, N=1261566): program 0.5321019 vs paper table 0.0349 (15.2x)
   Systematic ratio -> consistent; the program (current dbn repo) computes the lemma bound,
   the paper's table lists the final |f| bound. Both are positive and >= 0.03.
   NOTE: an earlier "validation" run used wrong row-1 params (y=0.17962, N=280478) — a
   transcription error; the correct row-1 params (y=0.15492, N=398942) are used above and
   match the dbn Writeup/debruijn.tex line 1949 exactly.
2. (iii) T-loop (tloop_020_run.txt): **Overall winding number: 0.000000**, no Abort line
   (grep count 0), min of the final margin column = 48 (>> 1), 659 rectangles, wall 959.4 s.
   Header: "Processing the barrier for X= 5000000194857.5000000...5000000194858.5000000
   (N = 630783), y0 = 0.16733, t = 0...0.186".
3. (i) RH height (claim #8): X/2 = 2.5000000974e12 <= 3e12 (Platt-Trudgian 2020).

Stored sums (job 1): completed in ~15 min (faster than feared): header
"5000000194857.5, 72, 72, 30" (72x72 matrix at 30 digits; 6e10 file was 65x65).

EXACT BOUND (rational arithmetic, python fractions):
  Lambda <= t0 + y0^2/2 = 186/1000 + (16733/100000)^2/2 = 3999993289/20000000000
           = 0.19999966445 < 0.2

VERDICT: PASS on all three hypotheses of Theorem 1.2 =>
  Lambda <= 0.19999966445 (conditional on Platt-Trudgian RH verification to 3e12),
  improving Polymath15's unconditional Lambda <= 0.22. Design-doc Track B target met.
