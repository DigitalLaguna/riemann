# HANDOFF — session 2026-08-24 ~16:55 UTC (tick 196)
# track: C (promotion) + D (scans) | gate: all tracks OPEN (21/21 seeds)

## State
38 claim rows: 22 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31; C: #33,#38), 3 FORMAL (A: #2, #12 [SUPERSEDED by
#25], #25), 13 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,#32,#37).
Track C: #38 (missing factor of kappa in bellotti-trudgian-yang-2026 final line)
promoted NOTE->NUMERIC this tick via evidence/2026-08-24-zfree-kappa/ (check.sh
re-runs kappa-sum.py, F1-F3 ALL PASS, byte-identical regression; CHECK PASS).
KEY RESULT: the paper's 4.896 zero-free constant is valid but NOT tight — the
proof actually supports A_corr = A_paper*kappa = 2.4678 (region ~1.98x wider).

## Last work
Tick 196: (1) Re-traced the proof (verbatim quotes re-verified) to confirm the
  LOGICAL step behind #38: LHS = (a*kappa/2)*f(0)*log t with f(0)=eta*w(0)*kappa
  (Definition 2) => (a*kappa^2*w(0)/2)*(eta*log t); paper divides by
  (a*kappa*w(0)/2), missing one factor of kappa. (2) Ran the existing checker
  (CHECK PASS) and promoted #38 NOTE->NUMERIC: "promoted #38: NOTE -> NUMERIC"
  (promote.sh, checker CHECK PASS). (3) Re-measured all three in-flight scans
  at 16:50Z:
  - robin-full-1e11: subseg 564/1000, best_R=0.972015886980 at
    n=13967553600 (unchanged; the SA number), ~40.4 s/subseg -> ETA ~21:35Z.
  - mertens-1e12: 9000/10000 seg, maxabs=331302 (unchanged), ~4.5 s/seg ->
    ETA ~17:56Z.
  - zero-scan-1e5: 260000/999990 (26%), 0.302 s/step (rising with t; was
    0.262 at 230000) -> ETA ~08-26 (later than 04:41Z at current rate).

## Next action
(a) TRACK C: the actual re-optimization (vary a_k / smoothing, minimize 1/A*)
    — NOW UNBLOCKED by #38. Start from A_corr = 2.4678 (NOT 4.896): the
    paper's stated constant is not tight, so the re-optimization's baseline is
    the corrected 2.4678. Prior-art pre-flight first (new attempt).
(b) TRACK D: mertens-1e12.service ~17:56Z: read
    evidence/2026-08-24-mertens-1e12/run.txt (expect "MERTENS-1e12 DONE rc=0"
    + final maxabs), run pre-registered F1-F6 + C1-C7, M(1e12) vs OEIS
    A084237 a(12)=62366, promote record.
(c) TRACK D: robin-full-1e11.service ~21:35Z: read
    evidence/2026-08-24-robin-1e11/full-run.txt (expect "ROBIN-FULL-1e11
    DONE rc=0" + final best_R), run F1/F2/F3a/F3b (see logs tick 184),
    promote claim (Robin full scan [1e10,1e11): max R, no witness R>=1).
(d) TRACK D: zero scan ~08-26: F5a/b/c + F3/F4 + max/min g [1,1e5].
(e) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(f) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to
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
Week-1 reweight A30/B40/D15/C10/E5 stands. C: 2 NUMERIC (#33,#38) — 4.896
reproduction chain machine-verified end-to-end (#33) AND the missing-factor-of-
kappa correction machine-verified (#38: true constant 2.4678, not 4.896). Next
C step is the actual re-optimization (vary a_k / smoothing, minimize 1/A*)
starting from A_corr = 2.4678 — now unblocked, not started. E: 4 NUMERIC
(#10,#34,#35,#36) — Lagarias attempt fully machine-verified; next E attempt
next week (one per week, frontier-escalated). D: 9 NUMERIC + 2 NOTE (#28,#37),
3 scans in flight (robin-full-1e11 ETA 21:35Z, mertens-1e12 ETA ~17:56Z,
zero-scan ETA ~08-26). Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg
still the risk.
