bibkey:      polymath15-2019
title:       Effective approximation of heat flow evolution of the Riemann xi function, and a new upper bound for the de Bruijn-Newman constant
authors:     D.H.J. Polymath
year:        2019
url:         https://arxiv.org/abs/1904.12438
local:       lit/pdf/polymath15-2019.pdf (extracted text: lit/text/polymath15-2019.txt)
fetched:     2026-08-20
main_result: "Theorem 1.1 (New upper bound). We have Λ ≤ 0.22." (Theorem 1.1, p. 1)
             "In this paper we improve the upper bound" — from Λ < 1/2 (Ki-Kim-Lee) to Λ ≤ 0.22, combining numerical verification of RH with new asymptotics and zero-dynamics of H_t (Introduction, p. 1)
             "This leads to improvements to the bound Λ ≤ 0.22 conditional on the assumption that the Riemann Hypothesis can be numerically verified beyond the height T ≈ 3.06 × 10^10 used in Section 8. For instance, the final row of the table implies that one has the bound Λ ≤ 0.1 assuming that the Riemann hypothesis is verified up to the height T ≈ 4.5 × 10^21." (Section 9 discussion, p. 63)
constants:   Lambda <= 0.22 unconditionally (Theorem 1.1); RH verification height used: T ≈ 3.06e10 (Section 8); conditional table (Table 1): e.g. Lambda <= 0.1 if RH verified to T ≈ 4.5e21; upper bound on Lambda proportional to 1/log T heuristically
supersedes:  ki-kim-lee-2009 (Lambda < 1/2, sharpening de Bruijn's Lambda <= 1/2); matches Rodgers-Tao 2019 lower bound Lambda >= 0 so RH <=> Lambda = 0
superseded:  none known as of 2026-08-20 (design doc: Polymath15 project notes claim current RH heights should give Lambda <= 0.20 — verify against wiki card)
relevance:   Track B. The method and the bound to reproduce (Phase 1). Three components: zero-free region for H_t (Section 3 criterion, Theorem 1.2), rigorous asymptotics (Section 4, Theorem 1.3), zero dynamics (Section 3, Proposition 3.1). Section 6 rules out the naive triangle-inequality approach (see DEAD_ENDS B-017 in design doc). Numerics must be Arb ball arithmetic; a float result is a NOTE.
