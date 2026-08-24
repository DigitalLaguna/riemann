bibkey:      macarevey-2026
title:       On the Lagarias Inequality and Superabundant Numbers
authors:     Andrew MacArevey
year:        2026 (arXiv:2602.15905v2 [math.NT], 19 Feb 2026; v1 16 Feb 2026)
url:         https://arxiv.org/abs/2602.15905
local:       lit/pdf/2602.15905.pdf (7 pp; extracted text: lit/text/2602.15905.txt)
fetched:     2026-08-24
main_result: "we show that the sequence B_n := (H_n + exp(H_n) log(H_n))/n is strictly increasing for n >= 1. As a consequence, if the Lagarias inequality has counterexamples, then the least counterexample must be a superabundant number; equivalently, it suffices to verify the inequality on the superabundant numbers." (Abstract, p. 1; formula flattened from PDF layout, subscripts rendered as _n)
             "Corollary 2.1. The sequence (H_n + exp(H_n) log(H_n))/n, n = 1, 2, ... is strictly increasing. Proof. Proposition 2.1 gives B_{n+1} > B_n for all n >= 55. Direct computation verifies B_{n+1} - B_n > 0 for 1 <= n <= 54." (Corollary 2.1, p. 5; sequence display flattened)
             "Proposition 2.1. For all real x >= e^4, we have L'(x) > 0. Consequently, B_{n+1} > B_n for all integers n >= 55" (Proposition 2.1, p. 5)
             "Theorem 3.1. If there are counterexamples to the Lagarias inequality, the smallest such counterexample must be a superabundant number." (Theorem 3.1, p. 6)
constants:   analytic leg threshold x >= e^4 (B_{n+1} > B_n proven for n >= 55); finite leg 1 <= n <= 54 by "direct computation" (NOT reproduced in the paper — black box); L(x) = (H(x) + e^{H(x)} log H(x))/x with H(x) = psi(x+1) + gamma; Lemma 2.7: e^t >= 2t^2 + 3t + 1 for t >= 4; proof chain Lemmas 2.1-2.7 (integral bounds on psi')
supersedes:  - (new result; Section 3 strategy "inspired by [1]" = Assani-Chester-Paschal, arXiv:2503.03159, Robin/Kaneko-Lagarias "almost every n" — different result, not superseded)
superseded:  - (v2, 19 Feb 2026; no known successor as of 2026-08-24)
relevance:   Track E (tick-177 attempt): the SA restriction is the recorded next lever after claim #10 (Lagarias all-n check to 1e6) — verifying the inequality on superabundant numbers only pushes the verified range from 1e6 to 1e10 at ~100x lower cost. Track D: witness search on SA numbers. NOTE: the finite leg (1 <= n <= 54) is a black-box "direct computation" in the paper — tick 177 re-verifies it at 100 digits (F1a) and spot-checks the analytic leg (F1b).
