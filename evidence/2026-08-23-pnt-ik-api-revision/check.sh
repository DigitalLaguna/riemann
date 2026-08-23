#!/usr/bin/env bash
# Checker for claim #25: revised PNT+ IK additive-API lemmas (v2) build locally.
# Machine-verifies: branch, base 751a8c2, revised lemma names/contexts,
# sorry count not grown vs base, full lake build exit 0.
set -u
PNT=/home/niklas/riemann/tracks/a-lean/pnt
export PATH="$HOME/.elan/bin:$PATH"
fail() { echo "CHECK FAIL: $1"; exit 1; }

cd "$PNT" || fail "pnt dir missing"
[ "$(git branch --show-current)" = "ik-additive-lemmas" ] || fail "wrong branch: $(git branch --show-current)"
git merge-base --is-ancestor 751a8c2 HEAD || fail "base commit 751a8c2 not ancestor of HEAD"
[ "$(git rev-list --count 751a8c2..HEAD)" = "1" ] || fail "expected exactly 1 commit over base, got $(git rev-list --count 751a8c2..HEAD)"
git diff --quiet || fail "dirty tree in pnt"

F=PrimeNumberTheoremAnd/IwaniecKowalskiCh1.lean
# revised names and weakened contexts
grep -q "^lemma IsCompletelyAdditive.map_one \[AddCancelMonoid R\]" "$F" || fail "map_one [AddCancelMonoid R] missing"
grep -q "^lemma IsCompletelyAdditive.map_prime_pow \[AddCancelMonoid R\]" "$F" || fail "map_prime_pow [AddCancelMonoid R] missing"
grep -q "^theorem ArithmeticFunction.IsMultiplicative.isAdditive_log " "$F" || fail "isAdditive_log theorem missing"
# vacuity fix: hypothesis must exclude n = 0
grep -q "(hpos : ∀ n ≠ 0, 0 < f n)" "$F" || fail "isAdditive_log still has vacuous ∀ n, 0 < f n hypothesis"
# old over-weak/over-strong contexts must be gone from the added block
ADDED=$(git diff 751a8c2 HEAD -- "$F")
echo "$ADDED" | grep -q "AddGroupWithOne" && fail "AddGroupWithOne still present in added lines"

# pre-existing sorry count at base commit (must not grow)
BASE_SORRY=$(git show 751a8c2:"$F" | grep -c "sorry")
NOW_SORRY=$(grep -c "sorry" "$F")
[ "$NOW_SORRY" -le "$BASE_SORRY" ] || fail "sorry count grew: base=$BASE_SORRY now=$NOW_SORRY"

lake build > /tmp/claim25-build.log 2>&1 || { tail -20 /tmp/claim25-build.log; fail "lake build failed"; }
grep -q "Build completed successfully" /tmp/claim25-build.log || fail "no success line in build log"
echo "CHECK PASS: branch ik-additive-lemmas @ $(git log --oneline -1 | cut -c1-9), revised 3 lemmas (AddCancelMonoid x2, isAdditive_log with n≠0 hypothesis), sorry count $NOW_SORRY (base $BASE_SORRY), lake build exit 0"
