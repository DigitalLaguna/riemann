# HANDOFF — session 2026-09-18 ~05:50 UTC (tick 258)
# track: D (monitoring) | gate: all tracks OPEN (21/21 seeds)

## State
57 claim rows: 35 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43,#56; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 19 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53,#57).
This tick: no new claims (no job completed). PENDING (verified, not ledgered): none.

## Last work
Tick 258: verified all three in-flight D jobs healthy + progressing (systemd
active(running) + ckpt mtime fresh + counters advancing vs tick 257).
No reboot since 09-17 22:29Z (uptime 7:20 at 05:49Z).
- zero-scan-1e5: i_last=138944/999990 (was 133308), t≈13894/1e5 (13.9%).
  Rate 0.330 s/step — on documented mpmath cost-curve plateau (0.331).
  ETA ~09-21 ~15:00Z (in 09-21..09-24 band).
- mertens-1e12-promote: a_start=365.8e9/1e12 (was 328.1e9), maxabs=294816
  (was 222274; new in-scan record M=-294816 at x=330508686218 — below final
  331302 @ x=661066575037, which lies ahead of a_start: consistent).
  Rate 1.216e9/min stable; ETA ~14:30Z (completes today).
- robin-full-1e12: n_sub=502/9000 (was 459), best_R=0.9633611519799963
  (unchanged), best_n=107084577600. Rate 43.2 s/subseg; ETA ~09-22 ~13:00Z.
- promote-run.txt 0 bytes (stdout buffered until completion) — expected;
  ckpt actively checkpointing (mtime 05:50Z).

## Next action
(a) TRACK D: mertens-1e12-promote.service running. On completion (~09-18 ~14:30Z):
    read promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK PASS"); ledger
    #39 NOTE -> NUMERIC (36 total NUMERIC).
(b) TRACK D: zero-scan-1e5.service running. On completion (~09-21..09-24): read
    full-run.txt (summary prints to stdout only at completion); compute S(t)
    records per zero-spacing-design.md (NOTE-level, mpmath).
(c) TRACK D: robin-full-1e12.service running. On completion (~09-22 ~13:00Z): read
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
  zero-scan (i=138944/999990, ETA ~09-21 ~15:00Z), mertens-1e12 (a=365.8e9/1e12,
  ETA ~09-18 ~14:30Z), robin-full (n_sub=502/9000, ETA ~09-22 ~13:00Z) —
  all checkpointed/reboot-safe.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs
  #29,#41 (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream
  constant 2.55028364035787 NUMERIC (#55).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53,#57; PR leg still the risk
  (owner). Next review: week-4 kill decision 09-17 — owner to decide
  continue/reweight/kill with this handoff.
