# HANDOFF — session 2026-08-24 ~19:30 UTC (tick 201)
# track: C (A0 audit) | gate: all tracks OPEN (21/21 seeds)

## State
41 claim rows: 23 NUMERIC (B: #3,4,6,7,8,9,18; E: #10,#34,#35,#36; D:
#20,21,22,23,24,26,27,30,31; C: #33,#38,#40), 3 FORMAL (A: #2, #12 [SUPERSEDED
by #25], #25), 15 NOTE (#1,#5,#11,#13->#12,#14,#15,#16,#17,#19->#18,#28,#29,
#32,#37,#39,#41). Track C: #40 NUMERIC (Lemma-1 final-line re-opt, A_final=
2.3782) BUT its "improvement 4.896->4.8596" is now VOID per #41 NOTE (this
tick): the table's Lemma-1 A0=(4.8596)^-1 is a TYPO, true A0=(4.896)^-1, so the
unconditional constant is still capped at 4.896. Track D: mertens-1e12 scan
DONE (max |M(x)| x<=1e12 = 331302 @ 661066575037; M(1e12)=62366=OEIS a(12));
#39 NOTE, promotion in flight.

## Last work
Tick 201: A0-constraint audit of BTY-2026 (new attempt, prior-art pre-flight
logged). Machine (a0_check.py, mpmath 50 dps, evidence/2026-08-24-zfree-a0-
audit/): the table Lemma-1 row's own eta0=0.0071093/sigma0=0.9935164 match
A0=(4.896)^-1=0.204248366 to all printed digits (eta0=A0/logH, sigma0=1-A0/
log(KH+T0), H=3e12, K=16, T0=1e10), NOT the printed (4.8596)^-1=0.2057782.
Independent confirmation: the Lemma-1 final line requires A0<A_final=
0.2042621883; only (4.896)^-1 satisfies it (margin +1.38e-5; printed
(4.8596)^-1 fails, -0.0015). check.sh CHECK PASS. -> NOTE #41. Anomaly
resolved (constraint 7): #40's README provenance "A0 from Lemma 2's 4.8594"
was wrong; the row's own eta0/sigma0 contradict the printed A0.

## Next action
(a) TRACK C: re-audit lemmas 5,6,13,14 for A0_max = sup{A0: lemmas hold with
    eta0=A0/logH, sigma0=1-A0/log(KH+T0)}. Baseline now #41 (true A0=
    (4.896)^-1=0.2042484). Target: A0_max>=0.4204835 -> constant 2.3782;
    0.2042484<A0_max<0.4204835 -> constant 1/A0_max (partial win);
    A0_max<=0.2042484 -> no improvement. Identify which lemma binds FIRST
    (5 non-negativity / 6 A-range / 13 eta-range / 14 C2(eta) term). NEW
    attempt -> prior-art pre-flight first.
(b) TRACK D: robin-full-1e11.service ~21:50Z (subseg 773/1000, best_R=
    0.972015886980 at n=13967553600 unchanged): read
    evidence/2026-08-24-robin-1e11/full-run.txt (expect "ROBIN-FULL-1e11
    DONE rc=0" + final best_R), run F1/F2/F3a/F3b (see logs tick 184),
    promote claim (Robin full scan [1e10,1e11): max R, no witness R>=1).
(c) TRACK D: mertens-1e12-promote.service ~08-25 07:00Z: read
    evidence/2026-08-24-mertens-1e12/promote-run.txt (expect "PROMOTE-1e12
    DONE rc=0" + "promoted #39: NOTE -> NUMERIC"); ledger +1 NUMERIC.
(d) TRACK D: zero scan ~08-27 (27.5%): F5a/b/c + F3/F4 + max/min g [1,1e5].
(e) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then
    comment `propose #<PR>` on issue #816 (ASSIGNED to IlPreteRosso since
    2026-01-28, stale ~7 months; ping or wait for disclaim).
(f) TRACK B (weight 40): PARKED until week-2 review (08-29): X-sweep to 7e12;
    Arb-port of 0.20 pipeline (promotes NOTE #11); row-3 t=0.18 push BLOCKED
    on RH-to-1e13 source.

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
ETA 21:50Z, zero-scan ETA ~08-27, mertens-1e12 promotion ETA 08-25 07:00Z.
C: 3 NUMERIC (#33,#38,#40) + #41 NOTE (A0 typo, voids #40's improvement);
next C step = re-audit lemmas 5,6,13,14 for A0_max (path to 2.3782) — not
started. E: 4 NUMERIC (#10,#34,#35,#36); next E attempt next week
(frontier-escalated). Next review 2026-08-29 (week 2): milestone check +
spot-check 3 cards vs PDFs + decide B next step. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg
still the risk.
