# HANDOFF — session 2026-09-16 ~20:02 UTC (tick 241)
# track: D (job status) | gate: all tracks OPEN (21/21 seeds)

## State
55 claim rows: 34 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 18 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53).
No promotions this tick (both D jobs still in flight).

## Last work
Tick 241: machine status-check of both in-flight D jobs (no new attempt;
next actions are wait/owner-dependent). Both active since the 16:25Z restart.
- mertens-1e12-promote: python at 3h34m CPU (100%, single-thread);
  promote-run.txt still empty (check.sh prints only at completion).
  ETA ~09-17 05:06Z (original 1e12 run = 12h41m per journal; re-run started
  16:25Z). Confirms the 04:00-06:00Z window.
- zero-scan-1e5: 145000/999990 (t=14500/100000), recent rate 3.04/s
  (5000 steps/1646s). ETA ~09-18 22:30Z by integral over the measured cost
  profile (mult 3.34x calibrated to measured 145000 pts/12207s). Rate is
  NON-monotonic in t: plateau ~0.155 s/call at t~44-51k (slower), then fast
  RS regime ~0.042 s/call for t>52k (faster).

## Next action
(a) TRACK D: mertens-1e12-promote.service ETA ~09-17 05:00Z. When done:
    read evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + CHECK PASS); ledger +1 NUMERIC (#39 -> NUMERIC, 35 total).
(b) TRACK D: zero-scan-1e5.service ETA ~09-18/09-20. On completion: zero list
    in full-run.txt; compute S(t) records per zero-spacing-design.md (NOTE-level,
    mpmath).
(c) TRACK C: A0_max PINNED (#54) + downstream constant NUMERIC (#55:
    1/A0_max = 2.55028364035787). Next C step: owner reports 2.55028364035787
    to ANT network, or pick a new BTY constant to re-optimize.
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816.
(e) TRACK B (weight 40): PARKED: X-sweep to 7e12; Arb-port of 0.20 pipeline
    (promotes NOTE #11); row-3 t=0.18 push BLOCKED on RH-to-1e13 source.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)
- OWNER: week-4 kill decision (09-17) pending owner call. NOTE: "machine down
  3 weeks" was wrong — machine up since Sep 2 (last reboot); ticks simply
  didn't run 08-25 -> 09-15; reboots 09-16 02:37 + 18:16 killed in-flight jobs.

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands (no weekly review ran 08-29..09-15).
D: 10 NUMERIC + 3 NOTE (#28,#37,#39; #39 promotion in flight, ETA ~09-17 05:00Z);
  in flight: mertens-1e12 promotion (ETA ~09-17 05:00Z), zero-scan (ETA
  ~09-18/09-20, rate non-monotonic in t).
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs
  #29,#41 (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned at #54 (15 digits);
  downstream constant 2.55028364035787 now NUMERIC (#55).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53; PR leg still the risk
  (owner). Next review: week-4 kill decision 09-17 — owner to decide
  continue/reweight/kill with this handoff.
