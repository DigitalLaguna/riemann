# HANDOFF — session 2026-08-23 05:40 UTC (manual, after tick 125; owner online)
# track: A | gate: all tracks OPEN (21/21 seeds)

## State
25 claim rows: 13 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24), 3 FORMAL
(A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK lemmas v2),
9 NOTE (#1, #5, #11, #13->#12, #14, #15, #16, #17, #19->#18). NEW: #25 FORMAL —
owner's pre-PR review objections all resolved and machine-verified: (1) lemma 3
WAS VACUOUS — original `hpos : ∀ n, 0 < f n` unsatisfiable (f 0 = 0 for any
ArithmeticFunction; machine-proved False, evidence/2026-08-23-pnt-ik-api-revision/
vacuity-check.{lean,txt}); fixed to `∀ n ≠ 0`. (2) map_one/map_prime_pow context
weakened AddGroupWithOne -> AddCancelMonoid (first try AddMonoid for map_prime_pow
FAILED build — no cancellation; caught by compile-fail-retry). (3) renamed to
ArithmeticFunction.IsMultiplicative.isAdditive_log (dot-notation). (4) rebased onto
current main 751a8c2. Branch v2 @ 67661ab, 41 added lines, FULL lake build 4343 jobs
exit 0, sorry 7 = 7, force-pushed to fork, CHECK PASS via new check.sh.

## Last work
Owner reviewed staged PR body (04:40 UTC), raised 3 substantive + 2 housekeeping
objections; manual session resolved all against the machine (vacuity check, 2
build attempts, full build), booked #25, added HARD CONSTRAINT 7 to the operating
contract + design doc sec 4: "An unexplained mismatch blocks; it does not annotate"
(tick-72 shape: the v1 docstring/PR text documented the AddGroupWithOne anomaly
instead of resolving it). PR sheet rev 2: evidence/2026-08-22-pnt-ik-api/pr-body.md.

## Next action
(a) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: pr-body.md rev 2), then comment `propose #<PR>` on issue #816.
    CAVEAT (workflow, per CONTRIBUTING): #816 is ASSIGNED to IlPreteRosso since
    2026-01-28 (last note 2026-02-04 "Waiting for Mathlib..."); `propose` only
    moves the task if the proposer holds the claim -> ping @IlPreteRosso on #816
    (claim ~7 months stale) or wait for disclaim (options in pr-body.md).
(b) TRACK D (weight 15): sixth experiment — Robin full-scan [1e8,1e9] (needs
    segmented/faster sigma sieve; naive numpy ~30 min) OR S(t) scan.
    Pre-register falsification FIRST (witness => RH false => STOP, c5).
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12
    (stored sums = long pole); (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11);
    (iii) row-3 t=0.18 push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(d) Tracks A/C/E: A waits on the PR (its only critical path); C/E no in-flight work.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner;
  #816 claimant (IlPreteRosso) contact per CONTRIBUTING (see (a))
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands; "A claims first XS Lean issue by 09-03"
MET in substance (claim #25 FORMAL, review objections resolved pre-PR; PR leg = one
owner click). D 5 NUMERIC (#20-#24). Next review 2026-08-29 (week 2): milestone
check + spot-check 3 cards vs PDFs + decide B next step + D sixth experiment.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claims #7,#9,#18); the PR leg is still the risk.
