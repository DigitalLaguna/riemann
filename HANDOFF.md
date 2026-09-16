# HANDOFF — session 2026-09-16 ~00:25 UTC (tick 233)
# track: C (#51 promoted) | gate: all tracks OPEN (21/21 seeds)

## State
51 claim rows: 32 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51),
3 FORMAL (A: #2, #12 [SUPERSEDED by #25], #25), 16 NOTE (#1,#5,#11,#13->#12,
#14,#15,#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48).

## Last work
Tick 233: TRACK C — promoted #51 NOTE -> NUMERIC. promote.sh re-ran the
refined checker (check_theta_cross_fine.py): PASS (261.6s, RC=0). RIGOROUS
A0_max >= A0_g(hi) = 0.39211324739496 (14 digits), 1/A0 <= 2.55028364036;
estimate A0_max ~ 0.392113247395509. C now has 11 NUMERIC; ledger 32 NUMERIC.

## Next action
(a) TRACK D: mertens-1e12-promote.service in flight (4h1m at tick start; full
    1e12 sieve re-run ~10-12h; ETA ~09-16 08:00Z). When done: read
    evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12 DONE
    rc=0" + #39 promoted); ledger +1 NUMERIC (33).
(b) TRACK D: zero-scan-1e5.service at 100000/999990 @ ~7.1/s (14092s elapsed);
    ETA ~09-17 11:30Z (slightly slower than the 09:00Z estimate). ckpt-1e5.json
    protects against reboot (worst case lose <=5000 steps).
(c) TRACK C optional: 50dps bisection tightening (width 4.12e-11 -> 1e-15) to
    pin A0_max to ~15 digits, or a slightly-larger-theta point for a
    comfortable margin.
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
(#28,#37,#48); in flight: mertens-1e12 promotion, zero-scan ETA ~09-17 11:30Z.
C: 11 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47,#49,#50,#51) + #41 NOTE (A0 typo)
+ #48 NOTE (exact m=0 MARGINAL); next C step = optional tightening above.
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
A: 3 FORMAL (#2,#12,#25); PR leg still the risk (owner). Next review: week-4
kill decision 09-17 — owner to decide continue/reweight/kill with this handoff.
