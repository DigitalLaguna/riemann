#!/usr/bin/env python3
"""Track D experiment 7: Mertens M(x) = sum_{n<=x} mu(n), N up to 1e12.

Segmented mu sieve: memory O(SEG) instead of O(N). The full-array
mertens_extremal.py needs ~8 TB at N=1e12 (M int32 + absM int32 + mu int8);
the machine has 125 GB.

mu per segment [a,b): start at 1; for each prime p <= sqrt(N): flip sign at
multiples of p, multiply small-radical s(n) by p at multiples of p, zero mu at
multiples of p^2. Then r = n/s(n): since n <= N, n has at most ONE prime
factor > sqrt(N), so r > 1 iff n has such a factor, in which case flip the
sign once. Exact integer arithmetic (int8 mu, int64 s/M).

Checks (pre-registered F1-F5: logs/2026-08-23.tick.log, tick 131):
  C1: M(10) == -1.
  C2: M(n) == OEIS A002321 b-file for n <= 10000.
  C3: M(n) == independent sympy trial-division M(n) for n <= 1e5.
  C4: first k with |M(k)| == n equals OEIS A051402 b-file a(n) for all n in
      the b-file (n <= 10000) with n <= max_{x<=N} |M(x)|.
  C5: segmented mu for [0,1e6] == full-array mu_sieve(1e6) exactly
      (cross-check against the verified full-array code).
  C6: M(10^kmax) == M10K[kmax] (kmax = round(log10 N); OEIS A084237,
      fetched 2026-08-23) [N >= 1e11].
  C7: M(10^k) k=1..kmax-1 == machine-verified run values / OEIS
      [N >= 1e10].
  W:  witness line: max |M(x)|/sqrt(x) for x >= 100; >= 1.0 at x <= N would
      falsify the Mertens conjecture |M(x)| < sqrt(x) at that x.
Exit 0 iff all checks pass.
"""
import math
import sys
import heapq
import numpy as np

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10**11
SEG = int(sys.argv[2]) if len(sys.argv) > 2 else 10**8
EV = "evidence/2026-08-22-mertens"
CH = 10**7

# M(10^k): k<=10 from the machine-verified full-array runs (claims #20/#22/#24,
# evidence/2026-08-23-mertens-1e10/run.txt); k=11 from OEIS A084237 (fetched
# 2026-08-23, see logs/2026-08-23.tick.log tick 131 prior-art pre-flight);
# k=11 confirmed by the machine-verified 1e11 run (claim #27,
# evidence/2026-08-23-mertens-1e11/promote-run.txt); k=12 = 62366 from
# OEIS A084237 a(12) (Weisstein 2003 term; file fetched 2026-08-23,
# evidence/2026-08-23-mertens-1e9/oeis-a084237-m10n.txt).
M10K = {1: -1, 2: 1, 3: 2, 4: -23, 5: -48, 6: 212, 7: 1037,
        8: 1928, 9: -222, 10: -33722, 11: -87856, 12: 62366}


def full_mu(n):
    """full-array mu (same logic as mertens_extremal.mu_sieve, no C5 print)."""
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = False
    primes = np.nonzero(is_prime)[0]
    del is_prime
    mu = np.ones(n + 1, dtype=np.int8)
    mu[0] = 0
    for p in primes:
        mu[p::p] *= -1
        if p * p <= n:
            mu[p * p::p * p] = 0
    return mu


def main():
    L = math.isqrt(N)
    is_prime = np.ones(L + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    for i in range(2, math.isqrt(L) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = False
    primes = np.nonzero(is_prime)[0]
    del is_prime

    ok = True
    M_offset = 0            # M(a-1) at segment start a
    maxabs = 0
    first_x = -1
    M_at_first = 0
    firstk = np.full(10001, -1, dtype=np.int64)  # first x with |M(x)|==v, v<=10000
    heap = []               # top-10 (absval, x, signed M)
    M10 = {}
    best_r, i_r, M_r = 0.0, 1, 1
    best_r100, i_r100, M_r100 = 0.0, -1, 0

    for a in range(0, N + 1, SEG):
        b = min(a + SEG, N + 1)
        seg = b - a
        mu = np.ones(seg, dtype=np.int8)
        s = np.ones(seg, dtype=np.int64)
        if a == 0:
            mu[0] = 0
        for p in primes:
            p = int(p)
            start = ((a + p - 1) // p) * p
            if start < b:
                mu[start - a::p] *= -1
                s[start - a::p] *= p
            p2 = p * p
            if p2 < b:
                start2 = ((a + p2 - 1) // p2) * p2
                if start2 < b:
                    mu[start2 - a::p2] = 0
        xs = np.arange(a, b, dtype=np.int64)
        has_large = xs // s > 1
        if has_large.any():
            mu[has_large] *= -1
        del s

        if a == 0:
            c5 = bool((mu[:10**6 + 1] == full_mu(10**6)[:10**6 + 1]).all())
            print(f"C5 segmented mu == full-array mu n<=10^6: "
                  f"{'PASS' if c5 else 'FAIL'}")
            ok &= c5
        Mval = np.cumsum(mu, dtype=np.int64) + M_offset
        del mu
        absM = np.abs(Mval)

        if a == 0:
            c1 = int(Mval[10]) == -1
            print(f"C1 M(10) = {int(Mval[10])} (expect -1): "
                  f"{'PASS' if c1 else 'FAIL'}")
            ok &= c1

            ref = {}
            with open(f"{EV}/b002321.txt") as f:
                for line in f:
                    if line.startswith("#") or not line.split():
                        continue
                    n, v = line.split()
                    ref[int(n)] = int(v)
            bad = [n for n in ref if int(Mval[n]) != ref[n]]
            c2 = not bad
            print(f"C2 OEIS A002321 n<=10000: {len(ref)} values, "
                  f"mismatches={len(bad)}"
                  f"{' first=' + str(bad[:5]) if bad else ''}: "
                  f"{'PASS' if c2 else 'FAIL'}")
            ok &= c2

            from sympy import mobius
            lim3 = 10**5
            sm = 0
            bad3 = []
            for n in range(1, lim3 + 1):
                sm += mobius(n)
                if sm != int(Mval[n]):
                    bad3.append(n)
                    if len(bad3) >= 5:
                        break
            c3 = not bad3
            print(f"C3 sympy independent n<=10^5: mismatches={len(bad3)}"
                  f"{' first=' + str(bad3) if bad3 else ''}: "
                  f"{'PASS' if c3 else 'FAIL'}")
            ok &= c3

        for k in range(1, int(round(math.log10(N))) + 1):
            xk = 10**k
            if a <= xk < b:
                M10[k] = int(Mval[xk - a])

        seg_max = int(absM.max())
        if seg_max > maxabs:
            maxabs = seg_max
            idx = int(np.nonzero(absM == seg_max)[0][0])
            first_x = a + idx
            M_at_first = int(Mval[idx])

        if not (firstk[1:] > 0).all():
            for start in range(0, seg, CH):
                stop = min(start + CH, seg)
                chunk = absM[start:stop]
                hist = np.bincount(chunk, minlength=10001)
                present = np.nonzero(hist)[0]
                present = present[present <= 10000]
                new = present[firstk[present] == -1]
                for v in new:
                    firstk[v] = a + start + int(np.nonzero(chunk == v)[0][0])
                if (firstk[1:] > 0).all():
                    break

        for start in range(0, seg, CH):
            stop = min(start + CH, seg)
            if a + start == 0:
                start += 1
                stop = min(stop, seg)
                if start >= stop:
                    continue
            xsf = np.arange(a + start, a + stop, dtype=np.float64)
            r = absM[start:stop].astype(np.float64) / np.sqrt(xsf)
            j = int(r.argmax())
            xv = a + start + j
            mv = int(Mval[start + j])
            if r[j] > best_r:
                best_r, i_r, M_r = float(r[j]), xv, mv
            if xv >= 100 and r[j] > best_r100:
                best_r100, i_r100, M_r100 = float(r[j]), xv, mv

        for start in range(0, seg, CH):
            stop = min(start + CH, seg)
            chunk = absM[start:stop]
            cmax = int(chunk.max())
            if len(heap) >= 10 and cmax < heap[0][0]:
                continue
            if len(chunk) <= 10:
                idx = np.argsort(chunk)[::-1][:10]
            else:
                idx = np.argpartition(chunk, -10)[-10:]
            for j in idx.tolist():
                x = a + start + int(j)
                av = int(chunk[j])
                mv = int(Mval[start + int(j)])
                if len(heap) < 10:
                    heapq.heappush(heap, (av, x, mv))
                elif av > heap[0][0]:
                    heapq.heapreplace(heap, (av, x, mv))

        M_offset = int(Mval[-1])
        del Mval, absM
        segi = a // SEG
        if segi % 100 == 99:
            print(f"progress: {segi + 1}/{(N + SEG - 1) // SEG} segments, "
                  f"maxabs={maxabs}", file=sys.stderr, flush=True)

    env = {}
    with open(f"{EV}/b051402.txt") as f:
        for line in f:
            if line.startswith("#") or not line.split():
                continue
            n, v = line.split()
            env[int(n)] = int(v)
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

    kmax = int(round(math.log10(N)))
    if N >= 10**11:
        c6 = M10.get(kmax) == M10K[kmax]
        print(f"C6 M(10^{kmax}) = {M10.get(kmax)} (expect {M10K[kmax]}, "
              f"OEIS A084237): {'PASS' if c6 else 'FAIL'}")
        ok &= c6
    if N >= 10**10:
        bad7 = [k for k in range(1, kmax) if M10.get(k) != M10K[k]]
        c7 = not bad7
        print(f"C7 M(10^k) k<{kmax} vs verified runs/OEIS: "
              f"mismatches={len(bad7)}"
              f"{' first=' + str(bad7) if bad7 else ''}: "
              f"{'PASS' if c7 else 'FAIL'}")
        ok &= c7

    print(f"max |M(x)| for x <= {N}: {maxabs}, first at x = {first_x}, "
          f"M = {M_at_first}")
    print(f"max |M(x)|/sqrt(x) for x <= {N}: {best_r:.9f} at x = {i_r} "
          f"(M = {M_r})")
    for k in range(1, kmax + 1):
        print(f"M(10^{k}) = {M10[k]}")
    print("top-10 |M(x)| locations:")
    for av, x, mv in sorted(heap, key=lambda t: (-t[0], t[1])):
        print(f"  x={x} M={mv}")
    print(f"witness: max |M(x)|/sqrt(x) for x >= 100: {best_r100:.9f} "
          f"at x = {i_r100} (M = {M_r100})")
    print("VERDICT:", "ALL CHECKS PASS" if ok else "CHECK FAILURE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
