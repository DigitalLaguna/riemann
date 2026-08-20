# Riemann research operator

A 24/7 agent project working on the Riemann Hypothesis and adjacent open
problems, run by a local model (qwen3.8-27b via llama-server on :8080) with
frontier escalation on defined triggers.

Design document (the source of truth): `~/riemann-agent-plot.md`
Operating contract (its Section 4, verbatim): `tools/prompt.md`

## The one rule

The agent may only produce artifacts a machine can judge: a Lean 4 proof
(compiler), rigorous numeric with interval/ball arithmetic (error bound), or
an explicit counterexample/witness (direct evaluation). Anything else is a
NOTE, never a result. Claims live in `ledger/claims.db`; status is raised
only by `tools/promote.sh` running a checker, never by the model asserting.

## Layout (fixed — no new top-level directories)

- `HANDOFF.md` — rewritten every tick, <80 lines, the control surface
- `DEAD_ENDS.md` — append-only, read before every new attempt
- `ledger/claims.db` — claim ledger, single source of truth on status
- `lit/{pdf,text,cards,reading}` — fetched papers, cards, per-track seed lists
- `tracks/{a-lean,b-dbn,c-constants,d-search,e-rh}` — per-track work
- `evidence/` — append-only, one dir per verified run, each with a check.sh
- `logs/` — append-only daily logs and ticks.log
- `tools/` — tick.sh, agent_tick.py, promote.sh, card.py, gate.py, prompt.md

## The loop

`riemann-tick.timer` (systemd user timer) fires `tools/tick.sh` every 30
minutes. Each tick is one bounded unit of work following the 7-step loop in
`tools/prompt.md`, committing its own result. A tick never ends with a dirty
tree.

## Tracks (weights)

A 40% Lean formalization (PNT+/ANT network) · B 30% de Bruijn-Newman upper
bound · C 15% explicit constant re-optimization · D 10% background witness
search · E 5% RH itself (one pre-registered attempt/week, frontier).

A track stays CLOSED until its seed reading list is fully carded; the gate
flips only via `tools/gate.py flip <track>`.

## For the owner (weekly check-in)

Run `python3 tools/gate.py status`, `tools/promote.sh list`, read the
one-page weekly review in `logs/`. Milestones and kill criteria are in the
design document, Section 7. Spot-check three random cards against their PDFs
at week 2 — that is the only human verification the system requires.

## Environment notes

- Bootstrap per design doc Section 5; adapted: python-flint 0.9.0 installed
  as a manylinux wheel (bundles FLINT incl. arb), so `apt libflint-dev`
  was not needed. Systemd units are user-level (`~/.config/systemd/user/
  riemann-tick.{service,timer}`), equivalent to the doc's system-level
  example without sudo.
- `tracks/a-lean/pnt` is the PNT+ clone (nested git repo, gitignored here).
- Escalation triggers and budget are in HANDOFF.md and the operating contract.
