bibkey:      odlyzko-teriele-1985
title:       Disproof of the Mertens conjecture
authors:     A. M. Odlyzko (Bell Labs, Murray Hill), H. J. J. te Riele (CWI, Amsterdam)
year:        1985
url:         https://doi.org/10.1515/crll.1985.357.138 (J. reine angew. Math. (Crelle's) 1985 (357), 138–160; PDF from CWI repository, https://ir.cwi.nl/pub/1823/1823D.pdf)
local:       lit/pdf/odlyzko-teriele-1985.pdf (23 pp; extracted text: lit/text/odlyzko-teriele-1985.txt)
fetched:     2026-08-20
main_result: "Our disproof is indirect, and does not produce any single value of x for which IM(x)I >x2 ." (Section 1, Introduction; 'IM(x)I' = |M(x)| and '>x2' = '> sqrt(x)' in the printed PDF, fraction glyphs flattened by extraction)
             "In fact, we suspect that there are no counterexamples to the Mertens conjecture for x ~ 1020 or perhaps even 10 30 . (Section 5 explains the reasons for this belief.)" (Section 1; '~' = '<=' and '1020' = 10^20, '10 30' = 10^30 as printed)
             "The disproof of the Mertens conjecture closes off another possible road to proving the Riemann hypothesis." (Section 1)
             Quantitative claim (Section 1, math flattened): lim sup M(x)/sqrt(x) > 1.06 and lim inf M(x)/sqrt(x) < -1.009, which disproves the Mertens conjecture |M(x)| < sqrt(x).
constants:   lim sup M(x)/sqrt(x) > 1.06; lim inf M(x)/sqrt(x) < -1.009; no counterexample expected below x <= 10^20 (10^30); Mertens conjecture |M(x)| < sqrt(x) for x > 1
supersedes:  Neubauer 1977 / Cohen-Dress 1979 computational verifications (verified |M(n)| < 0.6 sqrt(n) through 7.8e9; first M(n)/sqrt(n) > 1/2 at n = 7,725,038,629)
superseded:  none (the disproof stands); explicit counterexample M(10166132) = 1050 > sqrt(10166132) is due to the follow-up computation (verify exact reference before citing: Odlyzko-te Riele, follow-up note)
relevance:   Track D. The canonical example of 'computation disproves a conjecture' — the template for Track D's machine-verified disproofs. The explicit counterexample (M(10166132) = 1050) is the concrete witness; its interval-arithmetic re-verification is a candidate first NUMERIC claim. Also the origin of the Lagarias-Odlyzko algorithmic ideas used elsewhere in the project.
