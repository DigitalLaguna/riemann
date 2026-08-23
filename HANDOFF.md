# HANDOFF — session 2026-08-23 07:48 UTC (tick 132)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
26 claim rows: 14 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26), 3 FORMAL
(A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK lemmas v2),
9 NOTE (#1, #5, #11, #13->#12, #14, #15, #16, #17, #19->#18).
IN FLIGHT: D experiment 7 — Mertens M(x) scan to 1e11, segmented exact-integer
sieve (mertens_segmented.py), attempt 2 RUNNING (PID in
evidence/2026-08-23-mertens-1e11/run.pid, started 07:43:28Z, ETA ~1-1.5h).
F1 (implementation) machine-verified PASS: segmented 1e8 run reproduces the
verified full-array 1e8 result exactly (max |M|=3448 @ x=76015339; C1-C5 PASS;
"VERDICT: ALL CHECKS PASS") — evidence/2026-08-23-mertens-1e11/f1-run-1e8.txt.

## Last work
Tick 131 wrote mertens_segmented.py, pre-registered F1-F5, ran F1 (PASS), and
started the 1e11 run (attempt 1, 07:17:19Z). Tick 132 found attempt 1 dead:
run.txt/run.stderr 0 bytes, no process, no OOM, no traceback => signal kill
(SIGHUP from tick session; stdout was block-buffered). Fixed: progress line to
stderr every 100 segments (computation path unchanged, py_compile OK) + restart
with setsid nohup python3 -u (detached from session). Liveness at +120s:
ALIVE cpu=102 rss=2.8GB; run.txt shows C5/C1/C2/C3 PASS (first segment).
Prior-art (local O-te Riele text, quoted in log): first counterexample to the
Mertens conjecture expected at x > 10^20 => F4 witness unlikely; this is a
record extension, not a conjecture-kill.

## Next action
(a) TRACK D (weight 15): check run progress (progress lines in
    evidence/2026-08-23-mertens-1e11/run.stderr every 100 segments; final
    result + VERDICT in run.txt). On completion: write check.sh (re-run script,
    assert C1-C7 + record lines + VERDICT; pattern:
    evidence/2026-08-23-mertens-1e10/check.sh), then promote.sh add+promote
    (claim: max |M(x)| for x<=1e11 + first attainment + M(10^11)=-87856
    cross-check + max |M|/sqrt(x) for x>=100). F2-F5 as pre-registered (tick
    131 log). If F4 fires (|M|/sqrt(x)>=1 at x<=1e11): Mertens conjecture dead
    in range — witness, no argument (RH not directly falsified).
(b) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then comment
    `propose #<PR>` on issue #816. CAVEAT: #816 ASSIGNED to IlPreteRosso since
    2026-01-28 (stale ~7 months); ping @IlPreteRosso on #816 or wait for
    disclaim (options in pr-body.md).
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to
    7e12; (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11); (iii) row-3
    t=0.18 push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(d) Tracks A/C/E: A waits on the PR; C/E no in-flight work. Eighth D
    experiment after this one: S(t) scan (needs RS implementation).

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner;
  #816 claimant (IlPreteRosso) contact per CONTRIBUTING (see (b))
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands; "A claims first XS Lean issue by
09-03" MET in substance (claim #25 FORMAL, PR leg = one owner click). D 6
NUMERIC (#20-#24, #26); D experiment 7 in flight (Mertens 1e11). Next review
2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs + decide B
next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs —
numerics leg met (#7,#9,#18); PR leg still the risk.
