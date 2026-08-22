#!/usr/bin/env python3
"""Track D first experiment: Mertens function M(x) = sum_{n<=x} mu(n), N = 10^8.

Exact integer arithmetic: mu as numpy int8, M as int32 prefix sums.
Cross-checks = pre-registered falsification tests F1-F4 (logs/2026-08-22.tick.log):
  C1 (F1): M(10) == -1 (hand-computed from mu(1..10)).
  C2 (F2): M(n) == OEIS A002321 b-file for all n <= 10000.
  C3 (F3): M(n) == independent sympy trial-division M(n) for all n <= 10^5.
  C4 (F4): first k with |M(k)| == n equals OEIS A051402 b-file a(n) for all
           n <= max_{x<=N} |M(x)| (record-envelope check).
Outputs M(10^k) k=1..8, the |M| record, the |M(x)|/sqrt(x) record, top-10 |M(x)|.
Exit 0 iff all checks pass.
"""
import math
import sys
import numpy as np

N = 10**8
EV = "evidence/2026-08-22-mertens"


def mu_sieve(n):
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = False
    primes = np.nonzero(is_prime)[0]
    mu = np.ones(n + 1, dtype=np.int8)
    mu[0] = 0
    for p in primes:
        mu[p::p] *= -1
        if p * p <= n:
            mu[p * p::p * p] = 0
    return mu


def first_attainment(absM, maxabs):
    """firstk[v] = smallest i with absM[i] == v, for v = 1..maxabs (chunked)."""
    firstk = np.full(maxabs + 1, -1, dtype=np.int64)
    CH = 10**6
    for start in range(0, len(absM), CH):
        chunk = absM[start:start + CH]
        vals = np.unique(chunk)
        new = vals[firstk[vals] == -1]
        for v in new:
            firstk[v] = start + int(np.nonzero(chunk == v)[0][0])
        if (firstk[1:] > 0).all():
            break
    return firstk


def main():
    mu = mu_sieve(N)
    M = np.cumsum(mu, dtype=np.int32)
    ok = True

    c1 = int(M[10]) == -1
    print(f"C1 M(10) = {int(M[10])} (expect -1): {'PASS' if c1 else 'FAIL'}")
    ok &= c1

    ref = {}
    with open(f"{EV}/b002321.txt") as f:
        for line in f:
            if line.startswith("#") or not line.split():
                continue
            n, v = line.split()
            ref[int(n)] = int(v)
    bad = [n for n in ref if int(M[n]) != ref[n]]
    c2 = not bad
    print(f"C2 OEIS A002321 n<=10000: {len(ref)} values, mismatches={len(bad)}"
          f"{' first=' + str(bad[:5]) if bad else ''}: {'PASS' if c2 else 'FAIL'}")
    ok &= c2

    from sympy import mobius
    lim3 = 10**5
    s = 0
    bad3 = []
    for n in range(1, lim3 + 1):
        s += mobius(n)
        if s != int(M[n]):
            bad3.append(n)
            if len(bad3) >= 5:
                break
    c3 = not bad3
    print(f"C3 sympy independent n<=10^5: mismatches={len(bad3)}"
          f"{' first=' + str(bad3) if bad3 else ''}: {'PASS' if c3 else 'FAIL'}")
    ok &= c3

    env = {}
    with open(f"{EV}/b051402.txt") as f:
        for line in f:
            if line.startswith("#") or not line.split():
                continue
            n, v = line.split()
            env[int(n)] = int(v)
    absM = np.abs(M)
    maxabs = int(absM.max())
    firstk = first_attainment(absM, maxabs)
    checked = 0
    bad4 = []
    for n in range(1, maxabs + 1):
        if n in env:
            checked += 1
            if firstk[n] != env[n]:
                bad4.append(n)
                if len(bad4) >= 5:
                    break
    c4 = not bad4
    print(f"C4 OEIS A051402 envelope: checked={checked} n-values, "
          f"mismatches={len(bad4)}{' first=' + str(bad4) if bad4 else ''}: "
          f"{'PASS' if c4 else 'FAIL'}")
    ok &= c4

    i_max = int(np.nonzero(absM == maxabs)[0][0])
    print(f"max |M(x)| for x <= {N}: {maxabs}, first at x = {i_max}, "
          f"M = {int(M[i_max])}")
    idx = np.arange(N + 1, dtype=np.float64)
    ratio = absM.astype(np.float64) / np.sqrt(idx)
    ratio[0] = 0.0
    i_r = int(ratio.argmax())
    print(f"max |M(x)|/sqrt(x) for x <= {N}: {ratio[i_r]:.9f} at x = {i_r} "
          f"(M = {int(M[i_r])})")
    for k in range(1, 9):
        print(f"M(10^{k}) = {int(M[10**k])}")
    top = np.argpartition(-absM, 10)[:10]
    print("top-10 |M(x)| locations:")
    for i in sorted(top.tolist(), key=lambda i: (-int(absM[i]), i)):
        print(f"  x={i} M={int(M[i])}")
    print("VERDICT:", "ALL CHECKS PASS" if ok else "CHECK FAILURE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
