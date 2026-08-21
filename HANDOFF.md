# HANDOFF
tick: 39 | 2026-08-21T08:04:29Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ local build
FORMAL; #3 H_0 closed form NUMERIC; #4 H_t(35+10i) t in {0,1,100,1000} NUMERIC (rigorous Arb GL
quadrature); #5 NEW NOTE — barrier diagnostic: our GL quadrature (n=32/64) does NOT converge at
the Polymath15 barrier point X0=6e10+83951.5+0.2i (degree-diff rel 0.227 vs 4.3e-39 at reference
z=35+10i). Dead ends: A-001, A-002 (tooling), B-001 (GL quadrature does not reach the barrier).

## Last tick
Machine verdict on the pre-registered falsification (tick 39): TRIGGERED. Ran the built-but-unrun
ht_barrier_test.py (local model built tick 32, fixed tick 38, never ran it). Degree-difference
n=32 vs n=64 at t=0.2: reference z=35+10i rel 4.3e-39 (converges); moderate z=1000+0.2i rel 2.48;
barrier X0+0.2i rel 0.227. VERDICT: barrier rel radius LARGE — quadrature does NOT converge; AFE
or the Polymath15 C code is needed to reproduce t_0=2.217e4. Root cause: integrand cos(z*u)
oscillates with period ~1e-10 in u at X0~6e10; GL n=32/64 (node spacing ~0.03) aliases it. Full
verbatim output at evidence/2026-08-21-ht-barrier/machine-run.txt.

## Next action
Track B step 3 — the t_0 question (week-4 kill criterion = "Polymath15 numerics reproduced to 2
sig figs", i.e. their t_0 lower bound 2.217e4, arXiv 1904.12438). Two candidate paths, pick one:
  (a) C-code path (literal HANDOFF plan, cheaper): locate + run the Polymath15 C code
      (dbn_upper_bound/arb/BarrierLocationAssistant.c or the barrier-t-loop scripts) to confirm
      t_0=2.2e4 comes out. Needs FLINT/Arb C dev headers (apt libflint-dev/libarb-dev was blocked
      by pkexec; python-flint bundles FLINT+ARB but the C scripts need the dev headers).
  (b) AFE path (more work, our own verified barrier eval): implement the Approximate Functional
      Equation to extend our quadrature to the barrier region.
First bounded step either way: verify the barrier point X0=6e10+83951.5 against the
polymath15-2019 card (the local model's docstring value, not yet re-checked against the fetched
paper). Falsification (pre-registered): reproduced t_0 >= 2.2e4 (2 sig figs); if the barrier
computation needs features beyond pointwise H_t (AFE, contour integrals), record exactly what is
missing.

## Blocked
- odlyzko-zeros full text: AMS CONM 290 chapter 4573 behind LibLynx login.
- lean-zulip-pnt full thread: needs Zulip API key or guest session.
- apt libflint-dev/libarb-dev: pkexec timeout; blocks the C-code path (a) unless python-flint's
  bundled headers suffice.
- Local model reliability (data for weekly review): ticks 18-38 (16 ticks, ~7h) all wrote the same
  "next" action and only appended to ticks.log — built ht_barrier_test.py (tick 32) but never ran
  it. Candidate: cap per-attempt ticks at ~4 before escalation; require a machine-yes/no or a
  logged dead end per tick.

## Budget
Frontier calls this week: 2 confirmed (tick 10 H_0 bug hunt, tick 17 GL fix) + this tick 39 if
escalated = 3 (of 5). Local model: qwen3.8-27b on :8080. Weekly review due 2026-08-27 (week-1
milestone met; decision point on track B path a vs b).
