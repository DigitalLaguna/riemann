# HANDOFF — session 2026-08-25 ~00:40 UTC (tick 211)
# track: GARDEN (a0max_audit.py dedupe) | gate: all tracks OPEN (21/21 seeds)

## State
44 claim rows: 26 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31,#43; C: #33,#38,#40,#42,#44), 3 FORMAL (A: #2,
#12 [SUPERSEDED by #25], #25), 15 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,
#19->#18,#28,#29,#32,#37,#39,#41). No ledger delta this tick (garden step).

## Last work
Tick 211: GARDEN (handoff item f). Deduped a0max_audit.py: the copies in
evidence/2026-08-24-zfree-a0-audit/ (a0max_audit.py, check_a0max.sh, added
21:58-22:00 tick 205) were byte-identical (diff -q) to the canonical copies
in evidence/2026-08-24-zfree-a0max/ (claim #42's evidence_path). git rm'd
the two redundant files, appended a GARDEN note to zfree-a0-audit/README.md
(append-only; a0_check.py/check.sh/machine-run.txt stay = claim #41
evidence). Post-deletion machine re-runs: zfree-a0max/check.sh "CHECK PASS"
RC=0; zfree-a0-audit/check.sh "CHECK PASS" RC=0. Ledger refs verified: #42
-> zfree-a0max, #44 -> zfree-a0max-internal (runs canonical script), #41
NOTE evidence_path=None.

## Next action
(a) TRACK D: mertens-1e12-promote.service ETA ~08-25 07:00Z (6h09m at
    00:26Z; checker re-running the 1e12 sieve, pid 844915 alive). When done:
    read evidence/2026-08-24-mertens-1e12/promote-run.txt (expect
    "PROMOTE-1e12 DONE rc=0" + "promoted #39: NOTE -> NUMERIC"); ledger
    +1 NUMERIC (27).
(b) TRACK C: path to full 2.3782 = raise A0 past 0.20547, i.e. relax Lemma
    5's |z|>=138 requirement itself (new attempt -> prior-art pre-flight
    first; #42+#44 confirmed all OTHER internals hold at A0_max).
(c) TRACK D: zero scan 30.5% (305000/999990, 106208s elapsed) ETA ~08-27
    14:30-18:00Z: F5a/b/c + F3/F4 + max/min g [1,1e5].
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
mertens-1e12 promotion (6h09m at 00:26Z), zero-scan ETA ~08-27 14:30-18:00Z.
C: 5 NUMERIC (#33,#38,#40,#42,#44) + #41 NOTE (A0 typo); #42+#44 = A0_max
PARTIAL win 4.866889911 CONFIRMED (Lemma 5 main binds; all internals hold);
next C step = attack Lemma 5's 138 requirement (path to full 2.3782) — not
started. E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week
(frontier-escalated). Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean
PR upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR
leg still the risk.
