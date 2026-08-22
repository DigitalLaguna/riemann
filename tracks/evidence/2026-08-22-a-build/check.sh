#!/usr/bin/env bash
# check.sh — claim: 3 IK ch1 lemmas compile in PNT+ (branch ik-additive-lemmas on 7715064).
set -euo pipefail
cd "$(dirname "$0")/../../tracks/a-lean/pnt"
F=PrimeNumberTheoremAnd/IwaniecKowalskiCh1.lean
grep -q "lemma IsCompletelyAdditive.map_one" "$F"
grep -q "lemma IsCompletelyAdditive.map_prime_pow" "$F"
grep -q "theorem isMultiplicative_log_isAdditive" "$F"
if sed -n '63,105p' "$F" | grep -qw sorry; then echo "SORRY in lemma block (lines 63-105)" >&2; exit 1; fi
out=$(lake build PrimeNumberTheoremAnd.IwaniecKowalskiCh1 2>&1) || { echo "$out" | tail -20 >&2; exit 1; }
echo "$out" | grep -q "Build completed successfully" || { echo "$out" | tail -20 >&2; exit 1; }
echo "CHECK PASS: 3 IK lemmas compile (lake build module IwaniecKowalskiCh1, sorry-free)"
