#!/usr/bin/env python3
"""Track E (tick 180): F1a — finite leg of macarevey-2026 Cor 2.1.

Pre-registered (logs/2026-08-24.tick.log TICK 177):
  F1a: B_{n+1} - B_n > 0 for 1 <= n <= 54 at 100 digits, where
      B_n = (H_n + e^{H_n} log H_n)/n, H_n = nth harmonic number.
  DEAD if any n in [1,54] has B_{n+1} <= B_n at 100 digits.

Method:
  Primary: H_n as an EXACT Fraction (the exact value of the paper's
      H_n = psi(n+1)+gamma for integer n), converted to mpf at 100 dps via
      mpf(num)/mpf(den) (both exact ints, one correctly-rounded division).
  Cross-check: H_n = mp.digamma(n+1)+mp.euler at 100 dps (the F3 / claim-#10
      method). Both must give the same sign pattern; max |diff_p - diff_d|
      reported.
"""
import time
from fractions import Fraction
import mpmath as mp

def H_frac(n):
    s = Fraction(0, 1)
    for k in range(1, n + 1):
        s += Fraction(1, k)
    return s

def main():
    t0 = time.time()
    mp.mp.dps = 100
    # sanity: mpf(num)/mpf(den) is NOT a float64 round-trip
    assert mp.mpf(1) / mp.mpf(3) != mp.mpf(0.3333333333333333), \
        "mpf division went through float64"
    Hs = [H_frac(n) for n in range(1, 57)]  # exact, n = 1..56

    def B_primary(n):
        fr = Hs[n - 1]
        H = mp.mpf(fr.numerator) / mp.mpf(fr.denominator)
        return (H + mp.e**H * mp.log(H)) / n

    def B_digamma(n):
        H = mp.digamma(n + 1) + mp.euler
        return (H + mp.e**H * mp.log(H)) / n

    diffs_p, diffs_d = [], []
    for n in range(1, 55):
        dp = B_primary(n + 1) - B_primary(n)
        dd = B_digamma(n + 1) - B_digamma(n)
        diffs_p.append((n, dp))
        diffs_d.append((n, dd))
        print(f"n={n:2d}: B_{n+1}-B_n = {dp}")

    min_n, min_d = min(diffs_p, key=lambda t: t[1])
    max_cross = max(abs(p - d) for (_, p), (_, d) in zip(diffs_p, diffs_d))
    all_pos = all(d > 0 for _, d in diffs_p)
    same_sign = all((p > 0) == (d > 0) for (_, p), (_, d) in zip(diffs_p, diffs_d))
    print(f"min difference: {min_d} at n={min_n}")
    print(f"max |primary - digamma| over the 54 differences: {max_cross}")
    print(f"all 54 differences > 0 (primary, exact-H): {all_pos}")
    print(f"sign pattern identical (primary vs digamma): {same_sign}")
    verdict = "PASS" if (all_pos and same_sign) else "DEAD"
    print(f"VERDICT F1a: {verdict}")
    print(f"total {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
