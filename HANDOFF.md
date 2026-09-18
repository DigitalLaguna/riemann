# HANDOFF — session 2026-09-18 ~17:45 UTC (tick 262)
# track: C (new-attempt setup) + D (monitoring) | gate: all tracks OPEN (21/21 seeds)

## State
57 claim rows: 35 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43,#56; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 19 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53,#57).
This tick: no new claims (no job completed). PENDING: none.

## Last work
Tick 262: (a) verified all 3 in-flight D jobs healthy + progressing (4th monitor tick).
No reboot/suspend since 15:54Z. All ckpts actively checkpointing (mtimes 17:32Z).
- zero-scan-1e5: i_last=156370/999990 (was 150791), ~0.333 s/step (plateau). ETA ~09-21..09-22.
- mertens-1e12-promote: a_start=484.5e9/1e12 (was 446.2e9), maxabs=294816 (unchanged;
  final 331302 @ x=661e9 still ahead). ~1.24e9/min. ETA ~09-19 00:45Z.
- robin-full-1e12: n_sub=634/9000 (was 592), NEW best_R=0.9755059227362325 at
  n=160626866400 (was 0.9633611519799963) — equals SA_REF 0.975505922736 (superabundant n).
  ~44.5 s/subseg. ETA ~09-22..09-23.
(b) TRACK C new-attempt setup: read BTY constant list; prior-art pre-flight (3 arXiv
queries, logged); 4.8594 (Thm2/Lem2) recorded as DEAD END C-001 (blocked by unobtainable
thesis [16]); PICKED kappa_m/M (trig poly (17)/(18)) re-optimization; falsification test
pre-registered (dead if reopt A_final still > A0_max = 0.392113247395366294).

## Next action
(a) TRACK C (tick 263): set up kappa_m L-infinity minimization (Remez/LP) for M=6;
    FIRST verify we reproduce the paper's A_final = 0.420483467794 with the paper's
    kappa_m (reproduction gate); then re-optimize. Machine: solver + Arb.
(b) TRACK D: mertens-1e12-promote.service running. On completion (~09-19 ~00:45Z):
    read promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK PASS"); ledger
    #39 NOTE -> NUMERIC (36 total NUMERIC).
(c) TRACK D: zero-scan-1e5.service running. On completion (~09-21..09-22): read
    full-run.txt; compute S(t) records per zero-spacing-design.md (NOTE-level, mpmath).
(d) TRACK D: robin-full-1e12.service running. On completion (~09-22..09-23): read
    full-run-resume.txt (expect "VERDICT: ALL CHECKS PASS"); new D NUMERIC (full scan
    [1e11,1e12), SA_REF 0.975505922736).
(e) If any job is dead (reboot OR S3 suspend — check journal gap + ckpt mtimes): it
    RESUMES from its ckpt (no blind relaunch). Verify ckpt is valid JSON before resuming.
    Relaunch commands in logs/2026-09-18.tick.log TICK 259.
(f) OWNER: (1) open PNT+ PR (evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2) + comment
    `propose #<PR>` on issue #816; (2) week-4 kill decision (09-17) pending; (3)
    2609.20367v1 claimed-RH preprint — owner decides if frontier-escalated adversarial
    read warranted (I will not build on it).

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner.
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest (carded);
  odlyzko zero-data page 404 -> zero scan computes zeros itself.
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint.
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12).
- BTY 4.8594 (Thm2/Lem2): blocked by unobtainable thesis [16] (DEAD END C-001).
- OWNER: week-4 kill decision (09-17) pending. Reboots/suspends frequent, but all long
  jobs now checkpointed (ticks 244/246/247/248) -> reboot-safe.

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands (no weekly review ran 08-29..09-15).
D: 11 NUMERIC + 3 NOTE (#28,#37,#39; #39 promotion in flight); in flight:
  zero-scan (i=156370/999990, ETA ~09-21..09-22), mertens-1e12 (a=484.5e9/1e12,
  ETA ~09-19 00:45Z), robin-full (n_sub=634/9000, ETA ~09-22..09-23) — all
  checkpointed/reboot-safe.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs #29,#41
  (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream constant
  2.55028364035787 NUMERIC (#55). 4.8594 dead (C-001). Next: kappa_m/M re-optimize
  (reproduce A_final=0.420483467794 first).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53,#57; PR leg still the risk (owner).
Next review: week-4 kill decision 09-17 — owner to decide continue/reweight/kill.
