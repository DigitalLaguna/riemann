# HANDOFF — session 2026-08-23 ~20:10 UTC (tick 152)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. TWO scans in flight: (1) S(t) scan [1,1e5] pid 732546,
36% at 19:31Z (120000/333331, elapsed 6688s; rate ~1700s/20000pts -> ETA
~00:30Z 08-24); (2) FULL zero scan [1,1e5] step 0.1 pid 743305, launched
20:00Z tick 152 (10000/999990 at 362s; ETA ~3-4 days, i.e. ~08-27/28 —
handoff-151's "~10h" was optimistic; cost model in tick log).

## Last work
Tick 152 (this one): (1) S(t) scan status — pid alive 100% CPU, last flush
"progress 120000/333331 (36%) elapsed 6688s"; result file still 0 bytes
(flushes at end). (2) Full-run falsification pre-registered BEFORE launch
(appended to tracks/d-search/zero-spacing-design.md): RvM main term at 1e5 =
138067.5584; F5a |count-main|<=6 PASS (O(log T)~11.5 makes ±3 too tight —
supersedes handoff-151's ±3 line); F5b 6<|Δ|<=50 -> re-run step 0.05;
F5c |Δ|>50 -> pipeline dead; F3/F4 carry over to [1,1e5]. No independent
fetched N(1e5) exists (checked lmfdb/wiki-zeta/wiki-rvm html: no N(10^n)
table; S(t) 1e4 zero count 9644 is aliased lower bound, step 0.5). (3)
LAUNCHED full zero scan: nohup python3 zero_scan.py 1.0 100000.0 0.1,
pid 743305, full.stderr "coarse 10000/999990 elapsed 362s". Launch quirk:
first attempt timed out the tool (bg proc held output pipe via stdin);
nohup process survived, single instance verified.

## Next action
(a) TRACK D (weight 15): check both scans: st_run-1e5.txt (ETA ~00:30Z 08-24)
    + zero-scan full.stderr progress. On S(t) completion: max|S|, zero count
    (cross-check: must be <= zero-scan count), max arg jump (< pi else step
    0.3 too large -> re-run smaller). mpmath = NOTE not NUMERIC.
(b) TRACK D: on zero-scan completion (~08-27/28): F5a/b/c + F3/F4 verdicts +
    records max/min g for [1,1e5] -> NOTE claim via promote.sh (pilot was
    [1,1e3]-scoped only).
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
In flight: S(t) scan [1,1e5] (36%, ETA ~00:30Z 08-24) + full zero scan [1,1e5]
(1%, ETA ~08-27/28). Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg
still the risk.
