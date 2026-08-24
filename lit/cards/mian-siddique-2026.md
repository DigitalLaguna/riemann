bibkey:      mian-siddique-2026
title:       A Kernel-Checked Exclusion Certificate for Erdős Problem 647
authors:     Ibrahim Mian, Shayaan Siddique (arXiv v1, 18 Aug 2026)
year:        2026
url:         https://arxiv.org/abs/2608.17880
local:       lit/pdf/mian-siddique-2026.html (arXiv HTML v1 full text; abs page: evidence/2026-08-24-arxiv-sweep/2608.17880-abs.html)
fetched:     2026-08-24
main_result: "No n with 24<n\leq 10^{9} satisfies \max_{m<n}(m+\tau(m))\leq n+2" (Theorem 1.1, §1; LaTeX alttext of the statement as rendered in arXiv HTML v1; proved in Lean 4 against mathlib in the repository decanus, axiom closure exactly {propext, Classical.choice, Quot.sound}, no sorry, no native_decide)
constants:   24 (condition holds at n=24; exclusion lower bound); 10^9 (exclusion upper bound); 1024 (no primality facts needed beyond primes below 1024); 6,685,922 factorization witnesses in the replayed chain; threshold n+2 best possible since max(τ(n-1)+n-1, τ(n-2)+n-2) ≥ n+2 for every n
supersedes:  prior computational exclusions "up to 10^12 by direct sieve and up to roughly 9.17×10^18 within a modular reduction whose Lean component relies on native_decide" (Abstract) — those sit outside any proof kernel; this is the first exclusion checked end to end by one kernel. Finite fully-proved form of the domination-interval argument whose asymptotic step was the identified gap in a withdrawn January 2026 claim on this problem.
superseded:  none known as of 2026-08-24
relevance:   Track A (continuous intake, not a seed). Method template for large-scale computational formalization: witness-chain certificate format (each witness stores the maximal power of each prime below 1024 dividing it; the kernel recomputes a divisor-count lower bound with a doubling rule licensed by maximality), two-layer CI axiom gate, replay through standalone lean4checker, and two from-source verification legs (Lean toolchains built by gcc and by clang, mathlib rebuilt with no cache, olean digests byte-identical across three builds on two architectures). Directly applicable if we ever formalize the Track D Robin/Mertens scans in Lean. Authors' own framing: "the contribution is the trust base, not the range" (range is 3-10 orders of magnitude below the cited computational frontiers).
checked:     2026-08-24 (quote and constants verified against lit/pdf/mian-siddique-2026.html)
