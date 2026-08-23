# Track A: revised PNT+ IK additive-API lemmas (v2) — owner review fixes

Date: 2026-08-23 (manual session ~05:00 UTC, after tick 125)
Repo: tracks/a-lean/pnt @ https://github.com/AlexKontorovich/PrimeNumberTheoremAnd
Fork: https://github.com/DigitalLaguna/PrimeNumberTheoremAnd
Branch: `ik-additive-lemmas`, rebased: base `7715064` -> `751a8c2` (current upstream main)
Revised commit: `67661abc6ff51bc570aca7f93f85a3565bfe2afb` (supersedes `0197a66`, claim #12)

## Why (owner's pre-PR review of the staged PR body)

1. **Lemma 3 was VACUOUS (machine-confirmed).** Original hypothesis
   `(hpos : ∀ n, 0 < f n)` on `f : ArithmeticFunction ℝ` (= `ZeroHom ℕ ℝ`,
   hence `f 0 = 0` by `ArithmeticFunction.map_zero`) is unsatisfiable:
   `hpos 0 : 0 < 0`. `vacuity-check.lean` proves `False` from the original
   hypothesis set — `lake env lean` exit 0 (`vacuity-check.txt`). The lemma
   compiled, so the compiler never objected.
2. **Lemmas 1-2 over-assumed `[AddGroupWithOne R]`.** `f 1 = 0` needs only
   left cancellation; `k • f p` needs only `AddMonoid` (which
   `AddCancelMonoid` includes). `AddGroupWithOne` demanded `1 : R` + natural
   casts the statements never mention. Weakened both to `[AddCancelMonoid R]`.
   (First attempt at `[AddMonoid R]` for map_prime_pow FAILED the build —
   AddMonoid has no cancellation, and the base case calls `map_one hf`;
   compile-fail-retry caught it.)
3. **Naming.** `isMultiplicative_log_isAdditive` ->
   `ArithmeticFunction.IsMultiplicative.isAdditive_log` (dot-notation
   `hf.isAdditive_log` works; matches the `IsCompletelyAdditive.*` naming of
   the other two lemmas).
4. **Rebased onto current main** (`751a8c2`, 2 commits ahead of old base
   `7715064`, FKS2 files only) — the "two commits behind" paragraph in the
   PR body disappears.

## The revised lemmas (41 added lines, no deletions)

1. `IsCompletelyAdditive.map_one [AddCancelMonoid R]` — `f 1 = 0`
   (proof: `f 1 + f 1 = f 1` by complete additivity at (1,1), then
   `add_left_cancel`).
2. `IsCompletelyAdditive.map_prime_pow [AddCancelMonoid R]` — `f (p^k) = k • f p`
   (unchanged proof; context weakened).
3. `ArithmeticFunction.IsMultiplicative.isAdditive_log` —
   `hf : f.IsMultiplicative`, `hpos : ∀ n ≠ 0, 0 < f n` (vacuity fixed) ->
   `IsAdditive (toArithmeticFunction (fun n => Real.log (f n)))`
   (proof unchanged except `hpos m hm` / `hpos n hn` in the `Real.log_mul`
   calls; `hm`/`hn : ≠ 0` available from the `IsAdditive` goal context).

## Machine verdict

Toolchain: project-pinned `leanprover/lean4:v4.32.2`, mathlib `v4.32.2`.

    $ lake build
    Build completed successfully (4343 jobs).
    exit 0

(same tail verbatim in build-final.txt; sorry count 7 = 7 at base 751a8c2,
all pre-existing, none in the added block)

## Files

- `vacuity-check.lean` / `vacuity-check.txt` — machine proof that the ORIGINAL
  lemma-3 hypothesis set is unsatisfiable (exit 0 = `False` derived)
- `build-final.txt` — verbatim tail of the successful full `lake build`
- `check.sh` — re-runs the checker for claim #25 (branch/base/names/contexts/
  sorry count/full build)
