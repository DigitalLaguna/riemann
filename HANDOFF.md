# HANDOFF — session 2026-09-17 ~22:45 UTC (tick 244)
# track: D (recovery) | gate: all tracks OPEN (21/21 seeds)

## State
55 claim rows: 34 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 18 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53).
No promotions this tick (recovery tick). PENDING (verified, not yet ledg
ered): robin SA-scan (1e11,1e12] result (see Next (f)).

## Last work
Tick 244: machine rebooted 2026-09-17 22:29Z (~6 min before tick), killing
both transient D units (neither completed). Diagnosed + fixed + relaunched;
also discovered a dead robin job (not in prior handoff).
- zero-scan-1e5: had reached i=160000/999990 but ckpt-1e5.json was CORRUPTED
  to 0 bytes (reboot mid open("w")+json.dump); progress lost. FIX: save_ckpt
  now atomic (tmp+fsync+os.replace); verified (tiny scan: valid JSON + resume).
  Relaunched from scratch (pid 2982); ckpt valid (i_last=2886).
- mertens-1e12-promote: 3rd attempt, killed at ~30h wall (exp 12h41m);
  promote-run.txt 0 bytes. NO checkpoint. Relaunched (pid 2990).
- robin-1e12 (DISCOVERY): SA-scan robin_sa_1e12.py DONE+VERIFIED (sa-scan.txt
  "VERDICT: ALL CHECKS PASS"; no witness in (1e11,1e12] SA; max R=0.9755059227362326
  at n=160626866400) — not yet in ledger. FULL scan robin_full_scan.py [1e11,1e12)
  DIED Sep 16 23:16 CEST (~25h before reboot), UNKNOWN cause (0-byte stderr,
  96 null bytes in stdout, no journal stop line); ~105h no-checkpoint job.
- DEAD_ENDS +D-001 (non-atomic ckpt data loss, now fixed).

## Next action
(a) TRACK D: zero-scan-1e5.service running from scratch (atomic ckpt). On
    completion: read full-run.txt; compute S(t) records per zero-spacing-design.md
    (NOTE-level, mpmath). Re-estimate ETA once a fresh rate is measured.
(b) TRACK D: mertens-1e12-promote.service running. On completion: read
    promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK PASS"); ledger
    #39 NOTE -> NUMERIC (35 total).
(c) If mertens promote is killed by a reboot AGAIN: add a segment-boundary
    checkpoint to mertens_segmented.py, then relaunch (do not relaunch blind).
(d) TRACK D robin SA-scan: write check.sh (re-run robin_sa_1e12.py, assert
    F1-F3b PASS), promote.sh add NOTE then promote NUMERIC (track D, 11th NUMERIC).
(e) TRACK D robin FULL scan: investigate the Sep 16 23:16 death cause BEFORE
    relaunch; add a checkpoint (105h + frequent reboots).
(f) TRACK C: owner reports 2.55028364035787 to ANT network, or pick a new BTY
    constant to re-optimize.
(g) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner.
- mertens-1e12-promote: NO checkpoint; 12h41m job killed by reboots 3x
  (Aug 25, Sep 16 02:37, Sep 17 22:29). Add checkpoint before next blind relaunch.
- robin-full-1e12: DIED Sep 16 23:16 CEST, UNKNOWN cause; investigate before
  relaunch (105h no-checkpoint job).
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest (carded);
  odlyzko zero-data page 404 -> zero scan computes zeros itself.
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint.
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12).
- OWNER: week-4 kill decision (09-17) pending. Reboots frequent (Sep 15 x2,
  Sep 16 x2, Sep 17 x1) — long jobs vulnerable; prefer checkpointed runs.

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands (no weekly review ran 08-29..09-15).
D: 10 NUMERIC + 3 NOTE (#28,#37,#39; #39 promotion in flight); in flight:
  zero-scan (from scratch, atomic ckpt), mertens-1e12 promotion (no ckpt);
  robin SA-scan (1e11,1e12] verified, pending ledger; robin full scan dead.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs
  #29,#41 (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream
  constant 2.55028364035787 NUMERIC (#55).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53; PR leg still the risk
  (owner). Next review: week-4 kill decision 09-17 — owner to decide
  continue/reweight/kill with this handoff.
