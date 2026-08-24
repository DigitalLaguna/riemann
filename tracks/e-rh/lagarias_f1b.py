#!/usr/bin/env python3
"""Track E (tick 180): F1b — B_n strictly increasing for 1 <= n <= 1e7.

Pre-registered (logs/2026-08-24.tick.log TICK 177):
  F1b: B_n strictly increasing for 1 <= n <= 1e7 (float64 Euler-Maclaurin H_n,
       explicit error bound < 1e-13; min gap must exceed 10x the error bound).
       100-digit re-evaluation at the min-gap n + 200 seeded-random n
       (seed 177) must agree with float64 to < 1e-12.
  DEAD if any decrease or spot-check mismatch.

Method and explicit error bounds:
  H_n (float64):
    n <= 100:  exact Fraction -> float64 (correctly rounded; err < 5e-16)
    n > 100:   EM  log n + gamma + 1/(2n) - 1/(12n^2) + 1/(120n^4)
               truncation err < 1/(252 n^6) < 3.73e-15 (at n = 101)
               + float64 rounding of the ~5 ops on O(17) values < 1e-14
    => |err H_n| < 1.4e-14 < 1e-13 =: ERR_H   (spec bound satisfied)
  B_n = (H_n + exp(H_n) log H_n)/n in float64.
    f(H) = H + e^H log H;  f'(H) = 1 + e^H (log H + 1/H).
    For H in [1, 16.70]: e^{H_n}/n <= e^1/1 = 2.718 (e^{H_n}/n = e^gamma(1+O(1/n)),
    decreasing, max at n=1); log H + 1/H <= log 16.70 + 1/16.70 = 2.875.
    => f'(H_n)/n <= 1 + 2.718*2.875 = 8.815 =: LIP
    => |err B_n| <= LIP*ERR_H + 2e-14 (rounding of B ops) =: ERR_B
  Gap g_n = B_{n+1} - B_n: |err g_n| <= 2*ERR_B =: ERR_GAP.
  PASS requires: (i) no computed decrease, (ii) min gap > 10*ERR_GAP,
    (iii) all spot checks |B_100dig - B_64| < 1e-12.
"""
import math, random, time
from fractions import Fraction
import mpmath as mp

N = 10**7
GAMMA64 = 0.5772156649015329          # float64 nearest to Euler's constant
ERR_H = 1e-13
LIP = 8.815
ERR_B = LIP * ERR_H + 2e-14
ERR_GAP = 2.0 * ERR_B

def H64(n, H_exact):
    if n <= 100:
        return H_exact[n]
    inv = 1.0 / n
    inv2 = inv * inv
    return (math.log(n) + GAMMA64 + 0.5 * inv
            - (1.0 / 12.0) * inv2 + (1.0 / 120.0) * inv2 * inv2)

def B64(n, H_exact):
    Hn = H64(n, H_exact)
    return (Hn + math.exp(Hn) * math.log(Hn)) / n

def main():
    t0 = time.time()
    acc = Fraction(0, 1)
    H_exact = {}
    for n in range(1, 101):
        acc += Fraction(1, n)
        H_exact[n] = float(acc)

    min_gap = float('inf'); min_gap_n = None
    prev_B = None
    for n in range(1, N + 1):
        Bn = B64(n, H_exact)
        if prev_B is not None:
            g = Bn - prev_B
            if g < min_gap:
                min_gap = g; min_gap_n = n - 1
        prev_B = Bn
    t_scan = time.time() - t0
    print(f"scan: {N-1} gaps checked, {t_scan:.1f}s")
    print(f"min gap: {min_gap:.6e} at n={min_gap_n} (gap B_{min_gap_n+1}-B_{min_gap_n})")
    print(f"ERR_H={ERR_H:.1e}  LIP={LIP}  ERR_B={ERR_B:.3e}  ERR_GAP={ERR_GAP:.3e}")
    ratio = min_gap / ERR_GAP
    print(f"min_gap / ERR_GAP = {ratio:.3e}  (spec requires > 10)")
    no_decrease = min_gap > 0

    # spot checks: min-gap endpoints + 200 seeded-random n (seed 177)
    mp.mp.dps = 100
    def B100(n):
        H = mp.digamma(n + 1) + mp.euler
        return (H + mp.e**H * mp.log(H)) / n

    rng = random.Random(177)
    pts = [min_gap_n, min_gap_n + 1] + [rng.randint(1, N) for _ in range(200)]
    worst, worst_n = 0.0, None
    for n in pts:
        d = abs(float(B100(n)) - B64(n, H_exact))
        if d > worst:
            worst, worst_n = d, n
    print(f"spot checks: {len(pts)} points (min-gap endpoints + 200 random, seed 177)")
    print(f"max |B_100dig - B_64| = {worst:.3e} at n={worst_n}  (spec requires < 1e-12)")
    spot_ok = worst < 1e-12

    verdict = "PASS" if (no_decrease and ratio > 10 and spot_ok) else "DEAD"
    print(f"no computed decrease: {no_decrease}")
    print(f"VERDICT F1b: {verdict}")
    print(f"total {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
