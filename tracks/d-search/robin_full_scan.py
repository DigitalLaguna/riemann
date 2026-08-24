#!/usr/bin/env python3
"""Track D sixth experiment: Robin-criterion FULL scan over [A, B).

Robin's criterion (Lagarias 2002, eq 1.2, p.2): RH <=> sigma(n) < e^gamma * n * log log n
for all n >= 5041. This scans ALL n in [A,B) and checks the inequality directly
(no CA/SA reduction), finding the near-miss R(n) = sigma(n)/(e^gamma*n*log log n).
Original range [1e8, 1e9+1) produced claim #26; tick 167 generalized the range
(A, B, L, SA_REF as argv 1-4) and launched [1e9, 1e10+1).

Method: segmented multiplicative sieve (exact int64; sigma(n) < ~5e10 for n<=1e10,
no overflow). For each subsegment [a,b) of width L:
  - rem = [a..b-1] (int64), sigma = ones (int64).
  - For each prime p <= isqrt(B-1): for multiples of p in [a,b), multiply sigma by
    the p-power sum (1+p+...+p^v) and divide rem by p^v.
  - After all small primes, rem[i] is 1 or a prime > isqrt(B-1) (since p^2 > B-1 >= n);
    if >1, multiply sigma by (1+rem[i]).
  - sigma[i] = sigma(a+i) exactly.

Pre-registered checks (falsification tests; [1e8,1e9): logs/2026-08-23.tick.log
tick 128; [1e9,1e10): logs/2026-08-24.tick.log tick 167):
  F1 (cross-check): sieve sigma(n) == sympy.divisor_sigma(n) for the SA numbers in
     [A,B), edge cases, and 20 seeded-random n. Any mismatch => sieve bug => result invalid.
  F2 (WITNESS, constraint 5): if R(n) >= 1 for ANY n in [A,B) => RH FALSE => STOP.
     Verified in mpmath (50 digits) at the argmax.
  F3a (consistency, 50 digits): full-scan max R >= SA max R, both computed in-script
     at 50 digits from exact (sympy-cross-checked) sigmas. If lower => sieve missed an SA number.
  F3b (regression, display): the 12-significant-digit display of the full-scan max equals
     SA_REF (the 12-sig-digit display of the SA max R for this range, from the SA scan).
     For [1e8,1e9): SA_REF = 0.968152104902 (claim #23). Tick-128 F3 FAIL was a
     display-rounding artifact, resolved at 80 digits (evidence f3-resolution.txt).
Exit 0 iff F1 and F3 pass and no F2 witness hit.

Usage: robin_full_scan.py [A] [B] [L] [SA_REF]
  defaults: A=1e8, B=1e9+1, L=1e8, SA_REF=0.968152104902
"""
import math
import sys
import time
import random
import numpy as np
import sympy
import mpmath as mp

mp.mp.dps = 50
EULER_GAMMA = mp.mpf("0.57721566490153286060651209008240243104215933593992")
EG_MP = mp.e ** EULER_GAMMA
EG = float(math.exp(0.57721566490153286060651209008240243104215933593992))
BFILE = "evidence/2026-08-23-robin-1e9/b004394.txt"   # OEIS A004394 (superabundant numbers)
SA_REF_DEFAULT = "0.968152104902"   # claim #23: 12-SIG-DIGIT DISPLAY of the SA max R in (1e8,1e9]
# (the underlying 60-digit value is 0.96815210490180933969..., which ROUNDS UP to this
# display — see evidence/2026-08-23-robin-full-scan/f3-resolution.txt)


def read_seq(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                out.append(int(parts[1]))
    return out


def primes_upto(n):
    is_p = np.ones(n + 1, dtype=bool)
    is_p[0] = is_p[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_p[i]:
            is_p[i * i::i] = False
    return np.nonzero(is_p)[0].tolist()


def r_mp(n, sigma):
    return mp.mpf(sigma) / (EG_MP * mp.mpf(n) * mp.log(mp.log(mp.mpf(n))))


def nstr(x):
    return mp.nstr(x, 16)


def main():
    A = int(sys.argv[1]) if len(sys.argv) > 1 else 10**8
    B = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9 + 1
    L = int(sys.argv[3]) if len(sys.argv) > 3 else 10**8
    SA_REF = sys.argv[4] if len(sys.argv) > 4 else SA_REF_DEFAULT
    t0 = time.time()
    pmax = math.isqrt(B - 1)
    primes = primes_upto(pmax)
    sa_in_range = [n for n in read_seq(BFILE) if A <= n < B]
    print(f"range [{A},{B})  subseg width {L}  primes<={pmax}: {len(primes)}  "
          f"SA in range: {len(sa_in_range)}", flush=True)

    rng = random.Random(128)
    check_set = set(sa_in_range)
    check_set.update([A, B - 1, A + 1, B - 2, 999999937, 134217728, 387420489])
    check_set.update(rng.randint(A, B - 1) for _ in range(20))
    check_set = {c for c in check_set if A <= c < B}
    check_sigma = {}

    best_R = -1.0
    best_n = None
    best_sigma = None
    n_sub = 0
    for a in range(A, B, L):
        b = min(a + L, B)
        n = b - a
        rem = np.arange(a, b, dtype=np.int64)
        sigma = np.ones(n, dtype=np.int64)
        for p in primes:
            if p > b:
                break
            start = ((a + p - 1) // p) * p
            if start >= b:
                continue
            idx = np.arange(start, b, p) - a
            tmp = rem[idx].copy()
            power_sum = np.ones(len(idx), dtype=np.int64)
            power = np.ones(len(idx), dtype=np.int64)
            while True:
                mask = (tmp % p) == 0
                if not mask.any():
                    break
                tmp[mask] //= p
                power[mask] *= p
                power_sum[mask] += power[mask]
            sigma[idx] *= power_sum
            rem[idx] = tmp
        large = rem > 1
        if large.any():
            sigma[large] *= (1 + rem[large])
        nn = np.arange(a, b, dtype=np.float64)
        ll = np.log(np.log(nn))
        R = sigma.astype(np.float64) / (EG * nn * ll)
        i = int(np.argmax(R))
        if R[i] > best_R:
            best_R = float(R[i])
            best_n = int(a + i)
            best_sigma = int(sigma[i])
        for c in check_set:
            if a <= c < b:
                check_sigma[c] = int(sigma[c - a])
        n_sub += 1
        print(f"subseg {n_sub}: [{a},{b}) running best_R={best_R:.12f} at n={best_n} "
              f"({time.time()-t0:.1f}s)", flush=True)
        del rem, sigma, R, nn, ll

    R_best_mp = r_mp(best_n, best_sigma)
    print(f"\nFULL SCAN [{A},{B}): max R = {nstr(R_best_mp)} at n = {best_n} (sigma={best_sigma})",
          flush=True)
    print(f"1 - R = {nstr(1 - R_best_mp)}", flush=True)

    witness = R_best_mp >= 1
    print(f"F2 witness R(n)>=1 in [{A},{B}): "
          f"{'HIT n=%d R=%s' % (best_n, nstr(R_best_mp)) if witness else 'none (max R < 1)'}", flush=True)

    print(f"R at SA numbers in [{A},{B}) (mpmath):", flush=True)
    sa_max_mp = mp.mpf(0)
    for s in sa_in_range:
        if s in check_sigma:
            rs = r_mp(s, check_sigma[s])
            sa_max_mp = max(sa_max_mp, rs)
            print(f"  n={s} sigma={check_sigma[s]} R={nstr(rs)}", flush=True)

    mism = 0
    for c in sorted(check_sigma):
        ref = int(sympy.divisor_sigma(c))
        if ref != check_sigma[c]:
            mism += 1
            print(f"  MISMATCH n={c}: sieve={check_sigma[c]} sympy={ref}", flush=True)
    print(f"F1 cross-check: checked={len(check_sigma)} mismatches={mism}: "
          f"{'PASS' if mism == 0 else 'FAIL'}", flush=True)

    f3a = R_best_mp >= sa_max_mp
    print(f"F3a consistency: full-scan max R {nstr(R_best_mp)} >= SA max (50-digit) "
          f"{nstr(sa_max_mp)}: {'PASS' if f3a else 'FAIL'}", flush=True)
    f3b = mp.nstr(R_best_mp, 12) == SA_REF
    print(f"F3b regression: 12-sig-digit display of full-scan max == SA_REF "
          f"{SA_REF}: {'PASS' if f3b else 'FAIL'}", flush=True)

    ok = (mism == 0) and (not witness) and f3a and f3b
    print(f"VERDICT: {'ALL CHECKS PASS' if ok else 'CHECK FAILURE'}", flush=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
