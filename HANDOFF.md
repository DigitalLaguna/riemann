# HANDOFF — session 2026-08-24 ~04:00 UTC (tick 171)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
31 claim rows: 17 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,
27,30,31), 3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by
#25], #25 IK lemmas v2), 11 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,
#28,#29). Track D: 9 NUMERIC + 1 NOTE (#28 S(t) scan). ONE scan in flight:
zero-scan-1e5.service: 16.0% (160000/999990), 0.333 s/step (stable),
ETA ~08-27 08:00Z (validity window [08-27,08-30]).

## Last work
Tick 171: robin-full-1e10 COMPLETED (DONE rc=0 03:47:08Z) -> promoted #31 NUMERIC.
  FULL SCAN [1e9,1e10) (all n, no CA/SA reduction):
    max R = 0.9736697983827134 at n = 6983776800 (superabundant, sigma=37797580800)
    1 - R = 0.02633020161728659
    F2 witness R(n)>=1: none (max R < 1) => RH still consistent (no constraint-5 stop)
    F1 sigma cross-check vs sympy 31/31 (0 mismatches): PASS
    F3a full-scan max == SA max (#30) 0.9736697983827134: PASS (argmax IS the SA argmax)
    F3b 12-sig display 0.973669798383 == SA_REF: PASS
    VERDICT: ALL CHECKS PASS; check.sh: CHECK PASS
  With #26: full-scan max over [1e8,1e10) = 0.9736697983827134 @ 6983776800.
  Evidence: evidence/2026-08-24-robin-full-1e10/run.txt (lines 94-109).

## Next action
(a) TRACK D: zero scan completes ~08-27 08:00Z: read
    evidence/2026-08-23-zero-scan/full-run.txt for "ZERO-SCAN-1e5 DONE rc=0";
    F5a/b/c + F3/F4 verdicts + max/min g [1,1e5] -> NOTE via promote.sh
    (pilot was [1,1e3]-scoped only). Cross-check: zero count >= 134011.
    If completion falls outside [08-27,08-30], re-measure the cost profile.
(b) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then comment
    `propose #<PR>` on issue #816. CAVEAT: #816 ASSIGNED to IlPreteRosso since
    2026-01-28 (stale ~7 months); ping @IlPreteRosso on #816 or wait for disclaim.
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12;
    (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11); (iii) row-3 t=0.18
    push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(d) Tracks A/C/E: A waits on the PR; C has NOTE #29 (4.896 reproduction) parked;
    E no in-flight work.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner;
  #816 claimant (IlPreteRosso) contact per CONTRIBUTING (see (b))
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 (2025/26) is the
  closest on-arXiv reference for extreme arg / r-gaps — NOW CARDED
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page;
  odlyzko personal zero-data page 404 (evidence/2026-08-23-st-scan/odlyzko-*.html)
  -> zero scan computes zeros itself (pilot validated)
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 9 NUMERIC + 1 NOTE (#28).
In flight: zero scan [1,1e5] (16.0%, ETA ~08-27 08:00Z). Next review 2026-08-29
(week 2): milestone check + spot-check 3 cards vs PDFs + decide B next step.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics
leg met (#7,#9,#18); PR leg still the risk.
