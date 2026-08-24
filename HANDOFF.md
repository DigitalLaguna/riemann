# HANDOFF — session 2026-08-24 ~03:00 UTC (tick 169)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
30 claim rows: 16 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27,30),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 11 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29).
Track D: 8 NUMERIC + 1 NOTE (#28 S(t) scan). TWO scans in flight:
1. zero-scan-1e5.service: 15.0% (150000/999990), marginal 3.02 pts/s,
   ETA ~08-29 08:00Z (validity window [08-27,08-30]).
2. robin-full-1e10.service: launched tick 169 (pid 780213), full Robin scan
   [1e9,1e10) no reduction, L=1e8, ETA ~53 min -> ~03:45 UTC.

## Last work
Tick 169: tick 168's full Robin scan [1e9,1e10) launch was UNVERIFIED (log
entry ends before any launch output; at 169: no process, no unit, no output
file) -> A-005 class. Machine: (1) regression of the tick-167 generalized
robin_full_scan.py argv path on [1e8,3e8): max R = 0.9643557569555255 at
n=183783600, VERDICT ALL CHECKS PASS rc=0 — matches run2.txt exactly (R1 PASS).
(2) relaunched full scan as systemd transient unit robin-full-1e10.service:
active (running), run.txt header "range [1000000000,10000000001) subseg width
100000000 primes<=100000: 9592 SA in range: 7" (R2 PASS; SA count 7 == #30).
Zero scan: 150000/999990, marginal 3.017 pts/s (145k->150k), ETA unchanged.
check.sh committed for the full scan (verifies run.txt self-checks).

## Next action
(a) TRACK D: robin-full-1e10 completes ~03:45 UTC: read
    evidence/2026-08-24-robin-full-1e10/run.txt for "ROBIN-FULL-1e10 DONE rc=0"
    + "VERDICT: ALL CHECKS PASS"; bash evidence/2026-08-24-robin-full-1e10/check.sh;
    promote.sh add NOTE -> promote NUMERIC. If F2 witness HIT => RH FALSE =>
    STOP, page owner (constraint 5).
(b) TRACK D: zero scan completes ~08-29 08:00Z: read
    evidence/2026-08-23-zero-scan/full-run.txt for "ZERO-SCAN-1e5 DONE rc=0";
    F5a/b/c + F3/F4 verdicts + max/min g [1,1e5] -> NOTE via promote.sh
    (pilot was [1,1e3]-scoped only). Cross-check: zero count >= 134011.
    If completion falls outside [08-27,08-30], re-measure the cost profile.
(c) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then comment
    `propose #<PR>` on issue #816. CAVEAT: #816 ASSIGNED to IlPreteRosso since
    2026-01-28 (stale ~7 months); ping @IlPreteRosso on #816 or wait for disclaim.
(d) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12;
    (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11); (iii) row-3 t=0.18
    push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(e) Tracks A/C/E: A waits on the PR; C has NOTE #29 (4.896 reproduction) parked;
    E no in-flight work.

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
Week-1 reweight A30/B40/D15/C10/E5 stands. D 8 NUMERIC + 1 NOTE (#28).
In flight: zero scan [1,1e5] (15.0%, ETA ~08-29 08:00Z) + robin full scan
[1e9,1e10) (~53 min, ETA ~03:45 UTC). Next review 2026-08-29 (week 2):
milestone check + spot-check 3 cards vs PDFs + decide B next step.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics
leg met (#7,#9,#18); PR leg still the risk.
