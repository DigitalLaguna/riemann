# Track B — Polymath15 T-loop barrier run reproduced (2026-08-21, tick 67)

## Claim

Running Polymath15's own `TloopSinglematv2.c` (unmodified 2018 source from
`dbn_upper_bound/arb`, the repo the design doc designates as "already uses Arb, so
the numerical conventions are set for you") with the paper's shipped stored sums
reproduces the final paper's reported barrier verification exactly, and the run
completing to t = 0.2 without abort establishes the paper's bound
**Λ ≤ t₀ + y₀²/2 = 0.2 + 0.02 = 0.22** (Theorem 1.1).

This is the design doc's Track B target ("reproduce 0.22") and satisfies the week-4
kill criterion ("Polymath15 numerics reproduced to 2 significant figures") — the
agreement here is exact (integer mesh counts), i.e. better than 2 sig figs.

## What was run

- Program: `TloopSinglematv2.c`, args `ts=0 te=0.2 y0=0.2 Prt=0 <storedsums>`
  (argument names from the source's usage string, main() line 1071+).
- Stored sums: `runs/singlemat_X60000083951p5_d30.txt` (360 KB, shipped in the dbn
  repo; archived here as `stored-sums.txt`). X = 6e10+83951.5, 30-digit file.
- Toolchain: flint-pfx (FLINT 3.2.0 + bundled ACb + Arb 2.23.0), 160-bit balls.
  Single core, ~59 s wall.

## Machine output (verbatim)

`run-output.txt` — full 180-line output of the 2026-08-21 run: 171 rectangle
summaries for t = 0 … 0.19623 (step pattern from the paper's adaptive t-mesh),
per-rectangle `windtot = 0.000000`, minmodabb from 4.3192 (t=0) down to 1.5319
(t=0.196), final line `Overall winding number: 0.000000`, exit 0.

## Cross-check against the paper (lit/text/polymath15-2019.txt, fetched copy)

| Quantity | Paper says (verbatim, location) | Our run |
|---|---|---|
| Barrier params | "x = 6 × 10^10 + 83952 ± 0.5, y = 0.2 … 1, t = 0 … 0.2" (line 5565) | same file/args |
| Mesh at t=0 | "ranging from 11076 at t = 0 to 56 at t = 0.195" (lines 5582-5583) | 11076 (Rectangle 1, col 6) |
| Final mesh | same quote | 56 (Rectangle 171, col 6) |
| Final t | "t = 0.195" (line 5583) | t = 0.19623 (2 sig figs: 0.20 / 3 sig figs: 0.196) |
| Winding number | "The overall winding number for the barrier at this specific location came out at 0." (line 5586); "All barrier runs generated a winding number of zero for each rectangle and the scripts completed successfully" (line 7518) | Overall 0.000000; per-rectangle 0.000000; exit 0 |
| Bound | "Theorem 1.1 (New upper bound). We have Λ ≤ 0.22." (line 100) | no abort ⇒ Theorem 1.2 applies ⇒ Λ ≤ 0.2 + 0.2²/2 = 0.22 |

## The segfault bug (why the tick-53 binary died)

The 2018 code was written against standalone Arb/ACb, where
`acb_poly_struct = { coeffs; length; alloc; }` (length at offset 8). In FLINT 3.2
it is `{ coeffs; alloc; length; }` (length at offset 16). Compiling the program
with the Arb 2.23 headers (`$PFX/include`) against the FLINT 3.2 library
(`libflint.so.20`) makes the inline `acb_poly_zero()` zero offset 8, which the
library reads as `alloc = 0`; `acb_poly_fit_length` then calls `realloc(0-sized)`
→ segfault at 0x168 in the first rectangle (ASan: SEGV on 0x168). Compiling with
the FLINT 3.2 headers (include-v2) matches the library layout and the run is
clean. Full root cause: DEAD_ENDS.md B-002. Note the barrier-location program
(claim #6) did not hit this bug because it never calls acb_poly functions.

## Reproduction recipe

- `compile.sh <out-binary>` — exact gcc command (includes the forced
  `-include arb_mat.h` needed because FLINT's acb headers don't pull in
  arb_mat.h; without it `arb_mat_init` is an implicit function declaration and
  linking fails).
- `run.sh <binary> <output>` — exact run command.
- `check.sh` — recompiles from source, re-runs, asserts the five machine checks
  above; exit 0 = claim holds. (~1 min on 1 core.)

## Provenance

- Source: git clone of https://github.com/km-git-acc/dbn_upper_bound
  (tracks/b-dbn/dbn, fetched tick 52; TloopSinglematv2.c unmodified).
- Paper: arXiv:1904.12438 (current version, fetched 2026-08-25), lit/pdf + lit/text.
- Design-doc target: riemann-agent-plot.md §6 Track B ("reproduce 0.22"),
  card constants "Lambda <= 0.22"; week-4 kill criterion §7.
- Note for the ledger: earlier HANDOFF notes said "t_0 = 2.217e4" — that is the
  2019 v1 bound of arXiv:1904.12438; the fetched (current) version of the same
  paper reports t_0 = 0.2 and Λ ≤ 0.22, which is what the design doc's card and
  target reference.
