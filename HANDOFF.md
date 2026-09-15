# HANDOFF — session 2026-09-15 ~23:30 UTC (tick 231)
# track: C (record + promote tick 230 theta-cross) | gate: all tracks OPEN (21/21 seeds)

## State
50 claim rows: 31 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 16 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48).

## Last work
Tick 231: recorded + promoted tick 230's theta-cross result (tick 230 ran it
but left the log incomplete and recorded no claim). Built a self-contained
checker (evidence/2026-09-15-zfree-theta-cross/check_theta_cross.py + check.sh)
that re-runs the 3x3-probe bisection to recover the full-precision crossing,
then verifies the 7x9 fine fulltotal + 100dps corner + all 7 constraints.
Machine PASS (198.5s, RC=0): theta_cross=0.37621605098082137139, A0=A0_g=
0.392113247327986, 1/A0=2.5502836408, min fulltotal 3.999e-12 (knife-edge),
all 7 constraints True. Promoted #50 NOTE -> NUMERIC. Result: A0_max >=
0.392113247328 (constant 1/A0 <= 2.5502836408), improving #47's
0.350566297741 (2.852527486); a lower bound at the grid crossing, does NOT
reach #46's infeasible 0.3967 (2.5207) nor #40's target 0.4205 (2.3782).
Both in-flight D jobs still running (mertens 3h00m in, zero-scan checkpointed).

## Next action
(a) TRACK D: mertens-1e12-promote.service ETA ~09-16 08:00Z (full 1e12 sieve
    re-run ~10-12h). When done: read evidence/2026-08-24-mertens-1e12/
    promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + #39 promoted); ledger
    +1 NUMERIC (32).
(b) TRACK D: zero-scan-1e5.service ETA ~09-20 04:00Z (999990 steps @ ~2.66/s);
    ckpt-1e5.json protects against reboot (worst case lose <=5000 steps).
(c) TRACK C: #50 is a lower bound at the grid crossing (fulltotal = +4e-12
    knife-edge). Follow-up: (i) finer (mu,eta) grid / higher-dps re-verify to
    confirm robustness + pin A0_max tighter; (ii) slightly-larger-theta point
    for a comfortable margin (smaller A0). New attempt -> prior-art pre-flight
    first.
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
(#28,#37,#48); in flight: mertens-1e12 promotion, zero-scan ETA ~09-20
04:00Z (checkpointed). C: 10 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50)
+ #41 NOTE (A0 typo) + #48 NOTE (exact m=0 MARGINAL); next C step = #50
follow-up (finer grid / higher-dps robustness) — not started. E: 4 NUMERIC
(#10,#34,#35,#36); next E attempt next week (frontier-escalated). A: 3 FORMAL
(#2,#12,#25); PR leg still the risk (owner). Next review: week-4 kill decision
09-17 — owner to decide continue/reweight/kill with this handoff.
