# RH verification-height source search (track B row-3 literature gate)

Date: 2026-08-22 (tick 85). Pre-registered in logs/2026-08-22.tick.log (tick 84).

## Question
Is there a fetchable document claiming the Riemann hypothesis is verified up to
height >= 1e13? Row 3 of the Polymath15 Table-1 re-run (t=0.18, y=0.13206,
N0=830443, X=1e13+19877) needs RH verified to 1e13. Platt-Trudgian 2020 is 3e12.

## Queries run (arXiv API, export.arxiv.org/api/query, sortBy=submittedDate desc)
1. sweep:     ti:"Riemann hypothesis"  (max 40)          -> sweep.xml
2. targeted:  abs:"Riemann hypothesis" AND (abs:"verified" OR abs:"verification")  (max 40) -> targeted.xml
3. height13:  abs:"Riemann hypothesis" AND (abs:"10^{13}" OR abs:"10^13" OR abs:"10,000,000,000,000") (max 30) -> height13.xml
4. height12:  abs:"Riemann hypothesis" AND (abs:"10^{12}" OR abs:"10^12") (max 30) -> height12.xml

Raw Atom XML saved alongside (sweep.xml, targeted.xml, height13.xml, height12.xml).
Parsed output: results.txt (queries 1-2), results2.txt (queries 3-4).

## Verbatim quotes (the only verification-height claims found)
- arXiv:2004.09765 (Platt & Trudgian 2020), "The Riemann hypothesis is true up to
  $3\cdot 10^{12}$":
    "We verify numerically, in a rigorous way using interval arithmetic, that the
     Riemann hypothesis is true up to height $3\cdot10^{12}$. That is, all zeroes
     $β+ iγ$ of the Riemann zeta-function with $0<γ\leq 3\cdot 10^{12}$ have $β= 1/2$."
- arXiv:2109.02249 (2021), "Improving bounds on prime counting functions by partial
  verification of the Riemann hypothesis":
    "Using a recent verification of the Riemann hypothesis up to height
     $3\cdot 10^{12}$, we provide strong estimates on $π(x)$ ..."
  (i.e. it CONSUMES the 3e12 record, does not extend it.)

## Verdict (machine: arXiv API)
NO fetchable document claims RH verified to height >= 1e13. The record remains
Platt-Trudgian 2020 at 3e12. Grep for 10^13 / 10^{13} / 1e13 / 10,000,000,000,000
across all four result sets: NONE.

## Consequence (per pre-registered falsification test)
Row 3 WAITS. Track B pivots to the Phase-3 dominant-error-term audit: identify
which of the three components (zero-free region for H_t, asymptotics, zero
dynamics) is binding in the 0.20 bound, and put compute there.
