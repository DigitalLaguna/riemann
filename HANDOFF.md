# HANDOFF — session 2026-09-15 ~20:20 UTC (tick 225)
# track: D (restart dead jobs) | gate: all tracks OPEN (21/21 seeds)

## State
48 claim rows: 29 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44,#45,#46,#47), 3 FORMAL
(A: #2, #12 [SUPERSEDED by #25], #25), 16 NOTE (#1,#5,#11,#13->#12,#14,#15,
#16,#17,#19->#18,#28,#29,#32,#37,#39,#41,#48).

## Last work
Tick 225: machine was down 08-25 08:14Z -> 09-15 18:30Z (~3 weeks; weekly
reviews 08-29/09-05/09-12 missed). Both in-flight jobs died in the 08-25
reboot: mertens-1e12-promote (killed 11h55m into the checker re-run,
promote-run.txt empty) and zero-scan-1e5 (died at 340000/999990 = 34%;
zeros in memory only -> lost). This tick: (1) ledger repair — NOTE #48
(exact m=0 term at theta*, MARGINAL) was claimed in tick 221's log but never
added; added now, DB matches log (48 rows). (2) zero_scan.py gained
checkpointing (optional 4th arg, {zeros,i_last} every 5000 steps + per zero);
resume machine-tested PASS ([1,30] then [1,40] same ckpt: first 3 zeros
identical, +3 new known zeros). (3) relaunched both as transient units, both
"Active: active (running)" 22:14:46 CEST. Deleted stray garbage file
"udo systemctl stop llama-server" (tick 224 residual).

## Next action
(a) TRACK D: mertens-1e12-promote.service ETA ~09-16 08:00Z (full 1e12 sieve
    re-run ~10-12h). When done: read evidence/2026-08-24-mertens-1e12/
    promote-run.txt (expect "PROMOTE-1e12 DONE rc=0" + #39 promoted); ledger
    +1 NUMERIC (30).
(b) TRACK D: zero-scan-1e5.service ETA ~09-20 04:00Z (999990 steps @ ~2.66/s);
    ckpt-1e5.json protects against reboot (worst case lose <=5000 steps).
(c) TRACK C: full-total check at theta* (a1F + m>=1 lower bounds + exact m=0
    at (A0=0.3967, theta*=0.0572); if >0 -> A0_max 0.3967, constant 2.5207,
    up from #47's 0.3506/2.8525). New attempt -> prior-art pre-flight first.
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
04:00Z (checkpointed). C: 8 NUMERIC (#33,#38,#40,#42,#44,#45,#46,#47) + #41
NOTE (A0 typo) + #48 NOTE (exact m=0 MARGINAL); next C step = full-total
check at theta* — not started. E: 4 NUMERIC (#10,#34,#35,#36); next E attempt
next week (frontier-escalated). A: 3 FORMAL (#2,#12,#25); PR leg still the
risk (owner). Next review: week-4 kill decision 09-17 — owner to decide
continue/reweight/kill with this handoff.
