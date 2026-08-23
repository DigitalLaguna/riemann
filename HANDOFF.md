# HANDOFF — session 2026-08-23 ~20:10 CEST (tick 156)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. TWO scans in flight (both own systemd units, verified active,
99.9% CPU each, 48-core box load 3 -> no contention):
(1) S(t) scan [1,1e5] st-scan-1e5.service pid 732546: 66% (220000/333331),
elapsed 15066s. ETA ~21:25 UTC 08-23 (1.34h left) — MACHINE-MEASURED.
(2) FULL zero scan [1,1e5] step 0.1 zero-scan-1e5.service pid 745484: 5.5%
(55000/999990), elapsed 5210s. ETA ~08-27 ~09:00 UTC (3.46d left) — MACHINE-
INTEGRATED. (5.5% of points = 1.7% of total work; early pts cheap.)

## Last work
Tick 156 (this one): ETA refinement + anomaly closure. Tick-155 S(t) rate had
dropped 2.5x (0.1094->0.042 s/pt) — an unexplained mismatch (blocks per
constraint 7). MEASURED mpmath zeta(0.5+it) cost at 30 dps across t: it is
NON-MONOTONIC — generic 0.8-86ms (t<44k), 155ms PLATEAU (t in [44k,51k]), then
42ms RS regime (t>52k, flat to 1e5). Scan segment rates 0.085/0.137/0.109/0.042
match the profile exactly -> anomaly RESOLVED (mpmath property, not noise).
Mechanism (source quoted): zeta.py:558-560 dispatches to rs_zeta when
|im|>500*prec (t>50000 at prec=100 bits/30dps). Re-integrated zero-scan work
with the measured profile: REMAINING 83.1h (was 5.1d by power-law, which
over-estimated because cost DROPS 2x at t>52k). S(t) remaining 113331 pts all in
42ms regime = 1.34h. No new claims (both scans in flight; mpmath = NOTE when done).
Evidence: evidence/2026-08-23-zero-scan/zeta-cost-profile.md (table + citation +
integration + falsification).

## Next action
(a) TRACK D (weight 15): S(t) scan completes ~21:25 UTC 08-23: read
    evidence/2026-08-23-st-scan/st_run-1e5.txt for "ST-SCAN-1e5 DONE rc=0":
    max|S|, zero count (cross-check: must be <= zero-scan count), max arg jump
    (< pi else step 0.3 too large -> re-run smaller). mpmath = NOTE.
(b) TRACK D: zero scan: re-estimate ETA at 10% (next flush ~100000/999990,
    t=10001). On completion: F5a/b/c + F3/F4 verdicts + records max/min g
    [1,1e5] -> NOTE claim via promote.sh (pilot was [1,1e3]-scoped only).
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
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page;
  odlyzko personal zero-data page 404 (evidence/2026-08-23-st-scan/odlyzko-*.html)
  -> zero scan computes zeros itself (pilot validated)
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 7 NUMERIC (#20-#24,#26,#27).
In flight: S(t) scan [1,1e5] (66%, ETA ~21:25Z 08-23) + full zero scan [1,1e5]
(5.5%, ETA ~08-27 09:00Z). Both ETAs now machine-based (measured cost profile,
evidence/2026-08-23-zero-scan/zeta-cost-profile.md). Next review 2026-08-29
(week 2): milestone check + spot-check 3 cards vs PDFs + decide B next step.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg
met (#7,#9,#18); PR leg still the risk.
