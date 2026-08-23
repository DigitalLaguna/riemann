# HANDOFF — session 2026-08-23 09:55 UTC (tick 136)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
26 claim rows: 14 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26), 3 FORMAL
(A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK lemmas v2),
9 NOTE (#1, #5, #11, #13->#12, #14, #15, #16, #17, #19->#18). No new claims this tick.
IN FLIGHT: D experiment 7 — Mertens M(x) scan to 1e11, RUN DONE 09:21:22Z (attempt 3,
pid 700783). run3.txt captured (43 lines): C1-C7 ALL PASS, VERDICT: ALL CHECKS PASS.
RECORD: max |M(x)| x<=1e11 = 94909, first at x = 99481473379 (M = -94909);
M(10^11) = -87856 (OEIS A084237); F4 witness max |M|/sqrt(x) x>=100 = 0.570590889
at x = 7766842813 (M = 50286) < 1.0 (Mertens conjecture alive in range).
Independent mu check at record location PASS 9/9 (tracks/d-search/mu_direct.py;
mu(99481473379) = -1; evidence/.../mu-direct-check.txt).
NOW: determinism re-run check.sh (pid 705988, started 09:21:22Z, ~70 min) ->
check-run.txt (0 bytes until done), then watch.log gets "check.sh rc=N" +
"WATCHER DONE rc=N". ETA ~10:32Z. Watcher pid 705251 alive (mertens-watcher.service,
persistent cgroup).

## Last work
Tick 136 (this one): run finished 09:21:22Z (70m18s; ETA 09:25Z was right). Watcher
captured run3.txt from journal; all internal checks PASS (C1 M(10); C2 OEIS A002321
n<=1e4; C3 sympy n<=1e5; C4 OEIS A051402 envelope; C5 segmented==full mu n<=1e6;
C6 M(1e11)=-87856 vs OEIS A084237; C7 M(10^k) k<=10 vs verified 1e10 run). New record
94909 > 1e10 record 50286 (#24); first attainment 9.948e10 (> 1e10), in the last
segment (progress flat at 87995 through 900/1000). Bounded step this tick: independent
direct-factorization mu check at the record location (mu_direct.py, primes <= 316228,
all 9 implications of the top-10 list) — 9/9 PASS, rc=0. Pre-registered falsification:
any mu mismatch => record location suspect. Did not fire.

## Next action
(a) TRACK D (weight 15): read evidence/2026-08-23-mertens-1e11/watch.log for
    "WATCHER DONE rc=0" and check-run.txt for "CHECK PASS: Mertens record at
    10^11" (ready ~10:32Z). If PASS: promote.sh add+promote (claim: max |M(x)|
    x<=1e11 = 94909 first at x=99481473379 (M=-94909) + M(10^11)=-87856
    cross-check + witness 0.570590889<1.0 at x=7766842813). If F4 fired
    (witness>=1.0): Mertens conjecture dead in range (witness, no argument;
    RH not directly falsified) — page owner. If rc!=0: debug check-run.txt+watch.log.
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
(#20-#24, #26); D experiment 7 run DONE, determinism re-run in flight (ETA ~10:32Z)
— promotion next tick if PASS. Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg still
the risk.
