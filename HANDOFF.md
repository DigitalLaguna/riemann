# HANDOFF — session 2026-09-18 ~03:15 UTC (tick 253)
# track: D (monitoring) | gate: all tracks OPEN (21/21 seeds)

## State
57 claim rows: 35 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43,#56; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 19 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53,#57).
This tick: no new claims (no job completed). PENDING (verified, not ledgered): none.

## Last work
Tick 253: verified all three in-flight D jobs healthy + progressing + reboot-safe
(systemd active(running) + ckpt mtime <1min + counter advancing vs tick 252).
- zero-scan-1e5: i_last=110822/999990 (was 103123), t≈11083/1e5 (11%), 11424 zeros.
- mertens-1e12-promote: a_start=175.6e9/1e12 (was 139.7e9), maxabs-so-far=170358
  (record at x=108.9e9, matches original 08-24 trajectory).
- robin-full-1e12: n_sub=287/9000 (was 243), best_R=0.9633611519799963 (unchanged).
Reboot/restart audit (journalctl): every mertens stop/start is a reboot
(boot -2 end 09-16 00:37Z, boot -1 end 09-16 21:15Z) + one external restart
09-18 00:51Z; current boot since 22:29Z (09-17), uptime 4h48m. Each resumed
cleanly from the atomic ckpt (a_start only advances) -> no progress lost.
Mertens ETA slipped 13:37Z -> ~16:00Z (00:51Z restart gap + reboot pattern);
still completes today. Zero-scan ETA ~09-20, robin ETA ~09-22 (unchanged).

## Next action
(a) TRACK D: zero-scan-1e5.service running. On completion (~09-20): read
    full-run.txt (summary prints to stdout only at completion); compute S(t)
    records per zero-spacing-design.md (NOTE-level, mpmath).
(b) TRACK D: mertens-1e12-promote.service running. On completion (~09-18 ~16:00Z):
    read promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK PASS"); ledger
    #39 NOTE -> NUMERIC (36 total).
(c) TRACK D: robin-full-1e12.service running. On completion (~09-22 12:14Z): read
    full-run-resume.txt (expect "VERDICT: ALL CHECKS PASS"); new D NUMERIC (full
    scan [1e11,1e12), SA_REF 0.975505922736).
(d) If any job is killed by a reboot: it RESUMES from its ckpt (no blind
    relaunch). Verify ckpt is valid JSON before resuming.
(e) TRACK C: owner reports 2.55028364035787 to ANT network, or pick a new BTY
    constant to re-optimize.
(f) OWNER: (1) open PNT+ PR (evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2)
    + comment `propose #<PR>` on issue #816; (2) week-4 kill decision (09-17)
    pending; (3) 2609.20367v1 claimed-RH preprint — owner decides if a
    frontier-escalated adversarial read is warranted (I will not build on it).

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner.
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest (carded);
  odlyzko zero-data page 404 -> zero scan computes zeros itself.
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint.
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12).
- OWNER: week-4 kill decision (09-17) pending. Reboots frequent, but all long
  jobs now checkpointed (ticks 244/246/247/248) -> reboot-safe.

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands (no weekly review ran 08-29..09-15).
D: 11 NUMERIC + 3 NOTE (#28,#37,#39; #39 promotion in flight); in flight:
  zero-scan (i=110822/999990, ETA ~09-20), mertens-1e12 (a=175.6e9/1e12,
  ETA ~09-18 ~16:00Z), robin-full (n_sub=287/9000, ETA ~09-22 12:14Z) —
  all checkpointed/reboot-safe.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs
  #29,#41 (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream
  constant 2.55028364035787 NUMERIC (#55).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53,#57; PR leg still the risk
  (owner). Next review: week-4 kill decision 09-17 — owner to decide
  continue/reweight/kill with this handoff.
