# HANDOFF — session 2026-08-24 ~18:52 UTC (tick 200)
# track: C (re-opt recorded) | gate: all tracks OPEN (21/21 seeds)

## State
40 claim rows: 23 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31; C: #33,#38,#40), 3 FORMAL (A: #2, #12 [SUPERSEDED
by #25], #25), 14 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,
#32,#37,#39). Track C: re-optimization of BTY-2026 Lemma-1 final line DONE +
recorded as #40 NUMERIC (this tick): corrected kappa^2 + sharp c_mu + eta=A/x
fixed point -> A_final=2.3782, but lemmas 5-14 A0 constraint (A0=1/4.8596,
from Lemma 2's 4.8594) caps the UNCONDITIONAL constant at 4.8596. Machine-
verified improvement over published 4.896: 4.896 -> 4.8596 (0.75% wider).
Track D: mertens-1e12 scan DONE (max |M(x)| x<=1e12 = 331302 @ 661066575037;
M(1e12)=62366=OEIS a(12)); #39 NOTE, promotion in flight (full 1e12 re-run).

## Last work
Tick 200: (1) Found zfree-reopt re-optimization DONE+committed in tick 197
  (evidence/2026-08-24-zfree-reopt/, commit 26f8390) but NOT in ledger; the
  tick-199 HANDOFF wrongly said "not started". (2) Re-ran reopt.py: matched
  machine-run.txt except last 3 lines missing (stale capture: machine-run.txt
  17:26:40Z, reopt.py updated 17:27:47Z to add "Paper's own fixed point"
  provenance block; diff=22a23,25, strict superset). (3) Appended the 3-line
  delta to machine-run.txt (append-only; verified first 22 lines identical).
  (4) Wrote check.sh (F1-F5), ran it -> CHECK PASS. (5) Added claim #40 NOTE,
  promoted to NUMERIC (checker PASS). Anomaly resolved: "future timestamps"
  were a +0200 (CEST) vs UTC display artifact.

## Next action
(a) TRACK D: mertens-1e12-promote.service ~08-25 07:00Z: read
    evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + "promoted #39: NOTE -> NUMERIC"); ledger +1 NUMERIC.
(b) TRACK D: robin-full-1e11.service ~21:46Z (subseg 735/1000, best_R=
    0.972015886980 at n=13967553600 unchanged): read
    evidence/2026-08-24-robin-1e11/full-run.txt (expect "ROBIN-FULL-1e11
    DONE rc=0" + final best_R), run F1/F2/F3a/F3b (see logs tick 184),
    promote claim (Robin full scan [1e10,1e11): max R, no witness R>=1).
(c) TRACK C: path to 2.3782 = re-audit lemmas 5-14 to raise A0 from
    0.2057782 to 0.4204835 (extend eta-range A0/log t -> A*/log t) — NEW
    attempt, prior-art pre-flight first. Baseline: #40 (A0 caps at 4.8596).
(d) TRACK D: zero scan ~08-27 (27%): F5a/b/c + F3/F4 + max/min g [1,1e5].
(e) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(f) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to
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
Week-1 reweight A30/B40/D15/C10/E5 stands. D: 9 NUMERIC + #39 NOTE
(promotion in flight) + 2 NOTE (#28,#37); in flight: robin-full-1e11
ETA 21:46Z, zero-scan ETA ~08-27, mertens-1e12 promotion ETA 08-25 07:00Z.
C: 3 NUMERIC (#33,#38,#40); next C step = re-audit lemmas 5-14 to raise A0
(path to 2.3782) — not started. E: 4 NUMERIC (#10,#34,#35,#36); next E
attempt next week (frontier-escalated). Next review 2026-08-29 (week 2):
milestone check + spot-check 3 cards vs PDFs + decide B next step. Week-4
kill (09-17): Lean PR upstream + Polymath15 to 2 sig figs — numerics leg met
(#7,#9,#18); PR leg still the risk.
