# HANDOFF — session 2026-08-24 ~00:55 UTC (tick 165)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
28 claim rows: 15 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26,27),
3 FORMAL (A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK
lemmas v2), 10 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28).
Track D: 7 NUMERIC + 1 NOTE (#28 S(t) scan). ONE scan in flight:
FULL zero scan [1,1e5] step 0.1 zero-scan-1e5.service: 12.5% (125000/999990),
marginal 3.07 pts/s (overall 5.90). ETA CORRECTED this tick -> completion
~2026-08-29 08:00Z (range 08-28..08-29), NOT the old ~08-25 14:00Z. S(t) scan
[1,1e5] DONE rc=0 (claim #28).

## Last work
Tick 165 (this one): zero-scan ETA correction + cost-profile refinement.
Machine: zero-scan-1e5.service active (running) 6h, pid 745484 99.9% CPU;
full.stderr "coarse 125000/999990 elapsed 21185s". Marginal rate per 5000-pt
window dropped 4.98->3.86->3.07 pts/s between t=10501 and t=11501. Dense
re-measure of Z(t) (30dps, 10-rep warm, cost-profile-10k-30k.json) showed the
generic-regime cost is STEPPED not smooth: 31.4ms (t<=~10750) -> 49.5ms
(t~10750..~22500) -> 85ms (t~22500..~42000) -> 155ms plateau [44k,51k] -> 42ms
RS (>52k). The tick-156 profile linearly interpolated across these steps, so
the abrupt rate drop is the 31->49ms step (resolved, not an anomaly). Work
integration w(t)=cost(t)*[10+30*(1/2pi)ln(t/2pi)] with the REFINED profile:
model under-predicts by a STABLE factor (ratio 0.628 at t=5501, 0.644 at
t=12501; bisection=40 explains part ->0.809, residual ~1.24x unexplained).
Bias-corrected remaining = 459149s = 5.31d -> completion ~08-29 08:00Z.
The old "1.6d / 08-25" used the OVERALL average rate (6.418 pts/s), inflated
by cheap early points; marginal is 3.07 and still falling. Appended to
zeta-cost-profile.md (append-only). NOTE-grade (mpmath), no RH claim.

## Next action
(a) TRACK D (weight 15): zero scan completes ~08-29 08:00Z: read
    evidence/2026-08-23-zero-scan/full-run.txt for "ZERO-SCAN-1e5 DONE rc=0":
    F5a/b/c + F3/F4 verdicts + records max/min g [1,1e5] -> NOTE via promote.sh
    (pilot was [1,1e3]-scoped only). Cross-check: its zero count must be >=
    134011 (the S(t) sign-change lower bound). If completion falls outside
    [08-27,08-30], re-measure the cost profile (a step was missed / bias not
    constant).
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
In flight: full zero scan [1,1e5] (12.5%, ETA ~08-29 08:00Z, 5.3d remaining
bias-corrected; cost profile now stepped 31/49/85/155/42ms). S(t) scan DONE
(claim #28). Next review 2026-08-29 (week 2): milestone check + spot-check
3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR upstream +
Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
