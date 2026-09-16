# HANDOFF — session 2026-09-16 ~00:02 UTC (tick 232)
# track: C (#51 rigorous A0_max lower bound) | gate: all tracks OPEN (21/21 seeds)

## State
51 claim rows: 31 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 17 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48,#51).

## Last work
Tick 232: TRACK C #50 follow-up — closed the 1.4e-11 rigor gap in #50. #50's
verified feasible A0 was 0.392113247327986, i.e. 1.4e-11 BELOW its recorded
0.392113247328 (the 12-digit claim rested on monotonicity, not direct
verification). Re-bisected the theta-cross to width 4.12e-11 (30dps, 30 iters;
true crossing 0.376216048444350 — the old 20-iter midpoint was off 2.5e-9) and
verified the H>=0 bisection endpoint (hi, A0_g(hi)) at 50/100dps + all 7
constraints. Machine PASS (263s, RC=0): RIGOROUS A0_max >= A0_g(hi) =
0.39211324739496 (14 digits), 1/A0 <= 2.55028364036; estimate A0_max ~
0.39211324739551. Margin 2.41e-14 (50dps == 100dps, real not noise). Recorded
NOTE #51 (stronger than #50, confirms it). check.sh repointed to the refined
checker; #51 promotion deferred to next tick (budget).

## Next action
(a) TRACK C: promote #51 -> NUMERIC (one-liner, checker already PASS, ~263s):
    tools/promote.sh promote 51 NUMERIC evidence/2026-09-15-zfree-theta-cross
(b) TRACK D: mertens-1e12-promote.service ETA ~09-16 08:00Z (full 1e12 sieve
    re-run ~10-12h; ~3.5h in at tick start). When done: read
    evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12 DONE
    rc=0" + #39 promoted); ledger +1 NUMERIC (32).
(c) TRACK D: zero-scan-1e5.service at 90000/999990 @ ~7.45/s (faster than the
    old 2.66/s estimate); ETA ~09-17 09:00Z (was 09-20). ckpt-1e5.json protects
    against reboot (worst case lose <=5000 steps).
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816.
(e) TRACK B (weight 40): PARKED: X-sweep to 7e12; Arb-port of 0.20 pipeline
    (promotes NOTE #11); row-3 t=0.18 push BLOCKED on RH-to-1e13 source.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner
- S(t) record paper: not on arXiv; inoue-kobayashi-toma-2025 closest on-arXiv
  (carded); odlyzko zero-data page 404 -> zero scan computes zeros itself
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)
- OWNER: machine down 3 weeks (08-25 -> 09-15); weekly reviews missed;
  week-4 kill decision (09-17) pending owner call

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands (no weekly review ran 08-29..09-15).
D: 10 NUMERIC + #39 NOTE (promotion in flight, ETA ~09-16 08:00Z) + 3 NOTE
(#28,#37,#48); in flight: mertens-1e12 promotion, zero-scan ETA ~09-17 09:00Z.
C: 10 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50) + #51 NOTE (rigorous
A0_max >= 0.39211324739496, promote next tick) + #41 NOTE (A0 typo) + #48 NOTE
(exact m=0 MARGINAL); next C step = promote #51, then optional 50dps-bisection
tightening (width -> 1e-15) or a larger-theta point for a comfortable margin.
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25); PR leg still the risk (owner). Next review: week-4
kill decision 09-17 — owner to decide continue/reweight/kill with this handoff.
