# HANDOFF — session 2026-08-22 (tick 91, frontier)
# track: B | gate: all tracks OPEN (21/21 seeds)

## State
16 claims: 7 NUMERIC (B: #3,4,6,7,8,9; E: #10), 2 FORMAL (A: #2 PNT+ local build,
#12 IK additive-API lemmas), 7 NOTE (#1 scaffold, #5 B diag, #11 B abeff semantics,
#13 merged-into-#12, #14 B row-3 gate, #15 B Phase-3 audit, #16 B re-attribution).
WEEK-2 MILESTONE (first XS Lean issue, due 09-03): MET in substance — PNT+ issue #816
claimed: 3 API lemmas on branch ik-additive-lemmas @ 0197a66, FULL lake build exit 0
(4343 jobs, lean4 v4.32.2 + mathlib v4.32.2), no new sorries. PR filing needs owner (no gh auth).

## Last tick
tick 91 (track B): RE-ATTRIBUTION. The Phase-3 audit's (NOTE #15) "ASYMPTOTICS binding"
attribution is KILLED by its own pre-registered falsification test (tick 89). Machine
verdict (evidence/2026-08-22-f-bound-t018/check.sh, re-runnable, CHECK PASS):
  (1) tick-90 abeff re-run at t0=0.18 -> 0.532101858344813 >= 0.03 (falsification MET);
  (2) Polymath15 Table 1 FINAL |f| bound >= 0.03 in ALL 12 rows (min 0.0305, claim #8 C4);
  (3) row 2 (X=5e12, X/2=2.5e12<=3e12) is the best AVAILABLE row (Lambda=0.19999966445);
      row 3 (X=2e13, X/2=1e13>3e12, Lambda=0.1899998082) is BLOCKED by RH height.
=> BINDING CONSTRAINT = RH HEIGHT (X/2 <= 3e12, Platt-Trudgian), NOT the |f| asymptotics.
NOTE #15's own margin table had RH height (20%) tighter than asymptotics (25.3%); it
dismissed RH height as "external" — premature. NOTE #16 records the re-attribution.

## Next action
(a) OWNER: file the PNT+ PR from branch ik-additive-lemmas @ 0197a66
    (evidence/2026-08-22-pnt-ik-api/issue-816-draft.md ready; AI disclosure per
    PULL_REQUEST_STYLE.md) — closes the week-2 milestone fully.
(b) TRACK B (weight 40): run the 0.20-push pipeline (stored sums + T-loop + |f| bound)
    at a NEW X in (5e12, 6e12] (start X=6e12, N0~690618) to find a Table-1-style row with
    Lambda = t0 + y0^2/2 < 0.19999966445. Lambda is strictly decreasing in X (claim #8 C7),
    so a hit is EXPECTED if the pipeline runs clean; the table's discrete X grid skips this
    range. Pre-registered falsification test is in the tick-91 log section (winding!=0/abort
    at X=6e12, OR a valid row with Lambda >= 0.19999966445, kills "a better row exists").

## Blocked
- PNT+ PR filing (no gh/GitHub credentials on this box)
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint

## Budget
Week-1 review decision: REWEIGHT A30/B40/D15/C10/E5; condition "A claims first XS Lean issue
by 09-03" MET in substance (PR leg pending owner).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(claim #9); the PR leg is the risk.
