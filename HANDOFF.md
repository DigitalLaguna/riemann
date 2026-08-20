# HANDOFF
tick: 4 | 2026-08-20T17:12:00Z | track: all (carding) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE: all 21 seeds across tracks A-E fetched, carded with
verbatim quotes (card.py: 21 OK), all five gates flipped OPEN via gate.py.
Claims: #1 scaffold NOTE; #2 PNT+ local build FORMAL (promote.sh). PNT+ clone at
tracks/a-lean/pnt builds (4343 jobs). Dead ends logged: A-001 (gate.py keyword
paren), A-002 (binary-as-text crash killed tick 3). Known gaps: odlyzko-zeros
full chapter text behind AMS login; lean-zulip-pnt full thread behind Zulip JS
UI (both carded from landing/README docs, full text PENDING).

## Last tick
Carded the final seeds (conrey-2003, odlyzko-zeros, broughan-2017,
lean-zulip-pnt; D/E cards done earlier in the session). Machine said:
card.py OK x21; gate.py status: 21/21 PASS, tracks A-E OPEN. Two design-doc
errors found and recorded on the cards: Conrey article is in the MARCH 2003
Notices issue at pp. 341-353 (not 244-256); Broughan's book is actually
"Equivalents of the Riemann Hypothesis" by Kevin Broughan, Cambridge UP 2017.

## Next action
First real work on an open track — track B: re-implement Polymath15 heat-flow
numerics (Arb, per lit/cards/dbn-code.md conventions) to 2 significant
figures; week-4 kill criterion = "Polymath15 numerics reproduced to 2 sig figs"
so start it now. Pre-registered falsification: reproduced Lambda(t) curve
agrees with arXiv 1904.12438 Fig. 1 to 2 sig figs on t in [0, 10^4], else
method not understood (kill track B per week-4 criterion).
Env ready (probed this tick, verbatim output in log): python-flint 0.9,
flint.ctx.prec=N; acb.zeta(0.5+12.9113i) returns a complex ball with explicit
radius (~1e-24 at 80 bits). Note: 2nd arb() constructor arg is the RADIUS.

## Blocked
- odlyzko-zeros full text: AMS CONM 290 chapter 4573 behind LibLynx login.
  Retry: S2 search endpoint (was 429) or JSTOR.
- lean-zulip-pnt full thread: needs a Zulip API key or guest session;
  channel 423402 URL is the resolved reference meanwhile.
- apt libflint-dev/libarb-dev: pkexec prompt timed out (90s, no human at
  machine); non-blocking — python-flint 0.9 bundles its own FLINT+ARB and
  all numerics go through it (probe in log).

## Budget
Frontier calls used this week: 0 (of the 5 escalation triggers).
Local model: qwen3.8-27b on :8080 (tick 3 crashed on a PNG-as-text read;
fixed by keeping binaries out of `read`). Weekly review due 2026-08-27.
