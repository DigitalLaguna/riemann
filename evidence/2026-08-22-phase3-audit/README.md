# Track B — Phase-3 dominant-error-term audit (tick 88, 2026-08-22 UTC)

Question: in the 0.20 bound Lambda <= t0 + y0^2/2 = 0.19999966445 (claim #9,
t0 = 0.186, y0 = 0.16733, X = 5e12+194858, N0 = 630783), which of the three
components is BINDING — (1) zero-free region for H_t, (2) asymptotics (|f| bound),
(3) zero dynamics — so B knows where to put compute?

## Prior-art pre-flight (queries + results, before the run)
- Q1: grep dbn Writeup/debruijn.tex for "bottleneck|dominant|limiting|main cost":
  line 165 (verbatim, see below) is the ONLY such statement. It says hypothesis (ii)
  (the asymptotic zero-free region at final time t0, verified via the |f| lower bound)
  is "close to the limit of our ability to numerically verify", and hypothesis (iii)
  (the barrier) "does not present the main bottleneck".
  => Prior art identifies the ASYMPTOTICS (hypothesis ii / |f| bound) as the bottleneck,
     and the barrier (hypothesis iii) as NOT the bottleneck. It does NOT give a
     per-term numeric budget. Our audit must produce that budget (machine-computed).
- Q2: grep for "t0 + y0^2/2" attribution: Theorem debr-bound (line 443) gives the
  formula Lambda <= t0 + y0^2/2 from the de Bruijn zero dynamics. The y0^2/2 term is
  the zero-dynamics contribution; the t0 term is the time parameter constrained by the
  asymptotics (|f| bound) and the zero-free region (barrier + RH height).
- Verdict: prior art (paper line 165) predicts ASYMPTOTICS is binding. The audit
  confirms or refutes this with a machine-computed per-term budget.

## Pre-registered falsification test (from tick 85 log, verbatim)
  "A hit requires a machine-computed per-term error budget (Arb) showing one term
   >= 2x the sum of the others before B commits compute to it."
  OUTCOME THAT KILLS the audit: all three components contribute comparable error and
  none is clearly binding (no term >= 2x the sum of the others).

## Method
The bound is Lambda <= t0 + y0^2/2 (exact, from Theorem debr-bound / zero dynamics).
Decompose the bound into its two additive terms and attribute each to a component:
  - t0 term (0.186): the time parameter. Driven by the ASYMPTOTICS (the |f| bound
    determines the minimum feasible t0; the barrier has a 48x margin so it is not
    binding, and the RH height has a 20% margin so it is not binding).
  - y0^2/2 term (0.01399966445): the barrier-height cost. Driven by the ZERO-FREE
    REGION (the barrier height y0) converted by the ZERO DYNAMICS (the formula).
Per-term budget (exact rational arithmetic, a superset of Arb ball arithmetic):
  - Asymptotics: t0 = 0.186
  - Zero-free region + zero dynamics: y0^2/2 = 0.01399966445
HIT iff max(term) >= 2 * (sum of the other terms).

## Machine inputs (all from archived machine outputs, claim #8/#9)
- t0 = 186/1000, y0 = 16733/100000 (exact, from check.sh of claim #9)
- |f| final bound = 0.0376 (paper Table 1 row 2, machine-checked claim #8)
- |f| target = 0.03 (paper's stated safety margin)
- T-loop min margin = 48 (threshold 1; from tloop_020_run.txt, claim #9)
- RH height: X/2 = 2.5000000974e12 <= 3e12 (Platt-Trudgian, claim #8)
