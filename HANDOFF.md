# HANDOFF — session 2026-08-23 ~21:30 CEST (tick 155)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. TWO scans in flight (both own systemd units, verified active):
(1) S(t) scan [1,1e5] st-scan-1e5.service pid 732546: 54% (180000/333331),
elapsed 13312s; rate SLOWING (0.0849/0.1368/0.1094 s/pt per 20k seg, noisy,
most recent 0.1094). ETA ~00:00-00:30 UTC 08-24 (02:00-02:30 CEST), ~4.5-5h.
(2) FULL zero scan [1,1e5] step 0.1 zero-scan-1e5.service pid 745484: 4%
(40000/999990), elapsed 3246s; rate CLEARLY INCREASING (0.0498->0.1220 s/pt,
cost~t^0.5-0.55 Riemann-Siegel). ETA ~4-5 days, completion ~08-27..08-29,
best ~4.7 days (~08-28). (Handoff-153 "3-4 days" was the low end.)

## Last work
Tick 155 (this one): monitoring tick. (1) Verified BOTH scans alive via
systemctl (own cgroups, survived 5+ ticks; A-005 nohup-kill already closed).
(2) Re-estimated ETAs from fresh progress: S(t) rate rose from the 85s/20k
plateau to ~110-137s/20k -> ETA pushed 22:30Z -> ~00:00-00:30Z 08-24. Zero
scan rate rising 0.0498->0.1220 s/pt; power-law fit cost~t^a (a~0.45-0.56),
a=0.5 gives 4.7 days -> ~08-28. (3) MACHINE-CHECK: rvn(1e5) per zero_scan.py
= 138067.55841923953 EXACTLY matches design F5a threshold 138067.56 -> no
anomaly (my hand estimate 137986 was a log-precision slip). No new claims
(both scans in flight; mpmath = NOTE when done).

## Next action
(a) TRACK D (weight 15): S(t) scan completion ETA ~00:00-00:30 UTC 08-24:
    read evidence/2026-08-23-st-scan/st_run-1e5.txt for "ST-SCAN-1e5 DONE
    rc=0": max|S|, zero count (cross-check: must be <= zero-scan count), max
    arg jump (< pi else step 0.3 too large -> re-run smaller). mpmath = NOTE.
(b) TRACK D: zero scan: check full.stderr progress; re-estimate ETA at 10%
    (next flush ~50000/999990). On completion: F5a/b/c + F3/F4 verdicts +
    records max/min g [1,1e5] -> NOTE claim via promote.sh (pilot was
    [1,1e3]-scoped only).
(c) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then comment
    `propose #<PR>` on issue #816. CAVEAT: #816 ASSIGNED to IlPreteRosso since
    2026-01-28 (stale ~7 months); ping @IlPreteRosso on #816 or wait for disclaim.
(d) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12;
    (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11); (iii) row-3 t=0.18
    push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(e) Tracks A/C/E: A waits on the PR; C/E no in-flight work.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner;
  #816 claimant (IlPreteRosso) contact per CONTRIBUTING (see (c))
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 (2025/26) is the
  closest on-arXiv reference for extreme arg / r-gaps — NOW CARDED
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page;
  odlyzko personal zero-data page 404 (evidence/2026-08-23-st-scan/odlyzko-*.html)
  -> zero scan computes zeros itself (pilot validated)
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 7 NUMERIC (#20-#24,#26,#27).
In flight: S(t) scan [1,1e5] (54%, ETA ~00:00-00:30Z 08-24) + full zero scan
[1,1e5] (4%, ETA ~4-5 days, completion ~08-27..08-29, best ~08-28). Next review
2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs + decide B
next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs —
numerics leg met (#7,#9,#18); PR leg still the risk.
