# HANDOFF — session 2026-08-23 04:30 UTC (manual, after tick 125; owner online)
# track: A | gate: all tracks OPEN (21/21 seeds)

## State
24 claim rows: 13 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24), 2 FORMAL
(A: #2 PNT+ local build, #12 IK additive-API lemmas), 9 NOTE (#1, #5, #11, #13->#12,
#14, #15, #16, #17, #19->#18). NEW: #24 NUMERIC — D 5th experiment: Mertens record at
N=1e10: max |M(x)| = 50286 first at x=7766842813; M(1e10) = -33722 (= OEIS A084237
a(10)); |M(x)| <= sqrt(x) holds to 1e10. check.sh exit 0
(evidence/2026-08-23-mertens-1e10). TRACK A: owner forked PNT+ ->
DigitalLaguna/PrimeNumberTheoremAnd; branch ik-additive-lemmas @ 0197a66 (claim #12)
pushed to fork, SHA verified via GitHub API; PR sheet staged.

## Last work
tick 125 (D, 03:59 UTC): completed the N=1e10 Mertens cycle — check.sh re-run
reproduced run.txt exactly (G1), M(10^k) k=1..10 = OEIS A084237 a(1)..a(10) (G2),
claim #24 NOTE->NUMERIC via checker. Manual session 04:05-04:30 (A): push branch to
owner's fork (clean: 2 new upstream commits touch only FKS2 files, no overlap),
staged evidence/2026-08-22-pnt-ik-api/pr-body.md (title + body + AI disclosure per
PULL_REQUEST_STYLE.md sec 13.1 + issue-#816 situation).

## Next action
(a) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md), then comment
    `propose #<PR>` on issue #816 (CONTRIBUTING step 4) — closes week-2 milestone.
    CAVEAT: #816 is assigned to IlPreteRosso since 2026-01-28 (last note 2026-02-04
    "Waiting for Mathlib to merge relevant code"); CONTRIBUTING add. guideline 1 says
    contact the claimant first — ping on the issue or wait for disclaim (owner call,
    options in pr-body.md).
(b) TRACK D (weight 15): sixth experiment — Robin full-scan [1e8,1e9] (long pole:
    needs segmented/faster sigma sieve; naive numpy ~30 min) OR S(t) scan.
    Pre-register falsification FIRST (witness => RH false => STOP, c5).
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12
    (stored sums = long pole); (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11);
    (iii) row-3 t=0.18 push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(d) Tracks A/C/E: A waits on the PR (its only critical path); C/E no in-flight work.

## Blocked
- PNT+ PR: fork+push DONE; PR form + `propose #N` on #816 need owner; #816 claimant
  (IlPreteRosso, 2026-01-28) needs contact per CONTRIBUTING (see (a))
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands; condition "A claims first XS Lean issue
by 09-03" MET in substance (claim #12 FORMAL; PR leg = one owner click). D now 5
NUMERIC (#20-#24). Next review 2026-08-29 (week 2): milestone check + spot-check 3
cards vs PDFs + decide B next step + D sixth experiment.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claims #7,#9,#18); the PR leg is still the risk.
