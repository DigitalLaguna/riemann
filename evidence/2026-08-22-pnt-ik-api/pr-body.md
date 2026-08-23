# PR filing sheet — PNT+ issue #816 (staged 2026-08-23, manual session after tick 125)

- Fork: `DigitalLaguna/PrimeNumberTheoremAnd` (owner fork, 2026-08-23)
- Branch pushed to fork: `ik-additive-lemmas` @ `0197a66f3440c636a3ce3ba434389be873c24f04`
  (verified via GitHub API; = claim #12 commit, base `7715064`)
- Open the PR via:
  https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
- Base: `AlexKontorovich:main` · Head: `DigitalLaguna:ik-additive-lemmas`
- After opening: comment `propose #<PR number>` on issue #816 (CONTRIBUTING step 4).

## Title (paste)

[IK Ch.1] Additive-API lemmas: `IsCompletelyAdditive.map_one`, `map_prime_pow`, log-bridge (issue #816)

## Body (paste)

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
Patch: 40 added lines, no deletions.

Base note: branch is based on `7715064` (main at clone time); the two subsequent
main commits (`e94b9fb`, `751a8c2`) touch only FKS2 files, no overlap with
`IwaniecKowalskiCh1.lean`.

**AI disclosure** (per PULL_REQUEST_STYLE.md §13): Made with an AI coding agent —
local Qwen3.8-27B (llama-server) with frontier-model escalation; tool not in the
label table, the umbrella `ai` label suffices (a new label is welcome).

## Issue #816 situation (decide before/with filing)

Issue is OPEN, label `task`, but ASSIGNED to `IlPreteRosso` since 2026-01-28
(`claim` comment); last activity 2026-02-04: "Waiting for Mathlib to merge relevant
code before the next update on this issue." CONTRIBUTING additional guideline 1:
don't work an issue assigned to another contributor without prior communication.
Options: (i) comment on #816 pinging @IlPreteRosso (claim is ~7 months old) and
filing in parallel, or (ii) wait for the claimant to disclaim. Owner call.
