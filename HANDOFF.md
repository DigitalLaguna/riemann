# HANDOFF — session 2026-08-24 ~12:10 UTC (tick 187)
# track: C (promotion) + D (scans) | gate: all tracks OPEN (21/21 seeds)

## State
36 claim rows: 21 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31; C: #33), 3 FORMAL (A: #2, #12 [SUPERSEDED by
#25], #25), 12 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,#32).
Track C: #33 (4.896 headline justified by stated intermediates, F1-F5 ALL
PASS) promoted NOTE->NUMERIC this tick via evidence/2026-08-24-zfree-4896/
(check.sh re-runs final-bound.py, byte-identical regression; CHECK PASS).

## Last work
Tick 187: (1) Built evidence/2026-08-24-zfree-4896/ (check.sh + recorded
  run + README with verbatim paper quotes) and promoted #33 NOTE->NUMERIC:
  "promoted #33: NOTE -> NUMERIC" (promote.sh, checker CHECK PASS).
  (2) Re-measured all three in-flight scans at 12:02Z:
  - robin-full-1e11: subseg 133/1000, best_R=0.972015886980 at
    n=13967553600 (unchanged; the SA number), ~40 s/subseg -> ETA ~21:40Z.
    ANOMALY RESOLVED: prior handoff "~11:45Z (41/100 subseg)" — "41/100"
    was a typo for 41/1000 (width 1e8 over [1e10,1e11) = 1000 subsegs).
  - mertens-1e12: 5200/10000 seg, maxabs=294816 (unchanged), ETA ~18:15Z.
  - zero-scan-1e5: 230000/999990 (23%), 0.262 s/step (rising with t; was
    0.219 at 180000) -> ETA ~08-26 21:00Z (earlier than ~08-27 window).

## Next action
(a) TRACK D: robin-full-1e11.service ~21:40Z: read
    evidence/2026-08-24-robin-1e11/full-run.txt (expect "ROBIN-FULL-1e11
    DONE rc=0" + final best_R), run pre-registered F1/F2/F3a/F3b (see
    logs/2026-08-24.tick.log tick 184), promote claim (Robin full scan
    [1e10,1e11): max R, no witness R>=1).
(b) TRACK D: mertens-1e12 ~18:15Z: F1-F6 + C1-C7, M(1e12) vs OEIS
    A084237 a(12)=62366, promote record.
(c) TRACK D: zero scan ~08-26 21:00Z: F5a/b/c + F3/F4 + max/min g [1,1e5].
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(e) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to
    7e12; Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push
    BLOCKED on RH-to-1e13 source.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko-zeros carded from landing page (full chapter behind AMS
  login); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. C: 1 NUMERIC (#33) — 4.896
reproduction chain now machine-verified end-to-end; next C step is the
actual re-optimization (vary a_k / smoothing, minimize 1/A*) — not started.
E: 4 NUMERIC (#10,#34,#35,#36) — Lagarias attempt fully machine-verified;
next E attempt next week (one per week, frontier-escalated). D: 9 NUMERIC
+ 1 NOTE (#28), 3 scans in flight (robin-full-1e11 ETA 21:40Z,
mertens-1e12 ETA ~18:15Z, zero-scan ETA ~08-26 21:00Z). Next review
2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs + decide
B next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig
figs — numerics leg met (#7,#9,#18); PR leg still the risk.
