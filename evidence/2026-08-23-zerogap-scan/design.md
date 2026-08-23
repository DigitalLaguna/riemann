# Zero-spacing / Lehmer-pair scan — DESIGN (track D)
date: 2026-08-23 (tick 150)
status: DESIGN — pre-registered falsification below; NOT yet run.

## Goal
Compute zeros of Z(t) = re(e^{iθ_asym(t)} ζ(1/2+it)) up to height T, the
normalized consecutive gaps δ_n = (t_{n+1}-t_n)·log(t_n/2π)/(2π), and report:
  - max δ_n (largest normalized gap) + location
  - min δ_n (smallest normalized gap) + location
  - r-gaps r=1,2,3: max_n (t_{n+r}-t_n)·log(t_n/2π)/(2π r) + location
  - Lehmer-pair count (see definition note)
  - sanity: zero count N(T) vs Riemann-von Mangoldt; mean δ ≈ 1
First pass: T = 1e4 (N_rvm ≈ 10143). Extend to T = 1e5 (N_rvm ≈ 138069) only
if the first pass is competitive (F2) and fast enough.

## Record targets (scoped against carded prior art)
From inoue-kobayashi-toma-2025 (lit/cards/inoue-kobayashi-toma-2025.md):
  - λ1 > 3.18 (Bui-Milinovich [3], best under RH) — r=1 max-gap target.
  - µ1 < 0.515396 (Preobrazhenskii [10], best under RH) — r=1 min-gap target.
  - Theorem 2 (large r): λr ≥ 1+sqrt(2/r)-..., µr ≤ 1-sqrt(2/r)+...
    -> r=2: λ2 ≥ 2.0; r=3: λ3 ≥ 1.816. WEAK for small r (asymptotic is
    "sufficiently large r"); treat r=2,3 comparison as informational only.
  - Theorem 3: Montgomery-Odlyzko method limitation λ1 ≥ 3.022, µ1 ≤ 0.508
    (bounds what that method can certify — relevant if a large gap needs explaining).
Lehmer-pair line (evidence/2026-08-23-zerogap-preflight/preflight.txt):
  1508.05870, 1612.08627, 2411.07909, 2509.00906.
  DEFINITION NOTE: design uses the operational definition "a consecutive pair
  (γ_i,γ_{i+1}) is a Lehmer pair iff Z does not change sign at γ_{i+1}, i.e.
  the sign of Z on (γ_i,γ_{i+1}) equals the sign on (γ_{i+1},γ_{i+2})".
  VERIFY against 1508.05870 / 1612.08627 (fetch + verbatim quote) before any
  Lehmer-pair CLAIM. Count is reported regardless.

## Method
Z(t) real on the critical line (verified tick 142, st_check-run.txt).
  1. Grid t_i = t_start + i·step, step = 0.1. Safe: min gap at T=1e4 is 0.426
     (0.5×mean 0.852), so ≥4 grid pts per min gap -> no missed/merged zeros.
  2. Z(t_i) = re(e^{iθ_asym(t_i)} ζ(1/2+i t_i)), mpmath at DPS (default 15).
     θ_asym verified vs exact to 3.8e-19 (tick 142).
  3. Sign-change intervals (t_i,t_{i+1}) with Z(t_i)·Z(t_{i+1}) < 0.
  4. Bisect each to width 1e-9 (~27 steps).
  5. Sort, dedupe (1e-6), compute gaps.
mpmath = development tool, NOT rigorous -> first-pass result is a NOTE, not
NUMERIC (a NUMERIC claim needs Arb acb_zeta or an explicit error bound).

## PRE-REGISTERED FALSIFICATION (written before running)
F1 (method broken -> result VOID) if ANY of:
   - zero count N outside [0.99·N_rvm, 1.01·N_rvm]
   - mean δ outside [0.99, 1.01]
   - any δ < 0.4 (below known min ~0.5) or any δ > 6 (unphysical)
   - first zero not in [14.13, 14.14] (known γ_1 ≈ 14.1347)
F2 (record framing dead at this height): if max δ < 3.0, then T=1e4 is not
   competitive with the 3.18 Bui-Milinovich bound -> must go higher (T=1e5+)
   or drop the "record vs 3.18" framing.
F3 (Lehmer pairs): report the count. If 0, that is a checkable claim — verify
   the first Lehmer pair's location against a fetched source before claiming.

## What a hit (witness) means
A machine-computed concrete value that is a finite-height record or a specific
witness (e.g. a Lehmer pair at a specific t, or a max δ exceeding a previously
tabulated finite-height value). Track D: "a hit is a witness and needs no argument."

## Performance estimate
T=1e4: ~100k grid evals + ~274k bisection evals (mpmath 15 dps). Measured in
the [1,100] validation run, then extrapolated. Fallback: T=1e3 if too slow.
