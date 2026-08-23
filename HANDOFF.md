# HANDOFF — session 2026-08-23 08:57 UTC (tick 134)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
26 claim rows: 14 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26), 3 FORMAL
(A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK lemmas v2),
9 NOTE (#1, #5, #11, #13->#12, #14, #15, #16, #17, #19->#18). No new claims this tick.
IN FLIGHT: D experiment 7 — Mertens M(x) scan to 1e11, ATTEMPT 3 (pid 700783,
started 08:11:04Z under transient systemd unit mertens-1e11.service). At 600/1000
segments (08:47Z), maxabs=87995 and climbing; ETA finish ~09:15Z. OUTPUT GOES TO
THE SYSTEMD JOURNAL (fd1+fd2 -> journal socket), NOT run3.txt. A detached watcher
(pid 703261, setsid, session leader) is waiting for pid 700783 to exit, then:
journalctl _PID=700783 --output=cat > run3.txt, then bash check.sh > check-run.txt
(check.sh re-runs the exact-integer scan ~72 min, asserts C1-C7 + record/witness
determinism + F4 witness<1.0 + F5 maxabs>=50286), logging to watch.log.
F1 (implementation) machine-verified PASS (tick 131/132): segmented 1e8 run
reproduces the verified full-array 1e8 result exactly (evidence/.../f1-run-1e8.txt).

## Last work
Tick 134 (this one): found the handoff stale at tick 132 — tick 133 had restarted
the run as attempt 3 under systemd + written check.sh (residual commit 2edca8c) but
had NOT appended to the daily log nor rewritten HANDOFF.md. Diagnosed attempt-3's
output location: /proc/700783/fd shows fd1+fd2 -> socket (systemd journal), so
run3.txt stayed 0 bytes; the transient unit is gone from `systemctl`, so output is
retrieved by PID. Machine-verified liveness via `journalctl _PID=700783
--output=cat`: C5/C1/C2/C3 all PASS + progress 100->600/1000 segments (maxabs
50286->60442->62880->81220->81220->87995). F5 LOCKED: maxabs 87995 > 50286 (1e10
record #24) => final max |M|(1e11) > 50286 => first attainment MUST be > 1e10.
Installed + verified the detached watcher (pid 703261 alive, sleep-30 child); killed
a leftover bash wrapper (703257) that had held the tool pipe (600s timeout); watcher
reparented and still alive.

## Next action
(a) TRACK D (weight 15): read evidence/2026-08-23-mertens-1e11/watch.log for
    "WATCHER DONE rc=0" and check-run.txt for "CHECK PASS: Mertens record at
    10^11". (check-run.txt ready ~10:30Z.) If PASS: promote.sh add+promote
    (claim: max |M(x)| x<=1e11 + first attainment (>1e10) + M(10^11)=-87856
    cross-check + max |M|/sqrt(x) x>=100). If F4 fired (witness>=1.0): Mertens
    conjecture dead in range (witness, no argument; RH not directly falsified) —
    page owner. If rc!=0: debug from check-run.txt + watch.log.
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
(#20-#24, #26); D experiment 7 attempt 3 in flight (Mertens 1e11, watcher armed).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs +
decide B next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig
figs — numerics leg met (#7,#9,#18); PR leg still the risk.
