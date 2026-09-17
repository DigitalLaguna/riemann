# HANDOFF — session 2026-09-17 ~23:15 UTC (tick 245)
# track: D (recovery) | gate: all tracks OPEN (21/21 seeds)

## State
56 claim rows: 35 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43,#56; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 18 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#52,#53).
This tick: #56 NOTE->NUMERIC (robin SA-scan (1e11,1e12]; 11th D NUMERIC).
PENDING (verified, not yet ledg ered): none.

## Last work
Tick 245:
- robin SA-scan (1e11,1e12] PROMOTED: wrote evidence/2026-09-16-robin-1e12/
  check.sh (fresh re-run of robin_sa_1e12.py + assert F1-F3b + diff vs stored
  sa-scan.txt); machine: "CHECK PASS: Robin SA-scan (1e11,1e12] re-verified"
  (0.285s). promote.sh: NOTE #56 -> NUMERIC. (First check.sh run failed on my
  own cd path bug ../../.. vs ../..; fixed, not a math issue.)
- robin FULL scan death cause RESOLVED (was "UNKNOWN"): journalctl
  --list-boots shows boot -1 ended Wed 2026-09-16 23:15:47 CEST — a REBOOT
  25s after the last progress line (subseg 12, 516.7s). It is the 2nd Sep-16
  reboot (handoff listed "Sep 16 x2" without linking it). Machine down
  23:15:47 CEST Sep 16 -> 00:29:35 CEST Sep 18 (~25.2h). 96 null bytes =
  partial-write artifact of the hard kill. No bug; relaunch safe, but the
  105h job still needs a checkpoint first.
- Both transient units healthy at 23:07Z: zero-scan-1e5 (ckpt i_last=27311/
  999990, atomic ckpt OK, ~16.5 steps/s, ETA ~17h -> ~09-18 15:30Z);
  mertens-1e12-promote (pid 2990, 100% CPU, 29min/12h41m -> ~09-18 12:20Z).

## Next action
(a) TRACK D: zero-scan-1e5.service running. On completion: read full-run.txt;
    compute S(t) records per zero-spacing-design.md (NOTE-level, mpmath).
(b) TRACK D: mertens-1e12-promote.service running. On completion: read
    promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + "CHECK PASS"); ledger
    #39 NOTE -> NUMERIC (36 total).
(c) TRACK D robin FULL scan: add a subseg-boundary checkpoint to
    robin_full_scan.py (atomic, like zero_scan save_ckpt), then relaunch as a
    transient unit. Death cause resolved (reboot) — relaunch is safe.
(d) If mertens promote is killed by a reboot AGAIN: add a segment-boundary
    checkpoint to mertens_segmented.py, then relaunch (do not relaunch blind).
(e) TRACK C: owner reports 2.55028364035787 to ANT network, or pick a new BTY
    constant to re-optimize.
(f) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner.
- mertens-1e12-promote: NO checkpoint; 12h41m job killed by reboots 3x
  (Aug 25, Sep 16 02:37, Sep 17 22:29). Add checkpoint before next blind relaunch.
- robin-full-1e12: death cause RESOLVED (Sep 16 23:15:47 CEST reboot); still
  needs a checkpoint before relaunch (105h job, reboots frequent).
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest (carded);
  odlyzko zero-data page 404 -> zero scan computes zeros itself.
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint.
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12).
- OWNER: week-4 kill decision (09-17) pending. Reboots frequent (Sep 15 x2,
  Sep 16 x2, Sep 17 x1) — long jobs vulnerable; prefer checkpointed runs.

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands (no weekly review ran 08-29..09-15).
D: 11 NUMERIC + 3 NOTE (#28,#37,#39; #39 promotion in flight); in flight:
  zero-scan (i=27311/999990, atomic ckpt), mertens-1e12 promotion (no ckpt);
  robin SA-scan (1e11,1e12] LEDGERED (#56); robin full scan awaiting ckpt+relaunch.
C: 13 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51,#54,#55) + NOTEs
  #29,#41 (A0 typo),#48 (exact m=0 MARGINAL); A0_max pinned #54; downstream
  constant 2.55028364035787 NUMERIC (#55).
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25) + sweep NOTEs #32,#52,#53; PR leg still the risk
  (owner). Next review: week-4 kill decision 09-17 — owner to decide
  continue/reweight/kill with this handoff.
