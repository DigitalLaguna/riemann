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

Results will be appended to this file as they arrive.
