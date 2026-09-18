# HANDOFF — session 2026-09-18 ~20:40 UTC (tick 268)
# track: C (kappa_m re-opt) + D (monitoring) | gate: all tracks OPEN (21/21 seeds)

## State
57 claim rows: 35 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43,#56; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 19 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53,#57).
This tick: no new claims (constraint-extraction step, no standalone verified result).
PENDING: none.

## Last work
Tick 268 (TRACK C kappa_m constraint extraction):
- Read BTY verbatim: eq(17)/(18) p(x)=sum kappa_m x^m approx h(x)=1/(1+x);
  paper "minimise the L-infinity norm" then "perturb ... slightly less favourable
  coefficients that can be more easily analysed". Lemma 3 (493) p(x)>0 on (0,1]
  [C1]; line 696 B(y)>=0 all y [C2]; Lemma 12 (1875) k=0 term <= -0.041 [C3a];
  Lemma 13 (2010) [C3b]; Lemma 14 (2058) [C3c]. Exact params (530-540):
  w(0)=5.672787598, K=16, eta0=0.0071093, sigma0=0.9935164, A0=(4.8596)^-1.
- Machine (kappa_unbounded_test.py -> machine-run-unbounded.txt): (C1)+(C2)
  ALONE DO NOT BOUND kappa (add K*x^6, K<=50, both stay ok, kappa->50.5).
- Machine (kappa_c3_test2.py -> machine-run-c3b.txt): (C3a) Lemma-12 k=0 bound
  DOES bound kappa: max over sigma in [sigma0,1) of k=0 term = -0.0942 (paper),
  bisect K in kappa_6 -> Kmax=0.03830132421 (kappa=0.542375829445 > required
  0.521015891482995). => (C3a) alone does NOT kill the idea.
- Tick 267 trivial upper bound (kappa<=f(1)+E_paper=0.50408988) valid only under
  ||p-f||_inf<=E_paper, which the lemmas do NOT directly require -> hint, not proof.
- NOTE: ticks 266/267 ran scripts but did not append to the tick log or update
  HANDOFF; their outputs are in evidence/2026-09-18-zfree-kappa-reopt/ and are
  now recorded in logs/2026-09-18.tick.log (TICK 268).
D MONITOR: all 3 jobs active since 18:06:47Z (no reboot), ckpt fresh ~20:38Z.
zero-scan ETA ~09-21..09-22; mertens a~330.5e9/1e12 ETA ~09-19 00:45Z;
robin n_sub~763/9000 best_R=0.9755059227362325 ETA ~09-22..09-23. No D claims.

## Next action
(a) TRACK C (tick 269): check (C3b) Lemma 13 + (C3c) Lemma 14 for modified
    kappa_m (paper + K*x^6, K~0.017..0.038). Requires computing F values
    (Laplace transform of w, Arb). If either kills kappa at < 0.521015891482995
    -> DEAD (record C-002 in DEAD_ENDS). Else re-optimize + re-verify lemmas.
(b) TRACK D: mertens-1e12-promote completes ~09-19 00:45Z -> read
    promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK PASS"),
    ledger #39 NOTE -> NUMERIC (36 total NUMERIC).
(c) TRACK D: zero-scan-1e5 completes ~09-21..09-22 -> full-run.txt, S(t) records.
(d) TRACK D: robin-full-1e12 completes ~09-22..09-23 -> full-run-resume.txt
    (expect "VERDICT: ALL CHECKS PASS"); new D NUMERIC.
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
  zero-scan (ETA ~09-21..09-22), mertens-1e12 (a~330.5e9/1e12, ETA ~09-19
  00:45Z), robin-full (n_sub~763/9000, ETA ~09-22..09-23) — all checkpointed.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs #29,#41
  (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream constant
  2.55028364035787 NUMERIC (#55). 4.8594 dead (C-001). kappa_m re-opt: gate PASS,
  threshold kappa>0.521015891482995; (C1)+(C2) unbounded, (C3a) allows
  kappa>required -> NOT dead; next = check (C3b)+(C3c).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53,#57; PR leg still the risk (owner).
Next review: week-4 kill decision 09-17 — owner to decide continue/reweight/kill.
