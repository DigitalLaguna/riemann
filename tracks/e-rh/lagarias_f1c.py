#!/usr/bin/env python3
"""Track E (tick 181): F1c — B_n strictly increasing for 1e7 <= n <= 1e10.

Pre-registered (logs/2026-08-24.tick.log TICK 181):
  F1c: all 9999990000 gaps B_{n+1}-B_n for n in [1e7, 1e10-1] > 0
       (float64 EM H_n; complements F1b's [1, 1e7]).
       ERR_H_c = 1e-14, LIP_c = 6.737, ERR_B_c = 7.74e-14, ERR_GAP_c = 1.55e-13.
       PASS: (i) no computed decrease, (ii) min gap > 10*ERR_GAP_c,
       (iii) 202-point 100-digit spot check < 1e-12 (seed 181).
       DEAD if any decrease, ratio <= 10, or spot-check mismatch.

Why needed: the extension claim (Lagarias for all n <= 1e10) requires
B_m <= B_n for m = largest record-holder <= n, n up to 1e10; F1b covers
only [1, 1e7]; macarevey-2026 Prop 2.1 (analytic, n >= 55) is not
machine-verified. F1c closes the (1e7, 1e10] leg with a machine.

Method and explicit error bounds (n in [1e7, 1e10]):
  H_n (float64): EM  log n + gamma + 1/(2n) - 1/(12n^2) + 1/(120n^4)
    truncation err < 1/(252 n^6) < 1e-42 (negligible)
    float64 rounding: 5 ops on values in [16.69, 23.61], ulp <= 3.55e-15,
    each add rounds by < 0.5 ulp = 1.78e-15; 4 adds + log itself < 1e-14
    (absorption of the 1/(12n^2), 1/(120n^4) terms into the sum's rounding
    adds at most their magnitudes, <= 8.4e-17, negligible)
    => |err H_n| < 1e-14 =: ERR_H_c
  B_n = (H_n + exp(H_n) log H_n)/n in float64.
    f(H) = H + e^H log H; f'(H) = 1 + e^H (log H + 1/H).
    e^{H_n}/n = e^{gamma + 1/(2n) - 1/(12n^2) + 1/(120n^4)} < e^{gamma + 5e-8} < 1.7812
    log H + 1/H <= log 23.61 + 1/16.69 = 3.2210
    => f'(H_n)/n < 1 + 1.7812*3.2210 = 6.737 =: LIP_c
    B-op rounding (exp/log/mul/add/div; intermediates <= 5.6e10, ulp <= 7.5e-6,
    propagated /n >= 1e7): < 5e-15; flat bound 1e-14.
    => |err B_n| <= LIP_c*ERR_H_c + 1e-14 = 7.74e-14 =: ERR_B_c
  Gap g_n = B_{n+1} - B_n: |err g_n| <= 2*ERR_B_c = 1.55e-13 =: ERR_GAP_c
  PASS requires: (i) no computed decrease, (ii) min gap > 10*ERR_GAP_c,
    (iii) all spot checks |B_100dig - B_64| < 1e-12.
"""
import math, random, time
import numpy as np
import mpmath as mp

N0 = 10**7
N1 = 10**10
CHUNK = 10**8
GAMMA64 = 0.5772156649015329
ERR_H_C = 1e-14
LIP_C = 6.737
ERR_B_C = LIP_C * ERR_H_C + 1e-14
ERR_GAP_C = 2.0 * ERR_B_C

def B64(n):
    inv = 1.0 / n
    inv2 = inv * inv
    Hn = (math.log(n) + GAMMA64 + 0.5 * inv
          - (1.0 / 12.0) * inv2 + (1.0 / 120.0) * inv2 * inv2)
    return (Hn + math.exp(Hn) * math.log(Hn)) / n

def main():
    t0 = time.time()
    min_gap = float('inf'); min_gap_n = None
    n = N0
    while n < N1:
        m = min(n + CHUNK, N1)
        nf = np.arange(n, m + 1, dtype=np.float64)
        H = np.log(nf)
        H += GAMMA64
        H += 0.5 / nf
        H -= (1.0 / 12.0) / (nf * nf)
        H += (1.0 / 120.0) / (nf * nf * nf * nf)
        B = (H + np.exp(H) * np.log(H)) / nf
        g = np.diff(B)
        i = int(g.argmin())
        if g[i] < min_gap:
            min_gap = float(g[i]); min_gap_n = n + i
        n = m
    t_scan = time.time() - t0
    print(f"scan: {N1 - N0 - 1} gaps checked (n in [{N0}, {N1-1}]), {t_scan:.1f}s")
    print(f"min gap: {min_gap:.6e} at n={min_gap_n} (gap B_{min_gap_n+1}-B_{min_gap_n})")
    print(f"gap at n={N1-1}: {B64(N1) - B64(N1-1):.6e}")
    print(f"ERR_H_c={ERR_H_C:.1e}  LIP_c={LIP_C}  ERR_B_c={ERR_B_C:.3e}  ERR_GAP_c={ERR_GAP_C:.3e}")
    ratio = min_gap / ERR_GAP_C
    print(f"min_gap / ERR_GAP_c = {ratio:.3e}  (spec requires > 10)")
    no_decrease = min_gap > 0

    mp.mp.dps = 100
    def B100(n):
        H = mp.digamma(n + 1) + mp.euler
        return (H + mp.e**H * mp.log(H)) / n

    rng = random.Random(181)
    pts = [min_gap_n, min_gap_n + 1] + [rng.randint(N0, N1 - 1) for _ in range(200)]
    worst, worst_n = 0.0, None
    for n in pts:
        d = abs(float(B100(n)) - B64(n))
        if d > worst:
            worst, worst_n = d, n
    print(f"spot checks: {len(pts)} points (min-gap endpoints + 200 random, seed 181)")
    print(f"max |B_100dig - B_64| = {worst:.3e} at n={worst_n}  (spec requires < 1e-12)")
    spot_ok = worst < 1e-12

    verdict = "PASS" if (no_decrease and ratio > 10 and spot_ok) else "DEAD"
    print(f"no computed decrease: {no_decrease}")
    print(f"VERDICT F1c: {verdict}")
    print(f"total {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
