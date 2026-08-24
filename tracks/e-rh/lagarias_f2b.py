#!/usr/bin/env python3
"""Track E (tick 180): F2b — no sigma(n)/n record-holder in (1e7, 1e10] gaps.

Pre-registered (logs/2026-08-24.tick.log TICK 177):
  F2b: no m in (a,b) [consecutive b-file entries, a >= 1e7, b <= 1e10] with
      sigma(m)/m > sigma(a)/a (exact Fraction; candidates filtered by
      prod_{p|m} p/(p-1) > T0 = sigma(a)/a via DFS over prime products).
      DEAD if any such m (b-file incomplete in (1e7,1e10] -> claim scoped to
      1e7, F2b recorded as the wall).

Method:
  For each gap (a,b): T0 = sigma(a)/a (exact Fraction). A candidate m in (a,b)
  with sigma(m)/m > T0 must satisfy prod_{p|m} p/(p-1) > T0 (necessary, since
  sigma(m)/m = prod_{p^k||m}(1-p^{-(k+1)})/(1-1/p) < prod_{p|m} p/(p-1)).
  COMPLETENESS BOUND: let q = largest prime factor of a candidate m, m = R q^k,
  R q-smooth, R < b/q. Then prod_{p|R} p/(p-1) > T0 (q-1)/q. If q > Q = 1e5,
  then R < b/Q and max_{R < b/Q} prod_{p|R} p/(p-1) < T0 (q-1)/q for every
  gap (verified below per gap, with (q-1)/q replaced by its minimum
  (QMIN-1)/QMIN over primes q > Q, QMIN = nextprime(Q) = 100003),
  contradiction. Hence q <= Q and the DFS over primes <= Q is complete.
  DFS enumerates every Q-smooth m in (a,b) exactly once (increasing-prime
  order), tracks prod_{p|m} p/(p-1) as a float for pruning, and for each m with
  float prod > T0 checks sigma(m)/m > T0 exactly (Fraction).
"""
import sys, time
from fractions import Fraction
from sympy import divisor_sigma, primerange, nextprime

Q = 10**5
BFILE = "evidence/2026-08-24-lagarias-sa/a004394.txt"
PRIMES = list(primerange(2, Q + 1))
QMIN = nextprime(Q)  # smallest prime > Q (= 100003)
PF = [p / (p - 1) for p in PRIMES]   # float p/(p-1)

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

def sigma_frac(n):
    return Fraction(int(divisor_sigma(n)), n)

def max_prod_below(X):
    """max of prod_{p|R} p/(p-1) over R < X, via the same DFS (X small)."""
    best = [1.0]
    def dfs(m, prod, i):
        if prod > best[0]:
            best[0] = prod
        for j in range(i, len(PRIMES)):
            p = PRIMES[j]
            if m * p >= X:
                break
            np_ = prod * PF[j] if m % p else prod
            dfs(m * p, np_, j)
    dfs(1, 1.0, 0)
    return best[0]

def main():
    t0 = time.time()
    vals = parse_bfile(BFILE, 10**10)
    gaps = [(vals[i], vals[i+1]) for i in range(len(vals)-1)
            if vals[i] >= 10**7 and vals[i+1] <= 10**10]
    print(f"gaps in (1e7,1e10]: {len(gaps)}")
    nodes = [0]
    found = []

    def dfs(m, prod, i, a, b, T0f, T0):
        nodes[0] += 1
        if m > a and prod > T0f - 1e-12:
            if sigma_frac(m) > T0:
                found.append((a, b, m))
        for j in range(i, len(PRIMES)):
            p = PRIMES[j]
            mp = m * p
            if mp >= b:
                break
            dfs(mp, prod * PF[j] if m % p else prod, j, a, b, T0f, T0)

    for (a, b) in gaps:
        T0 = sigma_frac(a)
        T0f = float(T0)
        # completeness check: a candidate with largest prime factor q > Q
        # needs prod_{p|R} p/(p-1) > T0*(q-1)/q >= T0*(QMIN-1)/QMIN with R < b/Q
        mpb = max_prod_below(b // Q + 1)
        need = T0f * (QMIN - 1) / QMIN
        assert mpb < need, f"completeness bound fails for gap ({a},{b}): {mpb} >= {need}"
        n0 = nodes[0]
        dfs(1, 1.0, 0, a, b, T0f, T0)
        dn = nodes[0] - n0
        print(f"gap ({a},{b}) width={b-a} T0={T0f:.6f}: DFS nodes={dn}, "
              f"candidates checked, max_prod_below(b/Q)={mpb:.6f}")
        if found:
            break
    if found:
        for (a, b, m) in found:
            print(f"WITNESS m={m} in ({a},{b}): sigma(m)/m > sigma(a)/a")
        print(f"VERDICT F2b: DEAD")
    else:
        print(f"VERDICT F2b: PASS (no record-holder in any of the {len(gaps)} gaps)")
    print(f"total {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
