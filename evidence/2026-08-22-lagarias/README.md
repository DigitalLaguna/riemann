# Track E — Lagarias Problem E bounded falsification, N = 10^6 (claims #10)

Pre-registered tick 78 (2026-08-22T04:24:48Z, logs/2026-08-22.tick.log), run tick 78,
reproducibility re-run tick 79 (04:41 UTC).

## The equivalence (lagarias-2002, Theorem 1.1; card lit/cards/lagarias-2002.md)

RH <=> for all n >= 1:  sigma(n) <= H_n + e^{H_n} log H_n,  equality only at n = 1.
Verbatim from the paper (lit/text/lagarias-2002.txt line 613):
"For 1 <= n <= 5040 one verifies (1.1) directly by computer, the only case of equality
being n = 1."  Our run extends the direct computer verification from 5040 to 10^6.

## Method (explicit error bound)

sigma(n): exact integer, divisor sieve (O(N log N), N = 10^6, 1.2 s).
H_n: digamma(n+1) + euler at 100 digits (exact identity, mpmath 100-digit ops carry
per-op error < 1e-95; ~4 ops per n keeps total |err| < 1e-90).
margin(n) = H_n + e^{H_n} log H_n - sigma(n).
Verdict threshold: margin <= 1e-80 counts as non-positive (10 orders of magnitude
above the error bound, so the sign is rigorous).
Machine verdict: NO COUNTEREXAMPLE in [1,N]  vs  COUNTEREXAMPLE FOUND (witness n).

## Machine output (verbatim, run_N1e6.txt; re-run identical, run_N1e6_rerun.txt)

    sieve N=1000000: 1.2s
    scan N=1000000: 76.2s
    min margin (n>=2): 0.3171685434118021783180761906577313314269920015416883884949297863249837122715354412219748081124551881 at n=2
    VERDICT: NO COUNTEREXAMPLE in [1,1000000] (all margins > 1e-80 at 100 digits)

Re-run: min margin and verdict identical to all 50 printed digits; scan 76.7 s.

## Prior art (logged, tick 78)

- lagarias-2002 itself: direct check to 5040 (above quote).
- arXiv:2602.15905 (2026-02-16): least counterexample, if any, is superabundant
  (abstract fetched verbatim) -> next lever: verify on superabundants only, push N.
- arXiv:2503.03159 (2025-03-05): inequality holds for almost every n (classes listed
  in abstract) -> further lever.
- arXiv:2606.15096 (2026-06-13, agent paper "VGPT-RSI"): claims verified finite
  Lagarias bounds; its claimed bound must be checked before citing.

## Claim

#10 (track e, NUMERIC): "Lagarias inequality sigma(n) <= H_n + e^{H_n} log H_n holds
for all 1 <= n <= 10^6 (100-digit rigorous margin, min margin 0.31716854... at n=2,
machine verdict NO COUNTEREXAMPLE; extends lagarias-2002's own check at 5040 by a
factor of ~200). RH NOT falsified up to this bound."

Note: this is the expected negative result (a positive result would be a witness).
Track E week-1 "where it died" answer: it did not die — the obstruction map for the
Lagarias direction is empty so far; the search is witness-hunting (closer in spirit
to track D) and will be reclassified at the next attempt.
