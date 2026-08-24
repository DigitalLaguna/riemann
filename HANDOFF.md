# HANDOFF — session 2026-08-24 ~23:35 UTC (tick 205)
# track: D (Robin 1e11 promote) + C (#42 evidence fix) | gate: all tracks OPEN (21/21 seeds)

## State
43 claim rows: 25 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42), 3 FORMAL (A: #2, #12
[SUPERSEDED by #25], #25), 15 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,
#19->#18,#28,#29,#32,#37,#39,#41). This tick: +1 NUMERIC (#43 Robin full
[1e10,1e11)); #42 evidence-path corrected to zfree-a0max (checker now passes).
Track C: #42 NUMERIC (A0_max audit: Lemma 5 binds, A0_max=0.205470026688,
unconditional constant 4.896->4.866889911, PARTIAL win; NOT the full 2.3782).
Track D: #43 NUMERIC (Robin full [1e10,1e11): max R=0.9720158869800256 @
n=13967553600, no witness R>=1).

## Last work
Tick 205: (a) TRACK D: robin-full-1e11 run COMPLETED 20:43:10Z (ticks 203-204
only appended progress). Machine (evidence/2026-08-24-robin-1e11/check.sh):
"CHECK PASS: Robin full scan [1e10,1e11)" RC=0 (F1 sieve-vs-sympy 30/30, F2 no
witness, F3a full>=SA(50-digit), F3b 12-sig-digit==SA_REF, VERDICT ALL CHECKS
PASS, ROBIN-FULL-1e11 DONE rc=0). promote.sh add->NOTE #43, promote 43 NUMERIC
(checker re-ran PASS). (b) TRACK C: #42 anomaly — its recorded evidence_path
(zfree-a0-audit) had check.sh verifying the #41 typo audit (a0_check.py), not
the A0_max audit. Fixed: saved a0max machine output to zfree-a0max/machine-run.txt
(a0max_audit.py, mpmath 60 dps); zfree-a0max/check.sh "CHECK PASS" RC=0 (Lemma 5
binds A0=0.205470026688, 1/A0=4.866889911 PARTIAL win; Lemma 14 binds 10.50,
Lemma 13 binds 8.53e6, both hold at target 0.4204835). Re-pointed #42
evidence_path -> zfree-a0max (evidence_path-only UPDATE; status stays NUMERIC,
checker passes at new path). Anomaly resolved (constraint 7).

## Next action
(a) TRACK C: A0_max audit REMAINING caveats per #42 — Lemma 6 (A-range) +
    Lemma 5's other internal bounds (B(y)>0, eta0*C(138,138)<2*w0*eps0, eq-22
    C(-1,T0/eta0) term) not yet re-audited; if any binds below 0.20547 the
    4.8669 win shrinks. NEW attempt -> prior-art pre-flight first.
(b) TRACK D: mertens-1e12-promote.service ~08-25 07:00Z: read
    evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + "promoted #39: NOTE -> NUMERIC"); ledger +1 NUMERIC.
(c) TRACK D: zero scan ~08-27 (27.5%): F5a/b/c + F3/F4 + max/min g [1,1e5].
(d) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(e) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to 7e12;
    Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push BLOCKED
    on RH-to-1e13 source.
(f) GARDEN (weekly): dedupe a0max_audit.py + a0max checker across
    zfree-a0-audit (a0max_audit.py, check_a0max.sh) and zfree-a0max
    (a0max_audit.py, check.sh) — keep zfree-a0max canonical for #42.

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
ETA 08-25 07:00Z, zero-scan ETA ~08-27. C: 4 NUMERIC (#33,#38,#40,#42) + #41
NOTE (A0 typo); #42 = A0_max PARTIAL win 4.8669 (Lemma 5 binds); next C step =
re-audit Lemma 6 + Lemma 5 internal bounds (path to full 2.3782) — not started.
E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week (frontier-escalated).
Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards vs PDFs
+ decide B next step. Week-4 kill (09-17): Lean PR upstream + Polymath15 to
2 sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
