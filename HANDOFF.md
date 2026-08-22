# HANDOFF — session 2026-08-22 20:47 CEST (tick 107, local model; last frontier tick 91)
# track: B | gate: all tracks OPEN (21/21 seeds)

## State
17 claims: 7 NUMERIC (B: #3,4,6,7,8,9; E: #10), 2 FORMAL (A: #2 PNT+ local build,
#12 IK additive-API lemmas), 8 NOTE (#1 scaffold, #5 B diag, #11 B abeff semantics,
#13 merged-into-#12, #14 B row-3 gate, #15 B Phase-3 audit, #16 B re-attribution,
#17 B X=6e12 abeff argv resolved). No new claims this tick (poll only).
WEEK-2 MILESTONE (first XS Lean issue, due 09-03): MET in substance — PNT+ issue #816
claimed: 3 API lemmas on branch ik-additive-lemmas @ 0197a66, FULL lake build exit 0
(4343 jobs, lean4 v4.32.2 + mathlib v4.32.2), no new sorries. PR filing needs owner.

## Last tick
tick 107 (track B): RUN4 POLL. X=6e12 T-loop RUN4 (systemd unit tloop-x6e12-run4,
own cgroup) ALIVE at 20:42 CEST: 38min in, full core (CPU 38m16s), Memory 64.0M,
run4.txt 147456 B, Rectangle count 1186 (growing), last t ~0.022. err file 0 B,
"Abort" count 0, "Overall winding" count 0, status file start-line only.
STEADY-STATE RATE 0.62 s/rect (20s snapshot: 1154->1186). The tick-106 average
(2.2 s/rect) was inflated by slow setup (first ~130 rects took ~7 min).
RECT DENSITY (machine, matched-t): at t~0.022 run4 is at rect 1186; the verified
X=5e12 run is at rect ~359 at the same t => run4 uses ~3x the rects of the verified
run (verified total was 659). run4 has covered only ~12% of the t-range (0...0.185).
RE-ESTIMATED TOTAL ~2000-4000 rects; remaining ~800-2800 at 0.62-1.5 s/rect =>
ETA ~21:00-22:00 CEST (consistent with tick-106's 20:40-22:00; on the slower side).
Cgroup-kill diagnosis still holds (run4 survived past 20:10, where run2/run3 died).
check.sh (re-run tick 106): pass=3 fail=0 CHECK PASS — (i) RH height X/2=3e12<=3e12,
(ii) |f| bound 0.527400238236571>=0.03, Lambda=0.19899966445<0.19999966445 (exact
rational 3979993289/20000000000); (iii) T-loop winding PENDING.

## Next action
(a) TRACK B (weight 40): tick 108 (~21:13 CEST) POLL run4:
    systemctl --user status tloop-x6e12-run4 + tail evidence/2026-08-22-x6e12/tloop_x6e12_run4.txt
    On completion: tloop_x6e12_run4.status must show exit=0 AND file must contain
    "Overall winding number: 0.000000" AND no "Abort" -> NEW ROW
    Lambda=0.19899966445 < 0.19999966445 (improvement over claim #9) ->
    extend check.sh leg (iii) + promote candidate (new claim, track b).
    exit!=0 -> cgroup-kill diagnosis WRONG -> TloopSinglematv2_asan next (pre-registered).
    Still running -> log rect count + t, re-estimate, hand off (no re-launch).
(b) OWNER: file the PNT+ PR from branch ik-additive-lemmas @ 0197a66
    (evidence/2026-08-22-pnt-ik-api/issue-816-draft.md ready; AI disclosure per
    PULL_REQUEST_STYLE.md) — closes the week-2 milestone fully.

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
