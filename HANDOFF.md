# HANDOFF — session 2026-08-24 ~01:40 CEST (tick 163)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
28 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 10 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28).
Track D: 7 NUMERIC + 1 NOTE (#28 S(t) scan). ONE scan in flight:
FULL zero scan [1,1e5] step 0.1 zero-scan-1e5.service: 11.5% (115000/999990),
rate 6.418 pts/s, linear ETA 38.3h -> completion ~2026-08-25 14:00Z (cost drops
2x at t>52k so actual ETA <= 1.6d). S(t) scan [1,1e5] DONE rc=0 (21:11:10Z).

## Last work
Tick 163 (this one): S(t) scan completion confirmed + anomaly closure. Ticks
158-162 lost to timeout/crash without checking the S(t) scan (ETA was 21:25Z).
Machine: st_run-1e5.txt "ST-SCAN-1e5 DONE rc=0 2026-08-23T21:11:10Z"; max
|(1/pi)unwrap(arg zeta(1/2+it))| = 4059.01503522 at t=99996.4; zero count (sign
changes of Z, lower bound) = 134011; max arg jump 3.0209 rad < pi (step 0.3
valid). Result already claim #28 (NOTE, tick 159, committed). ANOMALY (c7):
#28 text "gap 3056" is a transposed-digit typo — 138067.558-134011 = 4056.56
(RvM main term recomputes to 138068.558, gap 4057.56); gap = ~4057 missed zeros
(close pairs in one 0.3-interval -> no sign change). RESOLVED in log; NOTE has
no authority, main result unaffected. Zero-scan ETA re-estimated 11.5% -> ~08-25
14:00Z (supersedes tick-156 3.46d, which assumed generic-regime cost throughout).

## Next action
(a) TRACK D (weight 15): zero scan completes ~08-25 14:00Z: read
    evidence/2026-08-23-zero-scan/full-run.txt for "ZERO-SCAN-1e5 DONE rc=0":
    F5a/b/c + F3/F4 verdicts + records max/min g [1,1e5] -> NOTE via promote.sh
    (pilot was [1,1e3]-scoped only). Cross-check: its zero count must be >=
    134011 (the S(t) sign-change lower bound).
(b) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then comment
    `propose #<PR>` on issue #816. CAVEAT: #816 ASSIGNED to IlPreteRosso since
    2026-01-28 (stale ~7 months); ping @IlPreteRosso on #816 or wait for disclaim.
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12;
    (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11); (iii) row-3 t=0.18
    push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(d) Tracks A/C/E: A waits on the PR; C/E no in-flight work.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner;
  #816 claimant (IlPreteRosso) contact per CONTRIBUTING (see (b))
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 (2025/26) is the
  closest on-arXiv reference for extreme arg / r-gaps — NOW CARDED
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page;
  odlyzko personal zero-data page 404 (evidence/2026-08-23-st-scan/odlyzko-*.html)
  -> zero scan computes zeros itself (pilot validated)
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 7 NUMERIC + 1 NOTE (#28).
In flight: full zero scan [1,1e5] (11.5%, ETA ~08-25 14:00Z, <=1.6d). S(t) scan
DONE (claim #28). Next review 2026-08-29 (week 2): milestone check + spot-check
3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR upstream +
Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
