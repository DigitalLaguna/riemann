# [IK Ch.1] Additive-API lemmas: `IsCompletelyAdditive.map_one`, `map_prime_pow`, log-bridge (issue #816)

> Ready-to-paste for the owner. Suggested: PR against `main` from branch
> `feat/ik-additive-api-816` (commit `0197a66`), or file as issue #816 follow-up.

---

Fills the TODO at `PrimeNumberTheoremAnd/IwaniecKowalskiCh1.lean:62`:

> **Think about more API for additive/completely additive functions, e.g. `f (p^k) = k * f p` for prime p, etc.**

Three lemmas, each with `@[blueprint]` attributes matching the file's conventions:

1. **`IsCompletelyAdditive.map_one`** — `f 1 = 0` for completely additive `f`
   (statement needs an `[AddGroupWithOne R]` context, which the `IsCompletelyAdditive`
   definition itself does not require — noted in the docstring).
2. **`IsCompletelyAdditive.map_prime_pow`** — `f (p ^ k) = k • f p` for prime `p`:
   the TODO's example itself (as `k • f p`, since the value type is an additive group).
3. **`isMultiplicative_log_isAdditive`** — if `f` is multiplicative with `f n > 0`
   for all `n`, then `log ∘ f` is additive on coprime arguments:
   `IsAdditive (toArithmeticFunction (fun n => Real.log (f n)))`.
   Proof: `hf.map_mul_of_coprime` + `Real.log_mul`.

Verified: full local build succeeds with the project-pinned toolchain
(`leanprover/lean4:v4.32.2`, mathlib `v4.32.2`):

    $ lake build
    Build completed successfully (4343 jobs).

No new `sorry`s; the 7 pre-existing `sorry` warnings are untouched.
Patch: 40 added lines, no deletions (see attached diff).
