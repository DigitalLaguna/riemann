# HANDOFF — session 2026-09-16 ~18:40 UTC (tick 234)
# track: D (jobs relaunched) | gate: all tracks OPEN (21/21 seeds)

## State
52 claim rows: 32 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 17 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52).

## Last work
Tick 234: TRACK D — both in-flight jobs found DEAD (reboot 09-16 02:37 killed
the transient units; second reboot 18:16 = current boot). Relaunched both as
systemd-run --user units (A-005): zero-scan-1e5 resumed from ckpt i=107955
(11083 zeros); mertens-1e12-promote full re-run (no ckpt, ~10-12h). Machine
verified: both "active (running)" + "resuming from i=107955" + both python
procs at ~100% CPU. Also: arXiv catch-up sweep 08-24 -> 09-16 (60 entries,
newest 09-15): 0 escalations, 5 drops with reasons, NOTE #52.

## Next action
(a) TRACK D: mertens-1e12-promote.service ETA ~09-17 04:00-06:00Z. When done:
    read evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + #39 promoted); ledger +1 NUMERIC (33).
(b) TRACK D: zero-scan-1e5.service at 107955/999990 @ ~6.95/s; ETA ~09-17
    06:00Z. On completion: zero list in full-run.txt; compute S(t) records
    per zero-spacing-design.md (NOTE-level, mpmath).
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
D: 10 NUMERIC + #39 NOTE (promotion in flight, ETA ~09-17 04:00-06:00Z) + 4 NOTE
(#28,#37,#48,#52); in flight: mertens-1e12 promotion, zero-scan ETA ~09-17 06:00Z.
C: 11 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51) + #41 NOTE (A0 typo)
+ #48 NOTE (exact m=0 MARGINAL); next C step = optional tightening above.
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25); PR leg still the risk (owner). Next review: week-4
kill decision 09-17 — owner to decide continue/reweight/kill with this handoff.
