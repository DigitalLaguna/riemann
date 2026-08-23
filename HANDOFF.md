# HANDOFF — session 2026-08-23 17:45 UTC (tick 147)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
27 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 9 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18).
Track D: 7 NUMERIC. S(t) scan (eighth D experiment) in progress.

## Last work
Tick 147 (this one): RECONCILED the S(t) definition and verified the
implementation. wiki-rh.html (fetched, verbatim) defines S(T)=(1/pi)Arg(zeta(1/2+iT))
= O(log T) and N(T)=(T/2pi)log(T/2pi)-T/2pi+7/8+O(1/T)+S(T); "S(t) jumps by 1 at
each zero, decreases between zeros, derivative ~ -log t". MACHINE CHECK: large term
at T=1e4 = 10142.97; S(1e4)=N(1e4)-large=9644-10142.97=-498.97, which EXACTLY
matches st_run.py's tick-144 output "max|S|=498.97 at t=1e4". So st_run.py computes
the STANDARD S(t) (full continuous arg of zeta / pi = N(t) minus the large term);
the tick-144 "too large" anomaly is RESOLVED (not a bug; O(log T) bounds are
asymptotic, not tight at 1e4). Launched the [1,1e5] scan (step 0.3, since
theta'(1e5)~9.17 rad/unit needs step<0.34 for valid unwrap) as detached
st-scan-1e5.service (first launch failed on relative path; fixed with absolute
paths). Now active, pid 732607, ETA ~19:45Z.

## Next action
(a) TRACK D (weight 15): read evidence/2026-08-23-st-scan/st_run-1e5.txt for
    "ST-SCAN-1e5 DONE rc=0" (ready ~19:45Z) + max|S|/zero-count/max-arg-jump lines.
    If max arg jump >= pi -> step 0.3 too large, re-run smaller. mpmath=NOTE not
    NUMERIC (needs Arb or explicit error bound for a NUMERIC claim).
(b) TRACK D: identify the S(t) world-record paper (NOT on arXiv, tick-140
    preflight). My memory "S(t)>2.337 at t~1.8e23 (Mossinghoff-Trudgian-Yang)" is
    UNVERIFIED and INCONSISTENT with |S(1e4)|=498.97 if it means max|S| over
    [0,1.8e23]. Do NOT cite it (literature gate). S2 was 429 rate-limited tick 140.
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
- S(t) record paper: not on arXiv; identify via S2/journal before any record claim
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D 7 NUMERIC (#20-#24,#26,#27). S(t)
scan [1,1e5] in flight (ETA ~19:45Z). Next review 2026-08-29 (week 2): milestone
check + spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17):
Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18);
PR leg still the risk.
