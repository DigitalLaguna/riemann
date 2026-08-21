# Track B — Polymath15 Table 1 (Sec 10) machine check: the Λ ≤ 0.20 path is unlocked (tick 70, 2026-08-21)

## What this is

The design doc's Track B target after 0.22 is "push below 0.20 with rigorous bounds",
and the design doc / Polymath15 project notes claim newer RH verification heights
should already give Λ ≤ 0.20. This evidence package machine-checks the arithmetic of
that claim against the fetched paper, so the next tick can run the actual 0.20
experiment with pre-registered inputs.

## The key formula (verified from the PDF, not the mangled pdftotext)

Theorem 1.2 hypothesis (i) — required RH verification height for a barrier at X with
parameter y0 — is read off the PDF via `pdftohtml -xml` coordinates (page 2,
hypothesis (i) text block, tops 728-768):

  no zeroes ζ(σ+iT) = 0 with  (1+y0)/2 ≤ σ ≤ 1  and  0 ≤ T ≤ X/2

Geometry: the left fraction has numerator tokens `1`(748), `y`(748), `0`(752), `+`(745)
over denominator `2`(762) at left 160-180 = (1+y0)/2; the right fraction has `X`(top 750,
left 339) over `2`(top 762, left 340) = X/2. (Plain pdftotext interleaves the two
fractions and the surrounding text, making it ambiguous.)

Self-consistency check (C5): the paper's own 0.22 run has X = 6e10+83951.5, so
X/2 = 3.0000042e10 ≤ 3.06e10 — exactly the Platt 2017 height [18] the paper says it
used (line 4286: "the result of Platt [18] that all the non-trivial zeroes of ζ with
imaginary part between 0 and 3.06 × 10^10 lie on the critical line"). If the formula
were 2X/(1+y0) (the other plausible reading of the mangled text), the required height
would be 1.0e11 > 3.06e10 and the paper's own proof would not close. Formula confirmed.

## The 0.20 row (Table 1, second row)

X = 5×10^12 + 194858, t0 = 0.186, y0 = 0.16733, Λ = 0.20, winding 0, N0 = 630783,
|f| lower bound 0.0376 (text lines 7233-7305 of lit/text/polymath15-2019.txt).

Required RH height: X/2 = 2.5000001e12 (barrier-center convention; left edge X−0.5
would give 2.500000097e12 — same verdict).
Available RH height: Platt–Trudgian 2020 (lit/text/platt-trudgian-2020.txt, Abstract,
p. 1, verbatim): "We verify numerically, in a rigorous way using interval arithmetic,
that the Riemann hypothesis is true up to height 3 · 10^12. That is, all zeroes
β + iγ of the Riemann zeta-function with 0 < γ ≤ 3 · 10^12 have β = 1/2."
Since β = 1/2 for all γ ≤ 3e12, in particular there are no zeroes with
(1+y0)/2 = 0.5837 ≤ σ ≤ 1 and γ ≤ 2.5e12. Hypothesis (i) holds. 2.5e12 < 3e12 ✓.

## Checks (run-output.txt, machine verdict PASS)

- C1 table parsed: 12 rows in every column
- C2 internal consistency: |t0 + y0²/2 − Λ| ≤ 0.005 for all 12 rows (actual max 0.0000)
- C3 winding number 0 in all 12 rows
- C4 |f| lower bound ≥ 0.03 in all 12 rows (min 0.0305; paper's stated safety margin)
- C5 X/2 formula self-consistent with the paper's own 0.22 run
- C6 0.20 row: X/2 = 2.5000001e12 ≤ 3e12 (Platt–Trudgian) and > 3.06e10 (not available
  at the paper's own height) → UNLOCKED by existing verified RH data
- C7 monotone: t0 and Λ strictly decrease as X increases

## Pre-registered next experiment (0.20 push)

Run the dbn Upper_bound programs with the 0.20-row parameters:
- barrier: X = 5e12+194858 (center), t0 = 0.186, y0 = 0.16733
- (iii) T-loop: winding number 0, no abort (min modabb > 1)
- (ii) asymptotic check: |f_{t0}(x + i y0)| lower bound ≥ 0.03 at x = N0 = 630783
  (paper achieved 0.0376)
- (i) RH height: X/2 = 2.5000001e12 ≤ 3e12 (Platt–Trudgian, above)
FALSIFIED if any of the three numerical checks fails (winding ≠ 0, abort, or
lower bound < 0.03). Success establishes Λ ≤ 0.186 + 0.16733²/2 = 0.20000 (2 dp: 0.20),
a strict improvement over the paper's unconditional 0.22 — the design doc's target.
Open question for the next tick: which dbn programs generate the stored sums and the
asymptotic lower bound for a new X (StoredSumSinglematv1.c and the H_t asymptotic
verifier), and how long they take at X = 5e12 (the 6e10 stored-sums file appeared at 17:01,
during the local ticks 53-67 window of 14:38-17:46, so several hours of machine time).
