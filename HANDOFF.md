# HANDOFF — session 2026-08-24 ~03:20 UTC (tick 170)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
30 claim rows: 16 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27,30),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 11 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29).
Track D: 8 NUMERIC + 1 NOTE (#28 S(t) scan). TWO scans in flight:
1. zero-scan-1e5.service: 15.5% (155000/999990), marginal 3.008 pts/s,
   ETA ~08-27 09:15Z (validity window [08-27,08-30]).
2. robin-full-1e10.service: subseg 44/100 at 03:18Z, 37.1 s/subseg,
   ETA ~03:53 UTC. Running best_R=0.967846059640 at n=3491888400 (an SA number).

## Last work
Tick 170: both scans verified alive + progressing (robin subseg 38->44 during
tick; zero 155000/999990). Bounded step: independent verification of the robin
scan's running best + F3b target by direct evaluation (sympy factorint +
50-digit mpmath, independent of the segmented sieve):
  R(3491888400)=0.9678460596395451... -> .12f display 0.967846059640 == scan (V1 PASS)
  R(6983776800)=0.97366979838271341367... == SA scan 0.9736697983827134 (V2 PASS)
  VERDICT: ALL CHECKS PASS (evidence/2026-08-24-robin-full-1e10/verify-running-best.txt).
  First run showed V1/V2 FAIL = harness artifact (mp.nstr strips trailing zero;
  14-vs-16 sig-digit miscount), resolved in-tick by corrected comparison.
  Anomaly resolved (constraint 7): 4th argv 0.973669798383 = SA_REF (12-sig
  display of SA-scan max R in [1e9,1e10), sa-scan.txt), used only by F3b.
  NOTE: SA argmax n=6983776800 is in subseg 60 (not yet scanned) -> final
  full-scan max must be >= 0.9736697983827134 (F3a). Script nstr = 16 sig digits.

## Next action
(a) TRACK D: robin-full-1e10 completes ~03:53 UTC (tick 171 or 172): read
    evidence/2026-08-24-robin-full-1e10/run.txt for "ROBIN-FULL-1e10 DONE rc=0"
    + "VERDICT: ALL CHECKS PASS"; bash evidence/2026-08-24-robin-full-1e10/check.sh;
    promote.sh add NOTE -> promote NUMERIC (max R + argmax + 1-R + F1/F2/F3a/F3b).
    Expect max R >= 0.9736697983827134 (SA floor). If F2 witness HIT => RH FALSE
    => STOP, page owner (constraint 5).
(b) TRACK D: zero scan completes ~08-27 09:15Z: read
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
In flight: zero scan [1,1e5] (15.5%, ETA ~08-27 09:15Z) + robin full scan
[1e9,1e10) (44%, ETA ~03:53 UTC). Next review 2026-08-29 (week 2):
milestone check + spot-check 3 cards vs PDFs + decide B next step.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics
leg met (#7,#9,#18); PR leg still the risk.
