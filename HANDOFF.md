# HANDOFF — session 2026-08-25 ~00:10 UTC (tick 210)
# track: C (A0_max internal audit -> #44 NUMERIC) | gate: all tracks OPEN (21/21 seeds)

## State
44 claim rows: 26 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44), 3 FORMAL (A: #2,
#12 [SUPERSEDED by #25], #25), 15 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,
#19->#18,#28,#29,#32,#37,#39,#41). This tick: +1 NUMERIC (#44 A0_max internal
audit CONFIRMS #42 PARTIAL win 4.866889911: Lemma 5 internals + Lemma 6
A-range all hold at A0_max=0.205470026688; tick 208's pre-registered
falsification test did NOT fire).

## Last work
Tick 210: TRACK C completion. Ticks 208-209 had already built + run
a0max_internal_audit.py (zfree-a0max, mpmath 60 dps) but the log entry ended
at the falsification test and no ledger row existed. This tick: (a) ran
zfree-a0max/check_internal.sh -> "CHECK PASS (internal)" RC=0; (b) created
evidence/2026-08-24-zfree-a0max-internal/ with its own check.sh (re-runs the
CANONICAL script in zfree-a0max, single copy; avoids the #42 checker/claim
mismatch) + machine-run.txt + check-run.txt -> "CHECK PASS (a0max internal)"
RC=0; (c) promote.sh add -> NOTE #44, promote 44 NUMERIC -> checker re-ran
PASS, "promoted #44: NOTE -> NUMERIC". Machine values: C(138,138)=21.57083788;
eta0^2*C(138,138) LHS 0.001103325869 < RHS 0.002799393866 (binds at A0=
0.326015468165 > A0_max); B(y)>0 (p real roots u=-1027.94, -35.15, both <0);
eq-22 W0-term 0.002167743713 < 5.7e10 (ratio 3.8e-14); A0_max > 1/6.

## Next action
(a) TRACK C: path to full 2.3782 = raise A0 past 0.20547, i.e. relax Lemma 5's
    |z|>=138 requirement itself (new attempt -> prior-art pre-flight first).
(b) TRACK D: mertens-1e12-promote.service still running (5h36m at 23:55Z;
    checker re-running the 1e12 sieve). When done: read
    evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + "promoted #39: NOTE -> NUMERIC"); ledger +1 NUMERIC.
(c) TRACK D: zero scan 30% (300000/999990, 103116s elapsed) ETA ~08-27 18:00Z:
    F5a/b/c + F3/F4 + max/min g [1,1e5].
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(e) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to 7e12;
    Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push BLOCKED
    on RH-to-1e13 source.
(f) GARDEN (weekly): dedupe a0max_audit.py across zfree-a0-audit (a0max_audit.py,
    check_a0max.sh) and zfree-a0max (canonical for #42) — keep zfree-a0max.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko-zeros carded from landing page (full chapter behind AMS
  login); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D: 10 NUMERIC + #39 NOTE
(promotion in flight) + 2 NOTE (#28,#37); in flight: mertens-1e12 promotion
(running since 18:18Z), zero-scan ETA ~08-27 18:00Z. C: 5 NUMERIC
(#33,#38,#40,#42,#44) + #41 NOTE (A0 typo); #42+#44 = A0_max PARTIAL win
4.866889911 CONFIRMED (Lemma 5 main binds; all internals hold); next C step =
attack Lemma 5's 138 requirement (path to full 2.3782) — not started.
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs
+ decide B next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to
2 sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
