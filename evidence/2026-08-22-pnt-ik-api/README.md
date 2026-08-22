# Track A: first verified API contribution to PNT+ (Iwaniec–Kowalski Ch.1 additive API)

Date: 2026-08-22 (tick 80)
Repo: tracks/a-lean/pnt @ https://github.com/AlexKontorovich/PrimeNumberTheoremAnd
Branch: `ik-additive-lemmas` (agent working branch; earlier `feat/ik-additive-api-816` exists from 08-22 07:17, same base)
Base commit: `7715064` "feat(FKS2): certify row 11 small-window numerics (#1729)" (tag v4.32.2-16-g7715064, = main HEAD at clone 08-20)
Agent commit: `0197a66` "feat(IK): prove IsCompletelyAdditive.map_one, map_prime_pow, isMultiplicative_log_isAdditive" (08-22 08:27)

## What was done (provenance)

The three lemmas were first written by crashed timer ticks 79/80 (08-22 04:35/05:06 CEST,
utf-8 crashes, no log sections left), found as an unrecorded working-tree diff by tick 82
(frontier, 08:22 06:10 CEST), which verified a target build: "Build completed successfully
(3567 jobs)" exit 0. This session (after tick 82, from 08:22 CEST) refined the proofs (4 error classes
root-caused in the drafts, see below), switched to branch `ik-additive-lemmas`, committed
(`0197a66`), and verified a FULL build: 4343 jobs, exit 0.

Filled the TODO comment at `PrimeNumberTheoremAnd/IwaniecKowalskiCh1.lean:62`
(= PNT+ issue #816, "Think about more API for additive/completely additive
functions, e.g. `f (p^k) = k * f p` for prime p, etc.") with three new lemmas,
each machine-verified by the Lean 4 compiler:

1. `IsCompletelyAdditive.map_one` — a completely additive arithmetic function satisfies `f 1 = 0`
   (needs `AddGroupWithOne` context; the TODO's example `f (p^k) = k * f p` needs `k • f p` smul)
2. `IsCompletelyAdditive.map_prime_pow` — `f (p ^ k) = k • f p` for prime `p` (the TODO example itself)
3. `isMultiplicative_log_isAdditive` — positive-valued multiplicative `f : ℕ → ℝ`
   gives additive `log ∘ f` on coprime arguments (via `hf.map_mul_of_coprime` + `Real.log_mul`)

All three carry `@[blueprint]` attributes matching the file's conventions (title + LaTeX statement).

## Machine verdict

Toolchain (project-pinned via `lean-toolchain` + `lakefile.toml`):
- Lean: `leanprover/lean4:v4.32.2`
- mathlib: `v4.32.2` (rev pinned in lakefile.toml)
- Machine: 48 cores, 125 GB RAM; mathlib obtained via `lake exe cache get` (bootstrap, 08-20)

Command and output (see build-final.txt, verbatim):

    $ cd tracks/a-lean/pnt && lake build
    ...
    Build completed successfully (4343 jobs).
    exit 0

Full build of all 4343 targets (PNT+ proper + the modified file) succeeds with
the agent's three lemmas in place. The 7 remaining `declaration uses sorry`
warnings are pre-existing at base commit 7715064 (lines 114, 131, 689, 911,
1662, 1829, 1844 of the new file) — none in the agent's lemmas.

## Bugs found in the agent's drafts during compile-fail-retry (for the record)

The four error classes below were all in the agent's initial drafts, not in PNT+ upstream
(base commit 7715064 builds cleanly — verified at bootstrap, claim #2). Root causes:

1. `add_left_inj (f 1)` has type `(f 1 + a = f 1 + b) → a = b` but the draft's
   equality was `f 1 + f 1 = f 1 + 0` (0 on the wrong side). Fixed: subtract `f 1`
   via `congrArg`/`rw [h1.symm]` + `simpa [add_assoc]`.
2. `simp [Nat.pow_zero, map_one hf]` — `Nat.pow_zero` unused in this mathlib version
   (linter warning, promoted to fatal in the retry loop). Fixed: `simp [map_one hf]`.
3. `pow_ne_zero` argument order: this mathlib's `Nat.pow_ne_zero` takes
   `(n ≠ 0)` first, `(a ≠ 0)` second. Fixed ordering in the induction step.
4. Log bridge: (a) `Real.log_mul` needs `x ≠ 0` / `y ≠ 0` but the context only has
   `0 < f n` — closed with `by linarith [hpos m]`; (b) `toArithmeticFunction` introduces
   `if n = 0 then 0 else …` ite branches — cleared with `simp only [toArithmeticFunction,
   coe_mk, mul_eq_zero]` + final `simp [hm, hn]` (note: bare `simp` does not discharge the
   ites with the local `≠` hypotheses in this mathlib version; explicit `[hm, hn]` is required).

## Filing status

`gh` CLI not installed / no GitHub credentials on this machine → the issue/PR
filing needs the owner. Ready-to-paste text: `issue-816-draft.md` (target: PNT+ issue #816,
"[IK]: Make ToAdditive version of IsMultiplicative for Arithmetic functions", open, label `task`
— verified via public GitHub API 08-22).
The branch is local at `ik-additive-lemmas`; push + PR when credentials available.

## Files

- `iwaniec-ik-api.patch` — full commit (git show 0197a66)
- `build-final.txt` — verbatim tail of the successful `lake build`
- `issue-816-draft.md` — ready-to-paste issue/PR text for the owner
- `check.sh` — re-runs the checker (promote.sh runs this for FORMAL)
