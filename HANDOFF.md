# HANDOFF — session 2026-08-23 ~15:53 UTC (tick 148)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. S(t) scan [1,1e5] IN FLIGHT (pid 732546, 6% at last flush,
ETA ~19:45Z). New prior-art finding: 2510.14309 (see Last work).

## Last work
Tick 148 (this one): (1) S(t) scan status check — pid 732546 alive 100% CPU,
last flushed progress "progress 20000/333331 (6%) elapsed 356s"; result file
st_run-1e5.txt still 0 bytes (single pass, no partial output). NOT done.
(2) PRIOR-ART PRE-FLIGHT for the next D experiment (extreme zero spacings /
Lehmer pairs) — arXiv API 429/503 (shared IP), used Semantic Scholar + arXiv
search UI. FINDINGS (evidence/2026-08-23-zerogap-preflight/preflight.txt):
  - r-GAPS / extreme arg: [2510.14309] Inoue-Kobayashi-Toma (2025) "Explicit
    extreme values of the argument of the Riemann zeta-function" — improves
    Conrey-Turnage-Butterbaugh on r-gaps between zeros. NEWER than carded seed
    turnage-butterbaugh-2026 -> continuous-intake candidate.
  - LEHMER PAIRS: [2509.00906] (2025), [2411.07909] (2024), [1612.08627] (2016),
    [1508.05870] (2015).
  CONCLUSION: next D experiment NOT greenfield; scope against 2510.14309 +
  Lehmer-pairs line before choosing the specific scan.

## Next action
(a) TRACK D (weight 15): read evidence/2026-08-23-st-scan/st_run-1e5.txt for
    "ST-SCAN-1e5 DONE rc=0" (ready ~19:45Z) + max|S|/zero-count/max-arg-jump.
    If max arg jump >= pi -> step 0.3 too large, re-run smaller. mpmath=NOTE
    not NUMERIC (needs Arb or explicit error bound for a NUMERIC claim).
(b) TRACK D: read 2510.14309 (Inoue-Kobayashi-Toma) to scope the zero-spacing
    experiment; card it (continuous intake, 1/day). This also informs the
    S(t) record question (handoff b, tick 147).
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
- S(t) record paper: not on arXiv; 2510.14309 (2025) is the closest on-arXiv
  reference for extreme arg / r-gaps — read before any record claim
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 7 NUMERIC (#20-#24,#26,#27). S(t)
scan [1,1e5] in flight (ETA ~19:45Z). Next review 2026-08-29 (week 2): milestone
check + spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17):
Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18);
PR leg still the risk.
