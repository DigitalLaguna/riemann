#!/usr/bin/env python3
"""Track E (tick 180): F2 — b-file == strict sigma(n)/n record-holders, n <= 1e7.

Pre-registered (logs/2026-08-24.tick.log TICK 177):
  F2: strict record-holders of sigma(n)/n for n <= 1e7 (exact int64 divisor
      sieve) == b-file entries <= 1e7. DEAD on any mismatch (b-file wrong or
      incomplete below 1e7).

Method: exact int64 divisor-sum sieve (numpy) for sigma(n), n <= 1e7; a number
is a strict record-holder iff sigma(n)/n > max_{k<n} sigma(k)/k, compared
exactly by cross-multiplication in Python ints (no float). Superabundant
numbers (OEIS A004394) are exactly the strict record-holders of sigma(n)/n.
"""
import time
import numpy as np

N = 10**7
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
    print(f"first 12 holders: {holders[:12]}")
    print(f"first 12 b-file:  {bf[:12]}")
    print(f"last 5 holders:   {holders[-5:]}")
    print(f"last 5 b-file:    {bf[-5:]}")
    match = (holders == bf)
    if not match:
        for i in range(max(len(holders), len(bf))):
            h = holders[i] if i < len(holders) else None
            b = bf[i] if i < len(bf) else None
            if h != b:
                print(f"FIRST MISMATCH at index {i}: holder={h} b-file={b}")
                break
    print(f"VERDICT F2: {'PASS' if match else 'DEAD'}")
    print(f"total {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
