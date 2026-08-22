# HANDOFF — session 2026-08-22 21:55 CEST (tick 109)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
20 claim rows: 9 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20), 2 FORMAL (A: #2 PNT+
local build, #12 IK additive-API lemmas), 9 NOTE (#1 scaffold, #5 B diag, #11 B abeff
semantics, #13->#12, #14 B row-3 gate, #15 B Phase-3 audit, #16 B re-attribution,
#17 B x6e12 abeff argv, #19->#18). NEW: #20 NUMERIC — Track D first experiment:
Mertens record at N=10^8 (max |M| = 3448, first at x=76015339; M(10^8)=1928; pipeline
cross-verified vs OEIS A002321 + A051402 envelope + independent sympy; checker
evidence/2026-08-22-mertens/check.sh exit 0). WEEK-2 MILESTONE (first XS Lean issue,
due 09-03): MET in substance — PNT+ issue #816 claimed, 3 API lemmas on branch
ik-additive-lemmas @ 0197a66, FULL lake build exit 0 (4343 jobs, lean4/mathlib v4.32.2),
no new sorries. PR filing needs owner (fork).

## Last tick
tick 109 (track D, 21:45-21:55 CEST): tick 108 had run D's first experiment (Mertens
N=10^8, all 4 pre-registered checks PASS, run.txt committed in e749f39) but left it
unclaimed (no check.sh, no ledger row, HANDOFF stale). This tick: wrote
evidence/2026-08-22-mertens/check.sh (full re-run + assert C1-C4 and record values),
checker exit 0, added #20 and promoted NOTE -> NUMERIC (machine: direct evaluation of
witnesses, exact integer arithmetic; precedent #10).

## Next action
(a) OWNER: one-click Fork of AlexKontorovich/PrimeNumberTheoremAnd -> then
    git push fork ik-additive-lemmas (branch @ 0197a66 in tracks/a-lean/pnt) + file PR
    (body ready: evidence/2026-08-22-pnt-ik-api/issue-816-draft.md, AI disclosure per
    PULL_REQUEST_STYLE.md) — closes the week-2 milestone fully.
(b) TRACK D (weight 15): second experiment — Robin-criterion near-misses over
    colossally abundant numbers. Pre-register falsification tests FIRST: (i) generated
    CA list must match fetched OEIS A004394; (ii) reduction check: max of
    R(n)=sigma(n)/(e^gamma*n*log log n) over all n<=10^6 must be attained at a CA
    number, else CA-only search is not extremal; (iii) a hit R(n)>=1 is an RH witness
    -> STOP and page owner (constraint 5). Alternative: Mertens at 10^9.
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12
    (stored sums = long pole, O(hours), isolated user unit like tloop-x6e12-run4);
    (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11); (iii) row-3 t=0.18 push
    — BLOCKED on RH-to-1e13 source (Platt-Trudgian only 3e12).
(d) Tracks A/C/E: no in-flight work; A's PR leg is the only A-critical path.

## Blocked
- PNT+ PR filing: fork not yet created (owner one-click; rest is scripted)
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 review decision: REWEIGHT A30/B40/D15/C10/E5; condition "A claims first XS Lean
issue by 09-03" MET in substance (PR leg pending owner).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs +
decide B next step (X-sweep vs Arb port) + D's second experiment.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claims #7,#9,#18); the PR leg is the risk.
