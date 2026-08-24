#!/usr/bin/env python3
"""Track E (tick 182): F2c — close the (1e7, 10810800) record-holder gap.

Pre-registered (logs/2026-08-24.tick.log TICK 182):
  F2c: strict record-holders of sigma(n)/n for n <= 10810800 (exact int64
      divisor sieve, same method as F2) == b-file entries <= 10810800.
  Confirms (i) 10810800 IS a record-holder and (ii) NO record-holder in
      (8648640, 10810800). Closes the gap between F2 (n<=1e7) and F2b
      (gaps with a>=1e7, first (10810800,21621600)).
  DEAD on any mismatch.

Why 10810800: it is the first b-file (SA) entry > 1e7. F2's scan stopped at
  1e7 (last holder 8648640); F2b's gap list starts at a>=1e7. The interval
  (1e7, 10810800) was covered by neither. Extending the exact record-holder
  scan to 10810800 covers it and confirms 10810800 is a record-holder.
"""
import time
import numpy as np

N = 10810800
BFILE = "evidence/2026-08-24-lagarias-sa/a004394.txt"

def parse_bfile(path, bound):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) != 2 or not parts[1].isdigit():
                continue
            v = int(parts[1])
            if v <= bound:
                out.append(v)
    return out

def main():
    t0 = time.time()
    sigma = np.ones(N + 1, dtype=np.int64)
    for d in range(2, N + 1):
        sigma[d::d] += d
    t_sieve = time.time() - t0

    holders = []
    max_num, max_den = 0, 1
    for n in range(1, N + 1):
        s = int(sigma[n])
        if s * max_den > max_num * n:   # s/n > max_num/max_den, exact
            holders.append(n)
            max_num, max_den = s, n
    t_hold = time.time() - t0

    bf = parse_bfile(BFILE, N)
    print(f"sieve {t_sieve:.1f}s; record-holder scan {t_hold:.1f}s")
    print(f"strict record-holders (exact): {len(holders)}")
    print(f"b-file entries <= {N}: {len(bf)}")
    print(f"last 6 holders:   {holders[-6:]}")
    print(f"last 6 b-file:    {bf[-6:]}")
    # specifically: any holder in (1e7, 10810800]?
    in_gap = [h for h in holders if h > 10**7]
    print(f"holders in (1e7, {N}]: {in_gap}")
    match = (holders == bf)
    if not match:
        for i in range(max(len(holders), len(bf))):
            h = holders[i] if i < len(holders) else None
            b = bf[i] if i < len(bf) else None
            if h != b:
                print(f"FIRST MISMATCH at index {i}: holder={h} b-file={b}")
                break
    print(f"VERDICT F2c: {'PASS' if match else 'DEAD'}")
    print(f"total {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
