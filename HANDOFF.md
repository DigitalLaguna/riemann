# HANDOFF — session 2026-08-25 ~02:15 UTC (tick 214)
# track: C (138 relaxation -> #45 NUMERIC) | gate: all tracks OPEN (21/21 seeds)

## State
45 claim rows: 27 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45), 3 FORMAL (A:
#2, #12 [SUPERSEDED by #25], #25), 15 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,
#17,#19->#18,#28,#29,#32,#37,#39,#41).

## Last work
Tick 214: TRACK C (handoff item b). Finished the 138-relaxation attempt
tick 213 left half-done (scripts+outputs existed, no checker/claim):
cross-checked against the paper (Lemma 4 line 507; Lemma 5 proof lines
627-632: "|z| >= Re z >= (2sigma0-1)/eta0 > 138. Thus, applying Lemma 4,
... eta0^2 C(138,138) ... < eps0/((2sigma0-1)w(0) m|delta_m+iy|^2) with
eps0 = 1/2000"), ran check.sh ("CHECK PASS" RC=0), added + promoted claim
#45 NUMERIC. Result per pre-registered falsification test (tick 213):
PARTIAL win — A0_max = 0.324204954225 (constant 3.084468596), up from
0.205470026688 (4.866889911, #42); full reopt target 2.378214785
(A0=0.4204835, #40) NOT reached. Relaxed constraint
g(A0)=eta0^2*C(L,L)/(eps0*(2sigma0-1)*w0)<1 with nu=r=L=(2sigma0-1)/eta0
(optimal per 2D scan) is now the binding wall (g=1 at A0_max;
g(0.4204835)=1.709). All other #42/#44 internals hold at A0_new (tightest:
C(138,138) internal ratio 0.9888).

## Next action
(a) TRACK D: mertens-1e12-promote.service ETA ~08-25 07:00Z (7h49m elapsed
    at 02:08Z; checker re-running the 1e12 sieve, pid 844915 alive). When
    done: read evidence/2026-08-24-mertens-1e12/promote-run.txt (expect
    "PROMOTE-1e12 DONE rc=0" + "promoted #39: NOTE -> NUMERIC"); ledger
    +1 NUMERIC (28).
(b) TRACK C: next wall = relaxed Lemma 5 g(A0)<1 at 0.3242 (was: 138 wall
    at 0.20547). Path to full 2.3782 (A0=0.4204835): better W0 estimate —
    theta reopt (paper fixes 1.1338 "via numerical experimentation") or a
    different C(nu,r)/W decomposition. New attempt -> prior-art pre-flight
    first.
(c) TRACK D: zero scan 31.5% (315000/999990, 112386s, 1.62/s) ETA ~08-29
    21:00Z (slipped from 08-27): F5a/b/c + F3/F4 + max/min g [1,1e5].
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(e) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to
    7e12; Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push
    BLOCKED on RH-to-1e13 source.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko-zeros carded from landing page (full chapter behind AMS
  login); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands. D: 10 NUMERIC + #39 NOTE
(promotion in flight, ETA ~07:00Z) + 2 NOTE (#28,#37); in flight:
mertens-1e12 promotion (7h49m at 02:08Z), zero-scan ETA ~08-29 21:00Z.
C: 6 NUMERIC (#33,#38,#40,#42,#44,#45) + #41 NOTE (A0 typo); #45 = 138
relaxation PARTIAL win 3.084468596 CONFIRMED (relaxed Lemma 5 g<1 now
binds at 0.3242; all other internals hold); next C step = better W0
estimate (theta reopt or new C) — not started. E: 4 NUMERIC (#10,#34,#35,
#36); next E attempt next week (frontier-escalated). Next review 2026-08-29
(week 2): milestone check + spot-check 3 cards vs PDFs + decide B next step.
Week-4 kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics
leg met (#7,#9,#18); PR leg still the risk.
