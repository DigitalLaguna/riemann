bibkey:      lagarias-2002
title:       An Elementary Problem Equivalent to the Riemann Hypothesis
authors:     Jeffrey C. Lagarias
year:        2002 (Amer. Math. Monthly 109 (6), 534–543; arXiv preprint math/0008177v2, May 2001)
url:         https://arxiv.org/abs/math/0008177 (journal DOI: 10.1080/00029890.2002.11919883)
local:       lit/pdf/lagarias-2002.pdf (9 pp, arXiv v2; extracted text: lit/text/lagarias-2002.txt)
fetched:     2026-08-20
main_result: "with equality only for n = 1." (Abstract, Problem E, p. 1)
             "The ‘E’ in Problem E might stand for either ‘easy’ or ‘elementary’. Perhaps ‘H’ for ‘hard’ would be a better letter to use, since our object is to show the following equivalence." (Section 1, p. 1; curly quotes as printed)
             Problem E, flattened from the PDF formula layout (Abstract + Section 1): Let H_n = sum_{j=1}^n 1/j. Show, for each n >= 1, that sigma(n) = sum_{d|n} d <= H_n + exp(H_n) log(H_n), with equality only for n = 1.
             "Theorem 1.1 Problem E is equivalent to the Riemann hypothesis." (Section 1)
constants:   Lagarias inequality sigma(n) <= H_n + e^{H_n} log(H_n) for all n >= 1, equality only at n = 1; sigma(n) = sum of divisors
supersedes:  -
superseded:  -
relevance:   Track D. This IS the 'RH is easy' bet target: Problem E is literally named 'E' (easy), and the paper's joke ('Perhaps H for hard would be a better letter') is the bet's hook. The inequality is machine-checkable: a single n with sigma(n) > H_n + e^{H_n} log(H_n) disproves RH (witness-verifiable with exact integer arithmetic); and the claim 'RH implies the inequality' is the formal side. Also a candidate for Track A (Lean formalization of the equivalence).
