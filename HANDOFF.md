# HANDOFF — session 2026-08-23 06:2x UTC (tick 129)
# track: D | gate: all tracks OPEN (21/21 seeds)

## State
26 claim rows: 14 NUMERIC (B: #3,4,6,7,8,9,18; E: #10; D: #20,21,22,23,24,26), 3 FORMAL
(A: #2 PNT+ local build, #12 IK lemmas v1 [SUPERSEDED by #25], #25 IK lemmas v2),
9 NOTE (#1, #5, #11, #13->#12, #14, #15, #16, #17, #19->#18). NEW: #26 NUMERIC —
Robin FULL scan [1e8,1e9] (all n, no CA/SA reduction): max R(n)=sigma(n)/(e^gamma*n*
loglog n) = 0.9681521049018093 (50-digit mpmath, exact int64 segmented-sieve sigma) at
n=367567200 (colossally abundant, sigma=1889879040); no witness R>=1 (Lagarias 2002 eq
1.2 => RH-consistent); F1 33-point sympy cross-check 0 mismatches. Tick-128 F3 CHECK
FAILURE RESOLVED (constraint 7): 0.968152104902 (claim #23) is the 12-SIG-DIGIT DISPLAY
(rounds UP, 13th digit 8) of the 50-digit value; 80-digit proof in
evidence/2026-08-23-robin-full-scan/f3-resolution.txt; F3 split into F3a (50-digit
consistency) + F3b (12-digit display regression); re-run VERDICT: ALL CHECKS PASS.

## Last work
Tick 128 ran the sixth D experiment (Robin full scan [1e8,1e9], 5.3 min) and ended with
VERDICT: CHECK FAILURE on F3 — an unexplained mismatch that blocks per constraint 7.
Tick 129 resolved it against the machine: pre-registered R1/R2/R3 (log), 80-digit
computation proved both published values are roundings of one quantity, fixed the check
logic (compare at 50 digits + display regression), re-ran the scan (deterministic,
5m19s), booked #26 NUMERIC via promote.sh (checker CHECK PASS).

## Next action
(a) OWNER: open PR via
    https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
    (title/body: evidence/2026-08-22-pnt-ik-api/pr-body.md rev 2), then comment
    `propose #<PR>` on issue #816. CAVEAT: #816 ASSIGNED to IlPreteRosso since
    2026-01-28 (stale ~7 months); `propose` only moves the task if proposer holds the
    claim -> ping @IlPreteRosso on #816 or wait for disclaim (options in pr-body.md).
(b) TRACK D (weight 15): seventh experiment — S(t) scan (Riemann-Siegel S(t) extremal
    values; needs RS implementation, bounded step) OR Mertens 1e11 (exact integer sieve;
    1e10 took 28 min => 1e11 ~2.5h, background run across ticks). Pre-register
    falsification FIRST (witness => RH false => STOP, c5).
(c) TRACK B (weight 40): PARKED until week-2 review (08-29): (i) X-sweep to 7e12
    (stored sums = long pole); (ii) Arb-port of the 0.20 pipeline (promotes NOTE #11);
    (iii) row-3 t=0.18 push — BLOCKED on RH-to-1e13 source (Platt-Trudgian 3e12).
(d) Tracks A/C/E: A waits on the PR (its only critical path); C/E no in-flight work.

## Blocked
- PNT+ PR: branch v2 on fork DONE; PR form + `propose #N` on #816 need owner;
  #816 claimant (IlPreteRosso) contact per CONTRIBUTING (see (a))
- odlyzko-zeros full chapter (AMS LibLynx login) — carded from landing page
- lean-zulip-pnt full thread (Zulip JS UI) — carded from README+blueprint
- RH verification to 1e13 for track B row-3 t=0.18 (Platt-Trudgian covers 3e12)

## Budget
Week-1 reweight A30/B40/D15/C10/E5 stands; "A claims first XS Lean issue by 09-03"
MET in substance (claim #25 FORMAL, PR leg = one owner click). D 6 NUMERIC
(#20-#24, #26). Next review 2026-08-29 (week 2): milestone check + spot-check 3 cards
vs PDFs + decide B next step + D seventh experiment. Week-4 kill (09-17): Lean PR
upstream + Polymath15 to 2 sig figs — numerics leg met (#7,#9,#18); PR leg still the risk.
