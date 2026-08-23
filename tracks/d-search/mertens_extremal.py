#!/usr/bin/env python3
"""Track D experiment: Mertens function M(x) = sum_{n<=x} mu(n).

N = 10^8 (default) or int(argv[1]). Exact integer arithmetic: mu as numpy
int8, M as int32 prefix sums. Cross-checks (pre-registered falsification
tests, see logs/2026-08-22.tick.log and logs/2026-08-23.tick.log):
  C1: M(10) == -1 (hand-computed from mu(1..10)).
  C2: M(n) == OEIS A002321 b-file for all n <= 10000.
  C3: M(n) == independent sympy trial-division M(n) for all n <= 10^5.
  C4: first k with |M(k)| == n equals OEIS A051402 b-file a(n) for all n in
      the b-file with n <= max_{x<=N} |M(x)| (inverse-Mertens envelope;
      A051402: "smallest k such that |M(k)| = n").
  C5: large-prime batching sanity (mu_sieve): for primes p > N/2 the only
      multiple <= N is p itself, so mu[p] must go 1 -> -1 under the batched
      sign-flip. Direct check of the N=1e10 speed-up.
Outputs M(10^k) for k <= log10(N), the |M| record, the |M(x)|/sqrt(x)
record, top-10 |M(x)| locations. Exit 0 iff all checks pass.

Memory/speed notes (for N = 10^10): mu_sieve batches the sign-flip for primes
p > N/2 into one vectorized op (cuts the Python loop ~2x); `del mu` after the
prefix sum; first-attainment via np.bincount (bounded values); top-10 via a
chunked heap (avoids a full-size argpartition temporary). Peak ~80 GB (M+absM).
"""
import math
import sys
import heapq
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**8
EV = "evidence/2026-08-22-mertens"


def mu_sieve(n):
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = False
    primes = np.nonzero(is_prime)[0]
    del is_prime
    mu = np.ones(n + 1, dtype=np.int8)
    mu[0] = 0
    # primes <= n//2: slice mu[p::p] has >= 2 elements -> per-prime loop
    # primes >  n//2: slice mu[p::p] is just [mu[p]] -> one vectorized flip
    split = int(np.searchsorted(primes, n // 2 + 1))
    isqrt_n = math.isqrt(n)  # p*p overflows int64 for p>3.03e9; use isqrt guard
    for p in primes[:split]:
        mu[p::p] *= -1
        if p <= isqrt_n:
            mu[p * p::p * p] = 0
    if split < len(primes):
        large = primes[split:]
        # C5 sanity: large primes start at mu=1 (no smaller factor touches them)
        if not bool((mu[large] == 1).all()):
            print("C5 large-prime pre-flip mu==1: FAIL")
            sys.exit(1)
        mu[large] *= -1
        if not bool((mu[large] == -1).all()):
            print("C5 large-prime post-flip mu==-1: FAIL")
            sys.exit(1)
        print(f"C5 large-prime batching: {len(large)} primes p>{n//2} flipped 1->-1: PASS")
    else:
        print("C5 large-prime batching: n/a (no primes > n//2): PASS")
    return mu


def first_attainment(absM, maxabs):
    """firstk[v] = smallest i with absM[i] == v, for v = 1..maxabs (chunked,
    bincount-based since values are bounded by maxabs)."""
    firstk = np.full(maxabs + 1, -1, dtype=np.int64)
    CH = 10**7
    for start in range(0, len(absM), CH):
        chunk = absM[start:start + CH]
        hist = np.bincount(chunk, minlength=maxabs + 1)
        present = np.nonzero(hist)[0]
        new = present[firstk[present] == -1]
        for v in new:
            firstk[v] = start + int(np.nonzero(chunk == v)[0][0])
        if (firstk[1:] > 0).all():
            break
    return firstk


def top_k_locations(absM, k=10, CH=10**7):
    """top-k (absval, x) by absval desc, x asc; chunked to avoid a full-size
    argpartition temporary. The record itself uses the first-attainment scan."""
    heap = []
    for start in range(0, len(absM), CH):
        stop = min(start + CH, len(absM))
        chunk = absM[start:stop]
        if len(chunk) <= k:
            idx = np.argsort(chunk)[::-1][:k]
        else:
            idx = np.argpartition(chunk, -k)[-k:]
        for j in idx.tolist():
            x = start + int(j)
            av = int(chunk[j])
            if len(heap) < k:
                heapq.heappush(heap, (av, x))
            elif av > heap[0][0]:
                heapq.heapreplace(heap, (av, x))
    return sorted(heap, key=lambda t: (-t[0], t[1]))


def main():
    mu = mu_sieve(N)
    M = np.cumsum(mu, dtype=np.int32)
    del mu
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
    CH = 10**7
    best_r, i_r = 0.0, 1
    for start in range(1, N + 1, CH):
        stop = min(start + CH, N + 1)
        r = absM[start:stop].astype(np.float64) / np.sqrt(
            np.arange(start, stop, dtype=np.float64))
        j = int(r.argmax())
        if r[j] > best_r:
            best_r, i_r = float(r[j]), start + j
    print(f"max |M(x)|/sqrt(x) for x <= {N}: {best_r:.9f} at x = {i_r} "
          f"(M = {int(M[i_r])})")
    kmax = int(round(math.log10(N)))
    for k in range(1, kmax + 1):
        print(f"M(10^{k}) = {int(M[10**k])}")
    print("top-10 |M(x)| locations:")
    for av, x in top_k_locations(absM, k=10):
        print(f"  x={x} M={int(M[x])}")
    print("VERDICT:", "ALL CHECKS PASS" if ok else "CHECK FAILURE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
