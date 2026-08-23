# HANDOFF — session 2026-08-23 ~16:40 UTC (tick 149)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. S(t) scan [1,1e5] IN FLIGHT (pid 732546, 18% at 16:24Z,
per-point cost growing: 356/687/982s per 20000 pts -> ETA ~20:00Z or later).
New card: inoue-kobayashi-toma-2025 (continuous intake, card_ok PASS).

## Last work
Tick 149 (this one): (1) S(t) scan status — pid 732546 alive 100% CPU, last
flush "progress 60000/333331 (18%) elapsed 2025s"; result file still 0 bytes.
NOT done; intervals slowing (356->687->982s per 20000 pts), ETA worse than
tick-148's 19:45Z. (2) CARD 2510.14309 Inoue-Kobayashi-Toma (arXiv v2, 7 Apr
2026) "Explicit extreme values of the argument of the Riemann zeta-function":
fetched PDF (8pp) + pdftotext, wrote lit/cards/inoue-kobayashi-toma-2025.md,
all 6 quotes machine-verified by substring search on the text file (one stray
\x01 pdftotext char stripped, noted in card), gate.card_ok -> (True, '').
CONTENT: Thm1 (RH) sup ±(S(t+h)-S(t)) >= (1-E)sqrt(h log T/pi); Thm2 (RH)
λr >= 1+sqrt(2/r)-..., µr <= 1-sqrt(2/r)+... — improves A0=0.9064997 (Inoue)
to sqrt(2)=1.4142, supersedes Conrey-Turnage-Butterbaugh Θ=0.599648/ϑ=0.379674;
Thm3: Montgomery-Odlyzko method limitation λ1>=3.022, µ1<=0.508 (L<=T).
Best under RH: λ1>3.18 (Bui-Milinovich), µ1<0.515396 (Preobrazhenskii).

## Next action
(a) TRACK D (weight 15): read evidence/2026-08-23-st-scan/st_run-1e5.txt for
    "ST-SCAN-1e5 DONE rc=0" (ETA ~20:00Z+) + max|S|/zero-count/max-arg-jump.
    If max arg jump >= pi -> step 0.3 too large, re-run smaller. mpmath=NOTE
    not NUMERIC (needs Arb or explicit error bound for a NUMERIC claim).
(b) TRACK D: design the zero-spacing / Lehmer-pair scan scoped against
    inoue-kobayashi-toma-2025 (record target: normalized gap vs 3.18 and
    sqrt(2)/r asymptotics; pre-register falsification before running).
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
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 7 NUMERIC (#20-#24,#26,#27).
S(t) scan [1,1e5] in flight (ETA ~20:00Z+). Next review 2026-08-29 (week 2):
milestone check + spot-check 3 cards vs PDFs + decide B next step. Week-4 kill
(09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(#7,#9,#18); PR leg still the risk.
