# HANDOFF — session 2026-08-24 ~09:44 UTC (tick 182)
# track: E | gate: all tracks OPEN (21/21 seeds)

## State
36 claim rows: 19 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35; D: #20,21,22,
23,24,26,27,30,31), 3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 14 NOTE
(#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,#32,#33,#36). Track E
attempt (Lagarias SA restriction, macarevey-2026) nearly complete: F1a/F1b/F1c
(B_n inc to 1e10), F2/F2c (b-file==record-holders to 10810800), F3/F4 (Lagarias
on 55 SA n<=1e10) all PASS; F2b (no record-holder in (10810800,1e10]) RUNNING.
Extension claim #36 (Lagarias for ALL n<=1e10) staged as NOTE + check.sh.

## Last work
Tick 182: closed the (1e7,10810800) record-holder gap in the tick-177
  pre-registration. F2 stopped at n=1e7 (last holder 8648640); F2b's gaps
  start at a>=1e7 (first (10810800,21621600)); (1e7,10810800) was uncovered.
  F2c (exact int64 divisor-sum sieve to 10810800): 38 record-holders == 38
  b-file entries; only holder in (1e7,10810800] is 10810800 itself.
  VERDICT F2c: PASS (evidence/2026-08-24-lagarias-bseq/f2c-run.txt).
  => 10810800 is a record-holder, none in (8648640,10810800); gap CLOSED.
  Added NOTE #36 (Lagarias ALL n<=1e10) + evidence/2026-08-24-lagarias-all/
  check.sh (re-runs F1a,F1b,F1c,F2c,F2b,F3,F4; ~40 min, F2b-dominated).

## Next action
(a) TRACK E: F2b (lagarias-f2b.service, own cgroup, ~37 min elapsed, output
    buffered) — when f2b-run.txt shows "VERDICT F2b: PASS", run as a background
    unit: systemd-run --user --unit=lagarias-all-check.service bash -c 'cd
    /home/niklas/riemann && bash tools/promote.sh promote 36 NUMERIC
    evidence/2026-08-24-lagarias-all/ > evidence/2026-08-24-lagarias-all/
    promote-run.txt 2>&1'  (check.sh re-runs F2b ~40 min); verify #36->NUMERIC.
    If F2b DEAD -> #36 scoped to n<=10810800, F2b = the wall (DEAD_ENDS).
(b) TRACK D: mertens-1e12 ~08-24 19:10Z (3200/10000 seg, maxabs=207478):
    F1-F6+C1-C7, M(1e12) vs OEIS A084237 a(12)=62366, promote record.
(c) TRACK D: zero scan ~08-27 (21.5%): F5a/b/c + F3/F4 + max/min g [1,1e5].
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(e) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to 7e12;
    Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push BLOCKED
    on RH-to-1e13 source.

## Blocked
- #36 promotion: BLOCKED on F2b verdict (running, own unit, survives ticks)
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko-zeros carded from landing page (full chapter behind AMS
  login); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. E: 3 NUMERIC (#10,#34,#35) + #36
NOTE staged (F2b running). D: 9 NUMERIC + 1 NOTE (#28), 2 scans in flight.
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs
+ decide B next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2
sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
