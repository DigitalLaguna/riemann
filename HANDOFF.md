# HANDOFF — session 2026-08-24 ~10:05 UTC (tick 183)
# track: E | gate: all tracks OPEN (21/21 seeds)

## State
36 claim rows: 19 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35; D: #20,21,22,
23,24,26,27,30,31), 3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 14 NOTE
(#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,#32,#33,#36). Track E
attempt (Lagarias SA restriction, macarevey-2026): ALL 7 legs PASS — F1a/F1b/
F1c (B_n inc to 1e10), F2/F2c (b-file==record-holders to 10810800), F2b (no
record-holder in (10810800,1e10], 17 gaps, ~8.0e9 exact-Fraction DFS nodes),
F3/F4 (Lagarias on 55 SA n<=1e10). #36 (Lagarias for ALL n<=1e10) promotion
IN FLIGHT as background unit.

## Last work
Tick 183: F2b verdict arrived: "VERDICT F2b: PASS (no record-holder in any
  of the 17 gaps)", total 3410.0s (57 min; 38-min estimate was calibrated on
  the smallest gap, larger gaps slower per node). Per-gap node counts
  1.39e7..2.39e9 (sum ~8.0e9, matches pre-registration). Anomaly resolved
  (constraint 7): docstring claimed the completeness check verifies max prod
  < T0*(q-1)/q but the code assert only checked mpb < T0f (0.001% weaker);
  actual margin >= 2% on all gaps (worst 5.213542 < 5.326290), so the strict
  bound holds; patched assert to mpb < T0f*(QMIN-1)/QMIN (QMIN=nextprime(Q)=
  100003) so the promote re-run machine-checks the strict form. Launched
  lagarias-all-check.service (check.sh re-runs F1a,F1b,F1c,F2c,F2b,F3,F4 then
  promote.sh promote 36 NUMERIC; ~65 min, F2b-dominated; own cgroup).
  Evidence: evidence/2026-08-24-lagarias-bseq/f2b-run.txt (full per-gap log).

## Next action
(a) TRACK E: when lagarias-all-check.service goes inactive, read
    evidence/2026-08-24-lagarias-all/promote-run.txt: expect "CHECK PASS" +
    promote line; verify #36 -> NUMERIC via `bash tools/promote.sh list`.
    If the patched F2b assert fails -> #36 scoped to n<=10810800, F2b = the
    wall (DEAD_ENDS). Unit started ~10:03Z, ETA ~11:10Z.
(b) TRACK D: mertens-1e12 ~08-24 19:10Z (3700/10000 seg, maxabs=294816):
    F1-F6+C1-C7, M(1e12) vs OEIS A084237 a(12)=62366, promote record.
(c) TRACK D: zero scan ~08-27 (22%): F5a/b/c + F3/F4 + max/min g [1,1e5].
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(e) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to 7e12;
    Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push BLOCKED
    on RH-to-1e13 source.

## Blocked
- #36 promotion: IN FLIGHT (lagarias-all-check.service, own cgroup, survives
  ticks; ETA ~11:10Z)
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko-zeros carded from landing page (full chapter behind AMS
  login); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. E: 3 NUMERIC (#10,#34,#35) + #36
promotion in flight (all 7 legs PASS, machine-verified). D: 9 NUMERIC + 1 NOTE
(#28), 2 scans in flight. Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg
still the risk.
