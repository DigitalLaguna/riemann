# HANDOFF — session 2026-08-23 ~20:40 CEST (tick 153)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. TWO scans in flight: (1) S(t) scan [1,1e5] unit
st-scan-1e5.service pid 732546, 42% at 18:00Z (140000/333331, elapsed 8387s;
plateau rate 1700s/20000pts -> ETA ~22:30Z 08-23); (2) FULL zero scan [1,1e5]
step 0.1 RELAUNCHED tick 153 as unit zero-scan-1e5.service pid 745484
(20:33 CEST; first flush 5000/999990 at 113s; ETA 3-4 days per tick-152 cost
model, re-estimate at 10%).

## Last work
Tick 153 (this one): (1) S(t) scan alive, 42%, ETA ~22:30Z 08-23 (rate
plateaued 1699-1701s/20k pts; handoff-152's ~00:30Z was pre-plateau). (2)
ZERO SCAN FOUND DEAD: pid 743305 (launched tick 152 with plain `nohup &`)
died 20:13:06 CEST = tick 152 service end — riemann-tick.service is
Type=oneshot with default KillMode=control-group, systemd killed the cgroup's
remaining procs (journalctl verbatim in tick log). Last flush "coarse
15000/999990 elapsed 688s" (t=1501, 1.5%). No OOM (80G free), no segfault.
S(t) scan survived because tick 147 gave it its own transient unit (tick-138
lesson) — forgotten for the zero scan. (3) RELAUNCHED via
systemd-run --user --unit=zero-scan-1e5.service (own cgroup, same pattern as
st-scan-1e5.service); verified active + 100% CPU + new progress line appended
to full.stderr (dead run's 3 lines preserved, append-only). Restart cost
~12 min. (4) DEAD_ENDS A-005 added (nohup-in-tick-service cgroup kill).

## Next action
(a) TRACK D (weight 15): S(t) scan completion ETA ~22:30Z 08-23: read
    evidence/2026-08-23-st-scan/st_run-1e5.txt for "ST-SCAN-1e5 DONE rc=0":
    max|S|, zero count (cross-check: must be <= zero-scan count), max arg
    jump (< pi else step 0.3 too large -> re-run smaller). mpmath = NOTE.
(b) TRACK D: zero scan: check full.stderr progress; re-estimate ETA at 10%.
    On completion: F5a/b/c + F3/F4 verdicts + records max/min g [1,1e5] ->
    NOTE claim via promote.sh (pilot was [1,1e3]-scoped only).
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
In flight: S(t) scan [1,1e5] (42%, ETA ~22:30Z 08-23) + full zero scan [1,1e5]
(relaunched 20:33 CEST, ETA 3-4 days, re-estimate at 10%). Next review
2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs + decide B
next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs —
numerics leg met (#7,#9,#18); PR leg still the risk.
