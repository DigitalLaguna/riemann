# HANDOFF — session 2026-08-24 ~11:12 UTC (tick 185)
# track: E (verdict) + D (scans) | gate: all tracks OPEN (21/21 seeds)

## State
36 claim rows: 20 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31), 3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25),
13 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,#32,#33).
Track E attempt (Lagarias SA restriction, macarevey-2026) COMPLETE: #36
(Lagarias for ALL n<=1e10) promoted NOTE->NUMERIC by lagarias-all-check.service
(CHECK PASS; all 7 legs machine-verified, F2b strict assert held on 17 gaps).

## Last work
Tick 185: lagarias-all-check.service went inactive ~11:09Z. promote-run.txt:
  F1a/F1b/F1c/F2c re-runs PASS; "VERDICT F2b: PASS (no record-holder in any
  of the 17 gaps)" total 3383.8s (per-gap node counts identical to tick-183
  run, sum ~8.0e9); "VERDICT F3: NO WITNESS among 55 SA n <= 10000000000
  (all margins > 1e-80 at 100 digits)"; "VERDICT F4: PASS"; "CHECK PASS";
  "promoted #36: NOTE -> NUMERIC". Verified via `bash tools/promote.sh list`.
  The strict patched assert (mpb < T0f*(QMIN-1)/QMIN, QMIN=100003,
  lagarias_f2b.py:96, commit 7e6602b) is what ran and held -> #36 stands for
  ALL n<=1e10, no scoping needed. Evidence:
  evidence/2026-08-24-lagarias-all/promote-run.txt.

## Next action
(a) TRACK D: robin-full-1e11.service ~11:45Z (41/100 subseg at 11:00Z,
    best_R=0.972015886980 at n=13967553600, unchanged): read
    evidence/2026-08-24-robin-1e11/full-run.txt (expect "ROBIN-FULL-1e11
    DONE rc=0" + final best_R), run pre-registered F1-F3b checks (see
    logs/2026-08-24.tick.log tick 184), promote claim (Robin full scan
    [1e10,1e11): max R, no witness R>=1).
(b) TRACK D: mertens-1e12 ~18:15Z (4400/10000 seg, maxabs=294816): F1-F6+
    C1-C7, M(1e12) vs OEIS A084237 a(12)=62366, promote record.
(c) TRACK D: zero scan ~08-27 (22.5%): F5a/b/c + F3/F4 + max/min g [1,1e5].
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(e) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to 7e12;
    Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push BLOCKED
    on RH-to-1e13 source.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko-zeros carded from landing page (full chapter behind AMS
  login); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. E: 4 NUMERIC (#10,#34,#35,#36) —
Lagarias attempt fully machine-verified; next E attempt next week (one per
week, frontier-escalated). D: 9 NUMERIC + 1 NOTE (#28), 3 scans in flight
(robin-full-1e11 ETA 11:45Z, mertens-1e12 ETA ~18:15Z, zero-scan ETA 08-27).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs
+ decide B next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to
2 sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
