bibkey:      dbn-code
title:       Polymath15 dbn_upper_bound code and writeup repository
authors:     km-git-acc (Kartik Mehta et al., Polymath15 computational team)
year:        2019
url:         https://github.com/km-git-acc/dbn_upper_bound
local:       tracks/b-dbn/dbn (local clone, fetched 2026-08-20)
fetched:     2026-08-20
main_result: "Most of the recent work has been done in the Pari/GP, Arb and Julia languages. For large scale runs, the Arb scripts are recommended, and for mathlike readability, the other two." (README.md, section "Computational Libraries and Machine Requirements")
             "(Currently, a dBN bound of 0.22 has been achieved unconditionally, and several tighter bounds conditional on RH verified to appropriate heights also demonstrated)" (README.md, section "Results")
constants:   none fixed in README; the pipeline: dbn_upper_bound/arb/*.c (Arb C scripts: Tloop*, BarrierLocationAssistant, RH_LinecountthreadedV3, New_abeff_largex_bounds, Abceff*), plus Pari/GP and Julia versions; the paper's LaTeX source is in Writeup/debruijn.tex; some key scripts only live as pastebin links (dbn_upper_bound/arb/Links.to.Arb.C.scripts.txt) — pastebin may rot, verify before relying
supersedes:  none; it is the code
superseded:  none known as of 2026-08-20
relevance:   Track B Phase 1: reproduce the 0.22 bound from this code. Arb C is the recommended path for large runs; our machine has libarb (python-flint wheel bundles FLINT/arb — C scripts need arblib headers, install check pending). The Writeup/ folder gives the exact parameters. Conditional results (0.20 target) need the 3e12 RH verification height swapped in.
