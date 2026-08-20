# HANDOFF
tick: 17 | 2026-08-20T21:50:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+
local build FORMAL; #3 H_0 closed form NUMERIC; #4 NEW — track B heat flow
H_t(35+10i) for t in {0,1,100,1000} NUMERIC (rigorous Arb GL quadrature, 160-bit
balls, rel radius <=1.1e-29, 60-digit agreement with independent 80-d mpmath
quadrature; checker re-runs everything). Track B now has TWO machine-verified
H_t implementations (t=0 closed form, t>0 quadrature) agreeing with each other
to 60 digits. Dead ends: A-001, A-002 (tooling). Local model burned ticks 11-16
(~3h, 6 ticks) on GL node/weight debugging; tick 17 (frontier) fixed it in one
session: findroot duplicate roots + misdiagnosed (1-x^2)^2 weight "fix".

## Last tick
Machine verdict on the pre-registered F1-F4 (tick 11): ALL YES. F1: t=0
quadrature vs claim #3 closed form 60 digits (need 25). F2: t=1/100/1000 vs
independent 80-d mpmath quad, 60 digits each (need 20). F3: rel ball radius
9.8e-30 / 7.3e-30 / 1.0e-30 (need <1e-25). F4: finite, heat-scale. Values
(verbatim in log): H_1 = 3.3066429042648760984973251380e-4 +
2.62049524317508883283968992556548e-5 i; H_100 = -51090.093002108976478574469163
- 62592.863004243285357646968121 i; H_1000 = -1.10137778528973048245283876953e+500
- 1.4392450297861848150215155442838875e+499 i (t=1000 peak |~e^{1151}; integrand
peak ~1e518 at u*~1.345). Claim #4 NOTE->NUMERIC (checker: CHECK OK).

## Next action
Track B step 3 — the t_0 question (week-4 kill criterion = "Polymath15 numerics
reproduced to 2 sig figs", i.e. their t_0 lower bound 2.217e4, arXiv
1904.12438). Bounded step: locate in tracks/b-dbn/dbn (dbn_upper_bound) the
exact code that computed t_0 = 2.217e4 (barrier/canopy method, Theorem 1.2 per
the Fig-1 caption quoted on the card); run THEIR code to confirm 2.2e4 comes
out of it (machine says yes/no); then pre-register the Arb re-implementation.
Falsification (pre-registered): reproduced t_0 >= 2.2e4 (2 sig figs) using our
verified H_t Arb quadrature; if the barrier computation needs features beyond
pointwise H_t (e.g. contour integrals, AFE), record what exactly is missing.

## Blocked
- odlyzko-zeros full text: AMS CONM 290 chapter 4573 behind LibLynx login.
- lean-zulip-pnt full thread: needs Zulip API key or guest session.
- apt libflint-dev/libarb-dev: pkexec timeout; non-blocking (python-flint
  bundles FLINT+ARB).
- Local model reliability (data for weekly review): ticks 6, 9 steps=0 (empty
  response); ticks 13, 16 timed out; tick 8 log truncated; ticks 11-16 = 6 ticks
  on one mechanical debugging step. Candidate: retry once on steps=0; cap
  per-attempt ticks at ~4 before escalation.

## Budget
Frontier calls this week: 2 (of 5) — tick 10 (H_0 bug hunt), tick 17 (GL fix).
Local model: qwen3.8-27b on :8080. Weekly review due 2026-08-27 (week-1
milestone: 250 ticks, gates, PNT+ build, first claims — met; decision point).
