#!/usr/bin/env bash
# Re-verifies: B_n = (H_n + e^{H_n} log H_n)/n strictly increasing, 1 <= n <= 1e7.
# F1a: all 54 differences B_{n+1}-B_n (1<=n<=54) > 0 at 100 digits (exact
#   harmonic numbers; digamma cross-check same sign pattern) — the finite leg
#   of macarevey-2026 Cor 2.1, independently re-verified.
# F1b: float64 Euler-Maclaurin scan of 9999999 gaps, no decrease, min gap
#   > 10x the explicit error bound, 202-point 100-digit spot check < 1e-12.
set -euo pipefail
cd "$(dirname "$0")/../.."
out_a=$(python3 tracks/e-rh/lagarias_f1a.py)
echo "$out_a"
echo "$out_a" | grep -q "VERDICT F1a: PASS"
out_b=$(python3 tracks/e-rh/lagarias_f1b.py)
echo "$out_b"
echo "$out_b" | grep -q "VERDICT F1b: PASS"
echo "CHECK PASS"
