# HANDOFF — session 2026-08-24 ~08:05 UTC (tick 179)
# track: E | gate: all tracks OPEN (21/21 seeds)

## State
34 claim rows: 18 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34; D: #20,21,22,23,24,
26,27,30,31), 3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 13 NOTE
(#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,#32,#33). Track E attempt
in flight (Lagarias SA restriction, macarevey-2026): F3+F4 DONE (#34 NUMERIC),
F1a/F1b/F2/F2b pending. Two scans in flight: mertens-1e12.service 20.0%
(2000/10000 seg, maxabs=170358, ETA ~08-24 19:10Z); zero-scan-1e5.service 20.5%
(205000/999990, 0.312 s/step, ETA ~08-27 04:00Z, validity window [08-27,08-30]).

## Last work
Tick 179: E attempt step 2 (tick 177 spec+pre-reg, tick 178 b-file fetch):
  b-file sanity: 55 plain-int SA entries <= 1e10, strictly increasing,
    last = 6983776800 == argmax of claim #31 (consistent).
  wrote tracks/e-rh/lagarias_sa_check.py; first run F4 DEAD (my sigma_trial
    bug: k=d should be k=1, missing d^1; n=4 trial=13 vs sympy=7); fixed,
    spot-checked on 216 values (0 mismatches).
  re-run (evidence/2026-08-24-lagarias-sa/f3f4-run.txt):
    F4: sigma cross-check 55/55 (trial division vs sympy): PASS
    F3: NO WITNESS among 55 SA n <= 1e10; min margin 0.3171685434... at n=2
        (100 digits; 150-dps re-eval agrees to ~34 digits)
  check.sh: CHECK PASS -> promoted #34 NOTE -> NUMERIC (scoped to the 55
    b-file entries; extension to ALL n <= 1e10 awaits F1a/F1b + F2/F2b).

## Next action
(a) TRACK E: F1a (B_{n+1}-B_n > 0 for 1<=n<=54 at 100 digits; B_n =
    (H_n + e^{H_n} log H_n)/n) + F1b (B_n strictly increasing to 1e7, float64
    EM + 100-digit spot checks); then F2 (b-file == strict sigma(n)/n record
    holders n <= 1e7, exact sieve) + F2b (no record holder in (1e7,1e10]
    between consecutive b-file entries). All pass -> promote extension claim
    (Lagarias holds for all n <= 1e10).
(b) TRACK D: mertens-1e12 completes ~08-24 19:10Z: read run.txt for
    "MERTENS-1e12 DONE rc=0", run F1-F6 + C1-C7 (M(1e12) vs OEIS A084237
    a(12)=62366), promote record (max |M(x)| at 1e12 + first-attainment x).
(c) TRACK D: zero scan completes ~08-27 04:00-11:00Z (window [08-27,08-30]):
    F5a/b/c + F3/F4 verdicts + max/min g [1,1e5] -> NOTE via promote.sh.
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
Week-1 reweight A30/B40/D15/C10/E5 stands. E: 1 NUMERIC (#34) + attempt in
flight (F1a/F1b/F2/F2b pending). D: 9 NUMERIC + 1 NOTE (#28), 2 scans in
flight. Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards
vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR upstream +
Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
