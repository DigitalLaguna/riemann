#!/usr/bin/env bash
# Checker for claim #12: PNT+ IK additive-API lemmas build locally.
# Machine-verifies: branch/commit, lemma presence, full lake build exit 0, no new sorries.
set -u
PNT=/home/niklas/riemann/tracks/a-lean/pnt
export PATH="$HOME/.elan/bin:$PATH"
fail() { echo "CHECK FAIL: $1"; exit 1; }

cd "$PNT" || fail "pnt dir missing"
[ "$(git branch --show-current)" = "ik-additive-lemmas" ] || fail "wrong branch: $(git branch --show-current)"
git merge-base --is-ancestor 7715064 HEAD || fail "base commit 7715064 not ancestor of HEAD"
git diff --quiet || fail "dirty tree in pnt"

F=PrimeNumberTheoremAnd/IwaniecKowalskiCh1.lean
grep -q "^lemma IsCompletelyAdditive.map_one " "$F" || fail "map_one lemma missing"
grep -q "^lemma IsCompletelyAdditive.map_prime_pow " "$F" || fail "map_prime_pow lemma missing"
grep -q "^theorem isMultiplicative_log_isAdditive " "$F" || fail "log bridge theorem missing"

# pre-existing sorry count at base commit (must not grow)
BASE_SORRY=$(git show 7715064:"$F" | grep -c "sorry")
NOW_SORRY=$(grep -c "sorry" "$F")
[ "$NOW_SORRY" -le "$BASE_SORRY" ] || fail "sorry count grew: base=$BASE_SORRY now=$NOW_SORRY"

lake build > /tmp/claim12-build.log 2>&1 || { tail -20 /tmp/claim12-build.log; fail "lake build failed"; }
grep -q "Build completed successfully" /tmp/claim12-build.log || fail "no success line in build log"
echo "CHECK PASS: branch ik-additive-lemmas @ $(git log --oneline -1 | cut -c1-9), 3 lemmas present, sorry count $NOW_SORRY (base $BASE_SORRY), lake build exit 0"
