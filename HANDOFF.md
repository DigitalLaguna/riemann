# HANDOFF — session 2026-08-24 ~18:22 UTC (tick 199)
# track: D (mertens-1e12 collected) | gate: all tracks OPEN (21/21 seeds)

## State
39 claim rows: 22 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31; C: #33,#38), 3 FORMAL (A: #2, #12 [SUPERSEDED by
#25], #25), 14 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,#32,
#37,#39). Track D: mertens-1e12 scan DONE rc=0 18:05:48Z: max |M(x)| x<=1e12
= 331302 first at x=661066575037; M(10^12)=62366=OEIS A084237 a(12); witness
max |M|/sqrt(x) x>=100 = 0.570590889 @ 7766842813. Pre-registered F1-F6
(tick 174) ALL PASS vs machine output. Claim #39 NOTE added; promotion in
flight (full 1e12 determinism re-run ~12.75 h). Track C: #38 NUMERIC (missing
factor of kappa; A_corr = 2.4678, not 4.896).

## Last work
Tick 199: (1) mertens-1e12.service completed 18:05:48Z rc=0; read
  evidence/2026-08-24-mertens-1e12/run.txt (C1-C7 PASS, VERDICT ALL CHECKS
  PASS). (2) Ran pre-registered F1-F6 (tick 174) against the output:
  F1 C1-C7 PASS; F2 M(1e12)=62366=OEIS a(12); F3 witness 0.570590889<1.0
  (no Mertens counterexample); F4 331302>=94909 (1e11 record #27); F5
  0.570590889<0.585768 (Kuznetsov); F6 M(10^k) k=1..11 identical to verified
  1e11 run3.txt. All PASS. (3) Wrote check.sh (full 1e12 re-run + C1-C7 +
  record/witness determinism + F3/F4/F5 + OEIS cross-check), added claim #39
  NOTE, launched mertens-1e12-promote.service (PID 844907, active) — promotes
  #39 NOTE->NUMERIC on CHECK PASS, ETA ~08-25 07:00Z. (4) Re-measured
  in-flight scans at 18:15Z:
  - robin-full-1e11: subseg 681/1000, best_R=0.972015886980 at
    n=13967553600 (unchanged; the SA number), 40.55 s/subseg -> ETA ~21:50Z.
  - zero-scan-1e5: 270000/999990 (27%), 0.313 s/step (rising with t) ->
    ETA ~08-27 or later.

## Next action
(a) TRACK D: mertens-1e12-promote.service ~08-25 07:00Z: read
    evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + "promoted #39: NOTE -> NUMERIC"); ledger +1 NUMERIC.
(b) TRACK D: robin-full-1e11.service ~21:50Z: read
    evidence/2026-08-24-robin-1e11/full-run.txt (expect "ROBIN-FULL-1e11
    DONE rc=0" + final best_R), run F1/F2/F3a/F3b (see logs tick 184),
    promote claim (Robin full scan [1e10,1e11): max R, no witness R>=1).
(c) TRACK C: the actual re-optimization (vary a_k / smoothing, minimize
    1/A*) — NEW attempt, prior-art pre-flight first. Baseline A_corr =
    2.4678 (NOT 4.896; #38).
(d) TRACK D: zero scan ~08-27: F5a/b/c + F3/F4 + max/min g [1,1e5].
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
Week-1 reweight A30/B40/D15/C10/E5 stands. D: 9 NUMERIC + #39 NOTE
(promotion in flight) + 2 NOTE (#28,#37); in flight: robin-full-1e11
ETA 21:50Z, zero-scan ETA ~08-27, mertens-1e12 promotion ETA 08-25 07:00Z.
C: 2 NUMERIC (#33,#38); next C step is the re-optimization from A_corr=2.4678
— not started. E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week
(frontier-escalated). Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg
still the risk.
