# Zero-spacing / Lehmer-pair scan — design (track D)
Date: 2026-08-23T17:35Z (tick 151). Status: design + pilot pre-registered; pilot run pending.

## Scope (scoped against lit/cards/inoue-kobayashi-toma-2025.md)
Definition (paper p. 2, verbatim from lit/text/inoue-kobayashi-toma-2025.txt):
"Let 0 < γ1 ≤ γ2 ≤ · · · ≤ γn ≤ · · · denote the sequence of ordinates of the zeros of ζ in the
upper half plane. We define the normalized large/small r-gap of nontrivial zeros by
λr = lim sup (γ_{n+r} − γ_n)/(2πr/ log γ_n),  µr = lim inf (γ_{n+r} − γ_n)/(2πr/ log γ_n)."
- r = 1: g_n = (γ_{n+1} − γ_n)·log(γ_n)/(2π) = normalized consecutive gap.
- Records to log: max g_n, min g_n over the scanned range (range-scoped records; mpmath -> NOTE).
- Comparison targets (card): λ1 > 3.18 (Bui-Milinovich, under RH), µ1 < 0.515396 (Preobrazhenskii);
  Thm 2 asymptotics λr >= 1+sqrt(2/r)−..., µr <= 1−sqrt(2/r)+... (r >= 2, v2).
- Lehmer-pair detection (no zero of ζ' between a pair): v2, needs a ζ' scan.

## Method
- Z(t) = re(e^{iθ(t)} ζ(1/2+it)); θ = Riemann-Siegel asymptotic, verified vs exact to 3.8e-19
  (tick 142); residual O(t^-5) ≈ 1e-23 rad at t = 1e5, negligible at 30 dps.
- Coarse scan step 0.05 -> sign changes -> bisection to 1e-10.
- mpmath 30 dps = development tool -> NOTE, not NUMERIC (same rule as the S(t) scan).

## Pre-registered falsification tests (written BEFORE first run, tick 151)
F1: first 7 computed zeros must match the fetched Wikipedia zeta page
    (evidence/2026-08-23-st-scan/wiki-zeta.html: 14.134725, 21.022040, 25.010858, 30.424876,
    32.935062, 37.586178, 40.918719) to 6 decimals (|Δ| < 5e-7).
    Any mismatch -> θ/Z pipeline wrong -> dead until fixed.
F2: zero count in [1,1e3] must be within ±3 of the RvM main term
    (T/2π)log(T/2π) − T/2π − 1/8 = 647.50 at T = 1e3. Off by > 3 -> aliasing/pipeline error -> dead.
F3: every normalized gap g_n must lie in (0.1, 10). Any outside -> bisection/aliasing artifact -> dead.
F4: record scope: max/min g_n is a record for [1,1e3] only (later [1,1e5]). Observed max < 3.18 or
    min > 0.515396 is NOT a contradiction (limsup/liminf); observed max >= 3.18 is a notable
    data point vs Bui-Milinovich.

## Pilot
zero_scan.py 1.0 1000.0 0.05 -> expect ~647 zeros, ~8 min.
