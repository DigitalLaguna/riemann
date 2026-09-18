# HANDOFF — session 2026-09-18 ~01:20 UTC (tick 249)
# track: D (monitoring) + A (sweep) | gate: all tracks OPEN (21/21 seeds)

## State
57 claim rows: 35 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43,#56; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 19 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53,#57).
This tick: #57 NOTE (arXiv sweep 09-18; 41 new, 0 escalations; 2609.20367
claimed-RH preprint flagged for owner). PENDING (verified, not yet ledgered): none.

## Last work
Tick 249:
- Verified all three in-flight D jobs healthy + progressing + reboot-safe
  (atomic ckpts from ticks 244/246/247/248): zero-scan i_last=75640/999990,
  mertens a_start=24.3e9/1e12, robin n_sub=116/1000. (Rates slower than
  no-contention estimates due to 3-way CPU contention.)
- Ran OVERDUE daily arXiv math.NT sweep (last 09-16): HTTP 200, 60 entries,
  newest 2609.20367v1 (09-17T13:25:52Z); 41 new vs 09-16. 0 escalations.
  NOTABLE: 2609.20367v1 "The Three Gates: A Rooted-Operator Approach to Weil
  Positivity" CLAIMS TO PROVE RH (red flags: non-standard jargon + "fantasy
  interludes"). Flagged for owner; NOT carded/read/built-on. 5 tangential
  papers noted+dropped (2609.17875 zero-density, 2609.18198, 2609.18414,
  2609.18569, 2609.17899). 35 irrelevant dropped. -> NOTE #57.

## Next action
(a) TRACK D: zero-scan-1e5.service running. On completion: read full-run.txt;
    compute S(t) records per zero-spacing-design.md (NOTE-level, mpmath).
    ETA ~09-19 morning (contention).
(b) TRACK D: mertens-1e12-promote.service running. On completion: read
    promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK PASS"); ledger
    #39 NOTE -> NUMERIC (36 total). ETA ~09-19 ~10:30Z.
(c) TRACK D: robin-full-1e12.service running. On completion: read
    full-run-resume.txt (expect "VERDICT: ALL CHECKS PASS"); new D NUMERIC
    (full scan [1e11,1e12), SA_REF 0.975505922736). ETA ~09-19 ~10:15Z.
(d) If any job is killed by a reboot: it RESUMES from its ckpt (no blind
    relaunch). Verify ckpt is valid JSON before resuming.
(e) TRACK C: owner reports 2.55028364035787 to ANT network, or pick a new BTY
    constant to re-optimize.
(f) OWNER: (1) open PNT+ PR (evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2)
    + comment `propose #<PR>` on issue #816; (2) week-4 kill decision (09-17)
    pending; (3) NEW: 2609.20367v1 claimed-RH preprint — owner decides if a
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
  zero-scan (i=75640/999990), mertens-1e12 (a_start=24.3e9/1e12),
  robin-full (n_sub=116/1000) — all checkpointed/reboot-safe.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs
  #29,#41 (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream
  constant 2.55028364035787 NUMERIC (#55).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53,#57; PR leg still the risk
  (owner). Next review: week-4 kill decision 09-17 — owner to decide
  continue/reweight/kill with this handoff.
