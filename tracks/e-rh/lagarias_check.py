#!/usr/bin/env python3
"""Track E bounded falsification: Lagarias Problem E (lagarias-2002, Theorem 1.1).

RH  <=>  for all n >= 1:  sigma(n) <= H_n + exp(H_n)*log(H_n),  equality only at n=1.
  sigma(n) = sum of positive divisors of n (exact integer, divisor sieve)
  H_n      = harmonic number = digamma(n+1) + euler (exact identity), 100 digits

Method (rigorous, explicit error bound): margin(n) = H_n + e^{H_n} log H_n - sigma(n)
evaluated at 100 digits for EVERY n in [1, N]. mpmath ops at 100 digits carry error
< 1e-95 each (a few ulp); ~4 ops per n keeps |err| < 1e-90. Verdict threshold:
margin <= 1e-80 counts as non-positive (conservative vs the error bound).
A single n >= 2 with margin <= 0 DISPROVES RH (witness).
Verdict is machine-yes/no: NO COUNTEREXAMPLE in [1,N]  vs  COUNTEREXAMPLE FOUND.
"""
import sys, time
import mpmath as mp

def sigma_sieve(N):
    sigma = [0]*(N+1)
    for d in range(1, N+1):
        for m in range(d, N+1, d):
            sigma[m] += d
    return sigma

def main(N):
    mp.mp.dps = 100
    g = mp.euler
    e = mp.e
    THRESH = mp.mpf('1e-80')
    t0 = time.time()
    sigma = sigma_sieve(N)
    print(f"sieve N={N}: {time.time()-t0:.1f}s", flush=True)
    counter = []
    minmargin, minn = None, None
    t1 = time.time()
    for n in range(1, N+1):
        Hn = mp.digamma(n+1) + g
        rhs = Hn + e**Hn * mp.log(Hn)
        m = rhs - sigma[n]
        if n >= 2:
            if minmargin is None or m < minmargin:
                minmargin, minn = m, n
            if m <= THRESH:
                counter.append((n, sigma[n], m))
        if n % 100000 == 0:
            print(f"  progress {n}/{N} ({time.time()-t1:.0f}s)", flush=True)
    print(f"scan N={N}: {time.time()-t1:.1f}s", flush=True)
    print(f"min margin (n>=2): {minmargin} at n={minn}", flush=True)
    if counter:
        for n, s, m in counter[:10]:
            print(f"COUNTEREXAMPLE n={n}: sigma={s} margin={m}", flush=True)
        print(f"VERDICT: COUNTEREXAMPLE FOUND (RH DISPROVEN) — {len(counter)} in [2,{N}]", flush=True)
    else:
        print(f"VERDICT: NO COUNTEREXAMPLE in [1,{N}] (all margins > 1e-80 at 100 digits)", flush=True)

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    main(N)
