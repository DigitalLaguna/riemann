bibkey:      polymath-wiki-dbn
title:       Polymath wiki: De Bruijn-Newman constant
authors:     Polymath wiki contributors (michaelnielsen.org/polymath)
year:        2019
url:         https://michaelnielsen.org/polymath/index.php?title=De_Bruijn-Newman_constant
local:       lit/pdf/polymath-wiki-dbn.html (extracted text: lit/text/polymath-wiki-dbn.txt)
fetched:     2026-08-20
main_result: "Polymath15 was able to establish the bound [math]\displaystyle{ \Lambda \leq 0.22 }[/math] , but with the recent numerical verification of RH in https://arxiv.org/abs/2004.09765 this may be improved to [math]\displaystyle{ \Lambda \leq 0.20 }[/math] ." (Section "Writeup", fetched page)
             "The current strategy is to combine the following three ingredients: Numerical zero-free regions for H_t(x+iy) of the form { x+iy: 0 <= x <= T; y >= epsilon } for explicit T, epsilon, t > 0. Rigorous asymptotics that show that H_t(x+iy) [is nonzero] whenever y >= epsilon and x >= T for a sufficiently large T. Dynamics of zeroes results that control Lambda in terms of the maximum imaginary part of a zero of H_t." (Intro, fetched page; bracketed word supplied by carder where the wiki's math markup elided it — verify against HTML before citing)
constants:   Lambda <= 0.22 (Polymath15); may be improved to Lambda <= 0.20 using the RH verification of Platt-Trudgian (arXiv:2004.09765, RH true to 3e12); current known range 0 <= Lambda < 1/2
supersedes:  project-state page for the Polymath15 effort; supersedes nothing as a result
superseded:  none known as of 2026-08-20 (wiki is a living document; re-check on each revisit)
relevance:   Track B Phase 2 target: the 0.20 number. The wiki states the improvement "may be" obtained with the new RH height — it is a note, not a proof: our job is to make it a NUMERIC claim (Arb ball arithmetic, explicit error bound) by re-running the Polymath15 code with the 3e12 verification height. Also defines the three-part bottleneck (zero-free region / asymptotics / zero dynamics) that Track B Phase 3 must attack.
