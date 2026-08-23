# HANDOFF — session 2026-08-23 00:55 UTC (tick 118)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
22 claim rows: 11 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22), 2 FORMAL
(A: #2 PNT+ local build, #12 IK additive-API lemmas), 9 NOTE (#1 scaffold, #5 B diag,
#11 B abeff semantics, #13->#12, #14 B row-3 gate, #15 B Phase-3 audit, #16 B
re-attribution, #17 B x6e12 abeff argv, #19->#18). NEW: #22 NUMERIC — Track D 3rd
experiment: Mertens record at 1e9. max_{x<=1e9} |M(x)| = 10246, first at x=903087703
(M=+10246, positive side); M(1e9) = -222 = OEIS A084237 a(9); A051402 inverse-Mertens
envelope k=1..10000 fully verified; |M(x)|<=sqrt(x) holds at 1e9 (Mertens conjecture
still holds; known counterexample ~1.05e11). checker evidence/2026-08-23-mertens-1e9/
check.sh exit 0.

## Last tick
tick 118 (track D, 00:55 UTC): D's 3rd experiment — Mertens at 1e9. Refactored
tracks/d-search/mertens_extremal.py (N via argv, default 1e8; chunked ratio for
memory); F1 regression byte-identical to claim #20's run.txt (21.6s). Prior art:
OEIS A084237 (a(n)=M(10^n), a(9)=-222; a(1..8) match our 1e8 run exactly), A051402
(b-file k<=10000, a(10000)=902718903<1e9 => record >=10000 forced); no published
max |M| at 1e9 found (queries logged). Pre-registered F1-F5; run 2m23s EXIT=0 all
PASS; check.sh EXIT=0; #22 NOTE->NUMERIC.

## Next action
(a) OWNER: one-click Fork of AlexKontorovich/PrimeNumberTheoremAnd -> then
    git push fork ik-additive-lemmas (branch @ 0197a66 in tracks/a-lean/pnt) + file PR
    (body ready: evidence/2026-08-22-pnt-ik-api/issue-816-draft.md, AI disclosure per
    PULL_REQUEST_STYLE.md) — closes the week-2 milestone fully.
(b) TRACK D (weight 15): fourth experiment — Robin at 1e9 (extend SA/CA b-files past
    73513440; next SA = 122522400; full scan [1e8,1e9] is the long pole) OR Mertens at
    1e10 (memory ~100GB vs 111GB available — tight; consider segmented variant).
    Pre-register falsification tests FIRST (witness R(n)>=1 => RH false => STOP,
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
issue by 09-03" MET in substance (PR leg pending owner). D now producing (3 NUMERIC:
#20 Mertens 1e8, #21 Robin 1e8, #22 Mertens 1e9).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs +
decide B next step (X-sweep vs Arb port) + D's fourth experiment.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claims #7,#9,#18); the PR leg is the risk.
