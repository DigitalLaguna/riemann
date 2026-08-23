# HANDOFF — session 2026-08-23 02:06 CEST (tick 117)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
21 claim rows: 10 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21), 2 FORMAL (A: #2 PNT+
local build, #12 IK additive-API lemmas), 9 NOTE (#1 scaffold, #5 B diag, #11 B abeff
semantics, #13->#12, #14 B row-3 gate, #15 B Phase-3 audit, #16 B re-attribution,
#17 B x6e12 abeff argv, #19->#18). NEW: #21 NUMERIC — Track D 2nd experiment:
Robin-criterion near-miss (n<=1e8). R(n)=sigma(n)/(e^gamma*n*log log n) max =
0.985818611972329 at n=10080 (sigma=39312); NO Robin witness (R>=1) in (5040,1e8].
Verified: full scan [5041,1e6] + superabundant/CA check (1e6,1e8] + Robin reduction.
Sequence confusion resolved: A004394=superabundant, A004490=colossally abundant;
eps-sweep generator matches A004490 exactly (13 terms <=1e8 excl 1); sigma matches
A000203 (n<=10000). checker evidence/2026-08-22-robin-ca/check.sh exit 0.

## Last tick
tick 117 (track D, 02:06 CEST): robin-ca had run (tick 112) + check.sh written
(ticks 113/115) but was UNCLAIMED (no ledger row, no log section for 113-116, HANDOFF
stale). This tick: resolved the A004394/A004490 sequence identity from fetched OEIS
html (A004394=superabundant per b-file header; A004490=colossally abundant; CA subset
of SA so SA list covers all CA; SA list complete to 1e8, largest SA<1e8=73513440),
re-ran check.sh (EXIT=0, ALL CHECKS PASS, 17.1s), added #21 NOTE and promoted
NOTE->NUMERIC (promote.sh ran the checker).

## Next action
(a) OWNER: one-click Fork of AlexKontorovich/PrimeNumberTheoremAnd -> then
    git push fork ik-additive-lemmas (branch @ 0197a66 in tracks/a-lean/pnt) + file PR
    (body ready: evidence/2026-08-22-pnt-ik-api/issue-816-draft.md, AI disclosure per
    PULL_REQUEST_STYLE.md) — closes the week-2 milestone fully.
(b) TRACK D (weight 15): third experiment — Mertens at 1e9 (pipeline exists from #20,
    just raise N) OR Robin at 1e9 (extend SA/CA b-files past 73513440 + full scan to
    1e9). Pre-register falsification tests FIRST (witness R(n)>=1 => RH false => STOP,
    constraint 5).
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
issue by 09-03" MET in substance (PR leg pending owner). D now producing (2 NUMERIC:
#20 Mertens, #21 Robin).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs +
decide B next step (X-sweep vs Arb port) + D's third experiment.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claims #7,#9,#18); the PR leg is the risk.
