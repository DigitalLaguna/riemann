# HANDOFF — session 2026-08-23 10:47 UTC (tick 138)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 14 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 10 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18, #27).
NEW: #27 NOTE (D Mertens record 1e11) — promote to NUMERIC IN FLIGHT.
IN FLIGHT: promote.sh promote 27 NUMERIC (checker re-runs full 1e11 scan,
started 10:45:33Z under mertens-promote.service persistent cgroup, ~70 min)
-> promote-run.txt + watch.log "PROMOTE DONE rc=N". ETA ~11:55Z.
DETERMINISM RE-RUN DONE 10:31:16Z: check.sh rc=0, CHECK PASS (record 94909
first at x=99481473379, M(10^11)=-87856, witness 0.570590889<1.0 reproduced
exactly vs run3.txt).

## Last work
Tick 138 (this one): determinism re-run (check.sh, started 09:21:22Z under
mertens-watcher.service) finished 10:31:16Z — check.sh rc=0, CHECK PASS,
C1-C7 ALL PASS. diff of record/witness/VERDICT lines run3.txt vs check-run.txt:
re-run raw output IDENTICAL to run3.txt (only delta = check.sh's own appended
"recorded:" summary). F4 witness 0.570590889 < 1.0 (Mertens conjecture alive
in [100,1e11]); F5 maxabs 94909 >= 50286 (1e10 record #24). Bounded step:
promote.sh add -> NOTE #27; launched promote.sh promote 27 NUMERIC via
systemd-run --user --unit=mertens-promote.service (persistent cgroup; same
protection that saved the watcher). Scan pid 712137 alive.

## Next action
(a) TRACK D (weight 15): read evidence/2026-08-23-mertens-1e11/watch.log for
    "PROMOTE DONE rc=0" and promote-run.txt for "promoted #27: NOTE -> NUMERIC"
    (ready ~11:55Z). If rc=0: #27 is NUMERIC (7th D NUMERIC). If rc!=0: debug
    promote-run.txt + watch.log. Then eighth D experiment: S(t) scan (needs RS
    implementation).
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
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 6 NUMERIC (#20-#24,#26) + #27
promote in flight (ETA ~11:55Z). Next review 2026-08-29 (week 2): milestone
check + spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17):
Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18);
PR leg still the risk.
