# HANDOFF — session 2026-09-18 ~19:15 UTC (tick 265)
# track: C (kappa_m re-opt) + D (monitoring) | gate: all tracks OPEN (21/21 seeds)

## State
57 claim rows: 35 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43,#56; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 19 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53,#57).
This tick: no new claims (setup step, no job completed). PENDING: none.

## Last work
Tick 265: (a) D monitor: all 3 jobs active since 16:06:47Z, no reboot
(uptime==wall), ckpt mtimes fresh ~19:05Z. zero-scan i~156k/999990 (ETA
~09-21..09-22); mertens a=330.5e9/1e12 maxabs=294816 (ETA ~09-19 00:45Z);
robin n_sub=763/9000 best_R=0.9755059227362325 @160626866400 (=SA_REF,
superabundant) (ETA ~09-22..09-23).
(b) TRACK C kappa_m re-opt (bounded step): verified all constants verbatim vs
BTY text; established A_final depends on kappa_m ONLY via kappa=sum kappa_m
(corrected denom a*kappa^2*w(0)/2, #38). Wrote kappa-reopt.py (mpmath 60 dps).
  REPRODUCTION GATE PASS: A_final(paper kappa=433/859)=0.420483467793734
  (target #40 0.420483467794, |diff| 2.66e-13).
  THRESHOLD: need kappa > 0.521015891482995 (paper 0.50407450523865, +3.361%)
  for A_final < A0_max=0.392113247395366294. Self-consistent (A_final(kappa_req)=A0_max).
  Evidence: evidence/2026-09-18-zfree-kappa-reopt/.

## Next action
(a) TRACK C (tick 266): extract BTY constraints on kappa_m and solve
    max kappa = sum kappa_m s.t. (C1) p(x)=sum kappa_m x^m > 0 for 0<x<=1
    (Lemma 3); (C2) B(y)>=0 all y in R (line 696); (C3) lemma 5-14 bounds
    (L-infinity approx quality). If max kappa < 0.521015891482995 -> DEAD
    (record C-002 in DEAD_ENDS). Else re-optimize + re-verify lemmas 5-14.
(b) TRACK D: mertens-1e12-promote.service running. On completion (~09-19
    00:45Z): read promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK
    PASS"); ledger #39 NOTE -> NUMERIC (36 total NUMERIC).
(c) TRACK D: zero-scan-1e5.service running. On completion (~09-21..09-22):
    read full-run.txt; compute S(t) records per zero-spacing-design.md (NOTE).
(d) TRACK D: robin-full-1e12.service running. On completion (~09-22..09-23):
    read full-run-resume.txt (expect "VERDICT: ALL CHECKS PASS"); new D NUMERIC.
(e) If any job dead (reboot OR S3 suspend — journal gap + stale ckpt mtimes):
    it RESUMES from ckpt (no blind relaunch). Verify ckpt valid JSON first.
    Relaunch commands in logs/2026-09-18.tick.log TICK 259.
(f) OWNER: (1) open PNT+ PR (evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2)
    + comment `propose #<PR>` on issue #816; (2) week-4 kill decision (09-17)
    pending; (3) 2609.20367v1 claimed-RH preprint — owner decides on
    frontier-escalated adversarial read (I will not build on it).

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner.
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest (carded);
  odlyzko zero-data page 404 -> zero scan computes zeros itself.
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint.
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12).
- BTY 4.8594 (Thm2/Lem2): blocked by unobtainable thesis [16] (DEAD END C-001).
- OWNER: week-4 kill decision (09-17) pending. Reboots/suspends frequent, but
  all long jobs checkpointed (ticks 244/246/247/248) -> reboot-safe.

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands (no weekly review ran 08-29..09-15).
D: 11 NUMERIC + 3 NOTE (#28,#37,#39; #39 promotion in flight); in flight:
  zero-scan (i~156k/999990, ETA ~09-21..09-22), mertens-1e12 (a=330.5e9/1e12,
  ETA ~09-19 00:45Z), robin-full (n_sub=763/9000, ETA ~09-22..09-23) — all
  checkpointed/reboot-safe.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs #29,#41
  (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream constant
  2.55028364035787 NUMERIC (#55). 4.8594 dead (C-001). kappa_m re-opt: gate PASS,
  threshold kappa>0.521015891482995; next = constrained max-kappa optimization.
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53,#57; PR leg still the risk (owner).
Next review: week-4 kill decision 09-17 — owner to decide continue/reweight/kill.
