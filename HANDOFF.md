# HANDOFF — session 2026-08-23 ~17:50 UTC (tick 151)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. TWO scans in flight: (1) S(t) scan [1,1e5] pid 732546,
30% at 17:26Z (100000/333331, elapsed 4987s; per-20000-pt intervals growing
356->1695s -> ETA ~23:00Z-09:00Z, was ~20:00Z); (2) zero-scan PILOT PASSED
tick 151 (evidence/2026-08-23-zero-scan/pilot-run.txt): 649 zeros in [1,1e3],
F1-F4 all PASS (first 7 zeros match fetched wiki-zeta.html to 6dp; count vs
RvM 647.62 within ±3; gaps in [0.327,3.073]). Full [1,1e5] zero scan NOT yet
launched.

## Last work
Tick 151 (this one): (1) S(t) scan status — pid 732546 alive 100% CPU, last
flush "progress 100000/333331 (30%) elapsed 4987s"; result file still 0 bytes;
ETA revised worse (per-point cost growing). (2) Zero-spacing scan designed +
piloted: tracks/d-search/zero-spacing-design.md (definition λr/µr quoted
verbatim from inoue-kobayashi-toma-2025 p.2: (γ_{n+r}−γ_n)/(2πr/log γ_n);
4 pre-registered falsification tests F1-F4 BEFORE run) + tracks/d-search/
zero_scan.py (Z(t)=re(e^{iθ}ζ(1/2+it)), coarse 0.05 + bisection 1e-10,
mpmath 30 dps). Pilot [1,1e3] step 0.05, 437s rc=0: count 649 (RvM 647.62,
|Δ|=1.38 PASS); first 7 zeros = wiki values to 6dp (PASS); max g = 3.073313
(zeros 650.6687/653.6496) < 3.18 Bui-Milinovich; min g = 0.327118
(750.6560/750.9664) < 0.515396 Preobrazhenskii; all gaps ⊂ (0.1,10). 2nd-
largest gap is the FIRST gap (g=2.903301, 14.1347->21.0220) — first zero
isolated, expected. mpmath = NOTE not NUMERIC; no ledger claim yet (pilot
validates pipeline; record claim comes from full scan).

## Next action
(a) TRACK D (weight 15): launch full zero scan in background:
    nohup python3 tracks/d-search/zero_scan.py 1.0 100000.0 0.1 >
    evidence/2026-08-23-zero-scan/full-run.txt 2> .../full.stderr &
    (step 0.1, ETA ~10h; miss-risk: pairs with actual gap < 0.1 = normalized
    < 0.115 at t=1e5, pilot min was 0.327; falsification: count vs RvM(1e5)
    main term ±3, else re-run step 0.05).
(b) TRACK D: read evidence/2026-08-23-st-scan/st_run-1e5.txt for completion
    (ETA ~23:00Z-09:00Z) + max|S|/zero-count/max-arg-jump. If max arg jump
    >= pi -> step 0.3 too large, re-run smaller. mpmath=NOTE not NUMERIC.
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
In flight: S(t) scan [1,1e5] (30%, ETA ~23:00Z+) + zero-scan pilot PASSED
(full [1,1e5] launch is next tick's step (a)). Next review 2026-08-29 (week 2):
milestone check + spot-check 3 cards vs PDFs + decide B next step. Week-4 kill
(09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(#7,#9,#18); PR leg still the risk.
