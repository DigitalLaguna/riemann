# HANDOFF — session 2026-09-16 ~18:05 UTC (tick 237)
# track: D (job status) + intake | gate: all tracks OPEN (21/21 seeds)

## State
53 claim rows: 32 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 18 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53).

## Last work
Tick 237: TRACK D job status (both still running) + due daily arXiv sweep.
(a) arXiv math.NT sweep (export.arxiv.org, cat:math.NT, submittedDate desc,
60 entries, newest 2609.17478v1 09-15): 0 new entries vs the 16:27Z catch-up
sweep (#52; all 60 ids identical, python id-set diff); 0 escalations, 0
drops. NOTE #53. (b) mertens-1e12-promote.service active (running) 1h30m,
CPU ~100% of 1 core, promote-run.txt still empty; ETA unchanged ~09-17
04:00-06:00Z. (c) zero-scan-1e5.service active; now 120000/999990 @ 3.02/s
(old run ~5.0/s; rate declines with t as zeta eval slows). ETA slipped from
09-17 06:00Z to ~09-20 or later. Anomaly resolved: handoff's "~6.95/s" was an
overestimate, never present in the stderr data.

## Next action
(a) TRACK D: mertens-1e12-promote.service ETA ~09-17 04:00-06:00Z. When done:
    read evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + #39 promoted); ledger +1 NUMERIC (33).
(b) TRACK D: zero-scan-1e5.service now 120000/999990 @ ~3.0/s (declining);
    ETA ~09-20 or later. On completion: zero list in full-run.txt; compute
    S(t) records per zero-spacing-design.md (NOTE-level, mpmath).
(c) TRACK C optional: 50dps bisection tightening (width 4.12e-11 -> 1e-15)
    to pin A0_max to ~15 digits.
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
D: 10 NUMERIC + 3 NOTE (#28,#37,#39; #39 promotion in flight, ETA ~09-17
04:00-06:00Z); in flight: mertens-1e12 promotion, zero-scan ETA ~09-20 or
later (rate 3.0/s, declining with t).
C: 11 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51) + NOTEs #29,#41
(A0 typo),#48 (exact m=0 MARGINAL); next C step = optional tightening above.
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53; PR leg still the risk
(owner). Next review: week-4 kill decision 09-17 — owner to decide
continue/reweight/kill with this handoff.
