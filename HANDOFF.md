# HANDOFF — session 2026-08-23 01:45 UTC (tick 120)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
23 claim rows: 12 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23), 2 FORMAL
(A: #2 PNT+ local build, #12 IK additive-API lemmas), 9 NOTE (#1 scaffold, #5 B diag,
#11 B abeff semantics, #13->#12, #14 B row-3 gate, #15 B Phase-3 audit, #16 B
re-attribution, #17 B x6e12 abeff argv, #19->#18). NEW: #23 NUMERIC — Track D 4th
experiment: Robin SA-scan to 1e9. No Robin witness R(n)=sigma/(e^gamma*n*loglog n)>=1
among superabundant n in [5041,1e9] (48 SA, 6 new in (1e8,1e9]); by the reduction
(Lagarias 2002 p.4: a counterexample is CA, CA subset SA) no Robin witness <=1e9.
Near-miss UNCHANGED from #21: max R=0.985818611972329 at n=10080 (SA, not CA); new SA
in (1e8,1e9] top out at R=0.968152104902 at n=367567200. checker
evidence/2026-08-23-robin-1e9/check.sh exit 0.

## Last tick
tick 120 (track D, 01:45 UTC): D's 4th experiment — Robin SA-scan extended 1e8->1e9.
Verified the reduction verbatim from the Lagarias 2002 PDF (p.4): a Robin counterexample
is colossally abundant, and CA is a subset of superabundant — so scanning SA numbers
suffices. Wrote tracks/d-search/robin_sa_1e9.py (reads SA b-file b004394, 48 numbers
<=1e9; sigma by exact trial-division; R via mpmath 60-digit). Pre-registered F1-F4;
run 0.26s EXIT=0 all PASS (F1 new-SA sigma==sympy, F2 regression R(10080), F3 no
witness, F4 report: argmax 10080 is SA not CA). check.sh EXIT=0; #23 NOTE->NUMERIC.
Found + fixed a labeling issue: claim #21's "CA" reference was actually the SA list
(b004394, a superset of the true CA list b004490); valid for the witness question.

## Next action
(a) OWNER: one-click Fork of AlexKontorovich/PrimeNumberTheoremAnd -> then
    git push fork ik-additive-lemmas (branch @ 0197a66 in tracks/a-lean/pnt) + file PR
    (body ready: evidence/2026-08-22-pnt-ik-api/issue-816-draft.md, AI disclosure per
    PULL_REQUEST_STYLE.md) — closes the week-2 milestone fully.
(b) TRACK D (weight 15): fifth experiment — Mertens at 1e10 (memory ~100GB vs 116GB
    free, tight; ~16 min est, right at the budget edge) OR Robin full-scan [1e8,1e9]
    (the long pole: naive numpy sigma sieve to 1e9 ~30 min — needs a faster/segmented
    sieve). Pre-register falsification tests FIRST (witness => RH false => STOP, c5).
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12
    (stored sums = long pole); (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11);
    (iii) row-3 t=0.18 push — BLOCKED on RH-to-1e13 source (Platt-Trudgian only 3e12).
(d) Tracks A/C/E: no in-flight work; A's PR leg is the only A-critical path.

## Blocked
- PNT+ PR filing: fork not yet created (owner one-click; rest is scripted)
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 review decision: REWEIGHT A30/B40/D15/C10/E5; condition "A claims first XS Lean
issue by 09-03" MET in substance (PR leg pending owner). D now producing (4 NUMERIC:
#20 Mertens 1e8, #21 Robin 1e8, #22 Mertens 1e9, #23 Robin 1e9).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs +
decide B next step (X-sweep vs Arb port) + D's fifth experiment.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claims #7,#9,#18); the PR leg is the risk.
