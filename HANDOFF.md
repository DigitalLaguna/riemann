# HANDOFF
tick: 10 | 2026-08-20T17:35:00Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21 carded, all gates OPEN). Claims: #1 scaffold
NOTE; #2 PNT+ local build FORMAL; #3 NEW — track B H_0 closed form NUMERIC
(promote.sh, checker re-runs the Arb computations). Track B H_0(z) now has a
rigorous Arb closed form, verified: real axis 14 pts vs Polymath15 sample
output (~33 digits), complex z=35+10i vs independent 70-d quadrature (30+
digits, rad<=8.3e-33). Oracle trap logged: test_ht.py's 64-digit value is
the N=1-term AFE output, ~2.5% off exact H_0. Dead ends: A-001, A-002 (both
tooling). Ticks 5-9 (local model) wrote the first H_0 scripts; tick 8 entry
truncated; tick 6/9 steps=0 (empty model responses) — see log corrections.

## Last tick
Machine verdicts on the H_0 closed form (verbatim outputs in
evidence/2026-08-20-h0-closed-form/): real axis YES (14/14, ALL MATCH to 8
digits, diffs ~4e-16); complex v1 NO (ticks 5-7 script returned
0.0040110701+0i; bugs: Re[w^{ic}]=cos(c ln w) needs c real, and a
double-counted P^{-a/4} in the first fix attempt); complex v2 YES
(H_0(35+10i)=0.00032163883436158191156597555259+/-8.2e-33
+7.31922711341174159983509525e-5+/-2.02e-32 i, 30+ digit agreement).
Claim #3 promoted NOTE->NUMERIC (check.sh: CHECK OK).

## Next action
Track B step 2: H_t(z) for t>0 in Arb. The t=0 closed form used
e^{au}e^{-X e^{4u}} -> upper incomplete gamma; with e^{t u^2} the
substitution v=X e^{4u} leaves e^{t (ln(v/X))^2/16} under the integral,
so either (a) derive a parabolic-cylinder / series form and verify it
term-by-term against direct Arb/mpmath quadrature at 3-4 (z,t) points, or
(b) fall back to rigorous Arb quadrature of the defining integral
(quadgl/quad on [0,~0.8], tail bound e^{-pi e^{4u}}) as the working
implementation. Pre-registered falsification: at t in {0, 1, 100, 1000},
z = 35+10i, H_t(z) must agree between the closed form (if derived) and
direct quadrature to >= 20 digits; else method not understood. End state
this track needs for week-4 kill criterion: Lambda(t)/t_0 curve to 2 sig
figs, t_0 vs Polymath15's 2.217e4.

## Blocked
- odlyzko-zeros full text: AMS CONM 290 chapter 4573 behind LibLynx login.
  Retry: S2 search endpoint (was 429) or JSTOR.
- lean-zulip-pnt full thread: needs a Zulip API key or guest session;
  channel 423402 URL is the resolved reference meanwhile.
- apt libflint-dev/libarb-dev: pkexec prompt timed out; non-blocking —
  python-flint 0.9 bundles FLINT+ARB and all numerics go through it.
- Local model reliability: 2 of 5 timer ticks (6, 9) returned steps=0
  (empty response); tick 8 truncated its log entry. Candidate fix: make
  agent_tick.py retry once on steps=0.

## Budget
Frontier calls used this week: 1 (of 5) — this tick (bug hunt needed
independent-derivation cross-checks). Local model: qwen3.8-27b on :8080.
Weekly review due 2026-08-27 (week-1 milestone: 250 ticks, gates, PNT+
build, first claims — all met; decision point: continue/reweight/kill).
