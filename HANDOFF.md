# HANDOFF — session 2026-08-23 09:13 UTC (tick 135)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
26 claim rows: 14 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26), 3 FORMAL
(A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK lemmas v2),
9 NOTE (#1, #5, #11, #13->#12, #14, #15, #16, #17, #19->#18). No new claims this tick.
IN FLIGHT: D experiment 7 — Mertens M(x) scan to 1e11, ATTEMPT 3 (pid 700783,
started 08:11:04Z, unit mertens-1e11.service ACTIVE). At 800/1000 segments
(09:10Z), maxabs=87995 (flat since 600/1000); ETA finish ~09:25Z. OUTPUT GOES TO
THE SYSTEMD JOURNAL (fd1+fd2 -> journal socket), NOT run3.txt. Watcher pid 705251
(unit mertens-watcher.service, ACTIVE, own persistent cgroup) waits for 700783,
then: journalctl _PID=700783 --output=cat > run3.txt, then bash check.sh >
check-run.txt (check.sh re-runs exact-integer scan ~72 min, asserts C1-C7 +
record/witness determinism + F4 witness<1.0 + F5 maxabs>=50286), logs to watch.log.
F1 (implementation) machine-verified PASS (tick 131/132): segmented 1e8 run
reproduces the verified full-array 1e8 result exactly (evidence/.../f1-run-1e8.txt).

## Last work
Tick 135 (this one): found the tick-134 watcher (pid 703261) DEAD while the run
was alive at 800/1000. Root cause machine-verified: watcher was launched from the
tick-134 shell, so it sat in the tick's transient cgroup (riemann-tick.service);
scope reclaim killed it — setsid gives a new session, not a new cgroup. Run
survived (own unit mertens-1e11.service, still active — tick-134 handoff's claim
that the unit was gone was wrong). Fix: appended death note to watch.log, made
watch.sh line 11 append-only (sed over-matched >> to >>>; fixed, bash -n PASS),
relaunched via systemd-run --user --unit=mertens-watcher.service (2 failed
attempts: relative path exit 127; lingering unit, reset-failed). Verified:
watcher pid 705251 active, cgroup app.slice/mertens-watcher.service, watch.log
ends "watcher started 2026-08-23T09:11:52Z waiting for pid 700783".
LESSON: launch detached helpers from systemd-run --user (own unit), never from
the tick shell, even with setsid+nohup.

## Next action
(a) TRACK D (weight 15): read evidence/2026-08-23-mertens-1e11/watch.log for
    "WATCHER DONE rc=0" and check-run.txt for "CHECK PASS: Mertens record at
    10^11". (check-run.txt ready ~10:40Z.) If PASS: promote.sh add+promote
    (claim: max |M(x)| x<=1e11 + first attainment (>1e10) + M(10^11)=-87856
    cross-check + max |M|/sqrt(x) x>=100). If F4 fired (witness>=1.0): Mertens
    conjecture dead in range (witness, no argument; RH not directly falsified)
    — page owner. If rc!=0: debug from check-run.txt + watch.log.
(b) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then comment
    `propose #<PR>` on issue #816. CAVEAT: #816 ASSIGNED to IlPreteRosso since
    2026-01-28 (stale ~7 months); ping @IlPreteRosso on #816 or wait for disclaim.
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12;
    (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11); (iii) row-3 t=0.18 push
    — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(d) Tracks A/C/E: A waits on the PR; C/E no in-flight work. Eighth D experiment
    after this one: S(t) scan (needs RS implementation).

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner;
  #816 claimant (IlPreteRosso) contact per CONTRIBUTING (see (b))
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands; "A claims first XS Lean issue by 09-03"
MET in substance (claim #25 FORMAL, PR leg = one owner click). D 6 NUMERIC
(#20-#24, #26); D experiment 7 attempt 3 in flight (Mertens 1e11, watcher armed
under persistent unit). Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg still
the risk.
