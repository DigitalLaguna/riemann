# PR filing sheet — PNT+ issue #816 (rev 2, 2026-08-23 ~05:30 UTC, after owner review)

- Fork: `DigitalLaguna/PrimeNumberTheoremAnd`
- Branch on fork: `ik-additive-lemmas` @ `67661abc6ff51bc570aca7f93f85a3565bfe2afb`
  (single commit over `751a8c2` = current upstream main; supersedes 0197a66/claim #12
  via claim #25 FORMAL)
- Open the PR via:
  https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/compare/main...DigitalLaguna:ik-additive-lemmas?expand=1
- Base: `AlexKontorovich:main` · Head: `DigitalLaguna:ik-additive-lemmas`
- After opening: comment `propose #<PR number>` on issue #816 (CONTRIBUTING step 4).
- NOTE: a web-UI merge commit (192dd05, "Merge AlexKontorovich:main into
  ik-additive-lemmas") was created on the fork branch during PR-form fiddling and
  then replaced by force-push of the clean rebased commit — no PR was opened, so
  nothing dangles.

## Title

Default (auto-filled from the commit, matches house style):
```
feat(IK): prove IsCompletelyAdditive.map_one, map_prime_pow, IsMultiplicative.isAdditive_log (issue #816)
```
Shorter alternative if you prefer:
```
feat(IK): additive-API lemmas for IwaniecKowalskiCh1 (issue #816)
```

## Body (paste)

Fills the TODO at `PrimeNumberTheoremAnd/IwaniecKowalskiCh1.lean:62`:

> **Think about more API for additive/completely additive functions, e.g. `f (p^k) = k * f p` for prime p, etc.**

Three lemmas, each with `@[blueprint]` attributes matching the file's conventions:

1. **`IsCompletelyAdditive.map_one`** — `f 1 = 0` for completely additive `f`
   (context: `AddCancelMonoid R`).
2. **`IsCompletelyAdditive.map_prime_pow`** — `f (p ^ k) = k • f p` for prime `p`:
   the TODO's example itself (as `k • f p`, since the value type is an additive
   group) (context: `AddCancelMonoid R`).
3. **`ArithmeticFunction.IsMultiplicative.isAdditive_log`** — if `f` is
   multiplicative with `f n > 0` for all `n ≠ 0`, then `log ∘ f` is additive on
   coprime arguments:
   `IsAdditive (toArithmeticFunction (fun n => Real.log (f n)))`.
   Proof: `hf.map_mul_of_coprime` + `Real.log_mul`. (The `n ≠ 0` in the
   positivity hypothesis is essential: an `ArithmeticFunction` maps `0` to `0`,
   so `∀ n, 0 < f n` is unsatisfiable and the lemma would be vacuous.)

Verified: full local build succeeds with the project-pinned toolchain
(`leanprover/lean4:v4.32.2`, mathlib `v4.32.2`), based on current `main`:

    $ lake build
    Build completed successfully (4343 jobs).

No new `sorry`s; the 7 pre-existing `sorry` warnings are untouched.
Patch: 41 added lines, no deletions.

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
