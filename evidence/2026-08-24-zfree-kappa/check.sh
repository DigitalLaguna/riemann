#!/usr/bin/env bash
# Checker: bellotti-trudgian-yang-2026 Theorem 1 proof, final line (p. 25), is
# missing a factor of kappa in the denominator. Paper writes
#   (a*kappa/2) f(0) log t > 1.02928  ==>  eta log t > 1.02928/(a*kappa*w(0)/2)
# but Definition 2 (p. 11) gives f(0) = eta*w(0)*kappa, so the correct
# implication is eta log t > 1.02928/(a*kappa^2*w(0)/2). With kappa = 433/859
# (paper line 1896; machine-verified as the exact sum of the eq (18) kappa_m
# coefficients, which also satisfy the approximation property (17)), the
# correct zero-free constant is A_corr = A_paper*kappa = 2.467799 < 4.896.
# Re-runs kappa-sum.py (exact Fraction arithmetic) and asserts F1-F3 PASS +
# VERDICT + byte-identical regression vs the recorded run.
set -euo pipefail
cd "$(dirname "$0")/../.."
EV="$(cd "$(dirname "$0")" && pwd)"
OUT="$(python3 tracks/c-constants/zfree-4896/kappa-sum.py)"
for f in F1 F2 F3; do
  printf '%s\n' "$OUT" | grep -q "^$f .* -> PASS" || { echo "CHECK FAIL: $f not PASS"; exit 1; }
done
printf '%s\n' "$OUT" | grep -q "^VERDICT: ALL CHECKS PASS$" || { echo "CHECK FAIL: verdict"; exit 1; }
printf '%s\n' "$OUT" | diff - "$EV/machine-run-kappa-sum.txt" >/dev/null \
  || { echo "CHECK FAIL: rerun differs from recorded run"; exit 1; }
echo "CHECK PASS"
