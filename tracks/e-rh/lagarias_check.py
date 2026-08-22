#!/usr/bin/env python3
"""Track E bounded falsification: Lagarias Problem E (lagarias-2002, Theorem 1.1).

RH  <=>  for all n >= 1:  sigma(n) <= H_n + exp(H_n)*log(H_n),  equality only at n=1.
  sigma(n) = sum of positive divisors of n (exact integer)
  H_n      = sum_{j=1}^n 1/j  (harmonic number)
A single n >= 2 with sigma(n) > H_n + exp(H_n)*log(H_n) DISPROVES RH (witness).

Method: exact-integer sigma via divisor sieve; float bulk scan for the margin
  margin(n) = H_n + exp(H_n)*log(H_n) - sigma(n);
then re-verify every near-miss (and any float-negative) at 100 mpmath digits.
Verdict is machine-yes/no: NO COUNTEREXAMPLE in [1,N]  vs  COUNTEREXAMPLE FOUND.
"""
import sys, time, math
import mpmath as mp

GAMMA = 0.577215664901532860606512090082402431

def sigma_sieve(N):
    sigma = [0]*(N+1)
    for d in range(1, N+1):
        for m in range(d, N+1, d):
            sigma[m] += d
    return sigma

def Hn_float(n):
    if n < 100:
        return sum(1.0/j for j in range(1, n+1))
    x = float(n)
    return math.log(x) + GAMMA + 1.0/(2*x) - 1.0/(12*x*x) + 1.0/(120*x**4)

def main(N, recheck=200):
    t0 = time.time()
    sigma = sigma_sieve(N)
    t1 = time.time()
    print(f"sieve N={N}: {t1-t0:.1f}s", flush=True)
    worst = (float('inf'), 1)
    ncounter = 0
    near = []
    top10 = []  # 10 smallest margins, n>=2
    for n in range(1, N+1):
        Hn = Hn_float(n)
        rhs = Hn + math.exp(Hn)*math.log(Hn)
        s = sigma[n]
        margin = rhs - s
        if n >= 2 and margin < 0:
            ncounter += 1
            print(f"FLOAT COUNTEREXAMPLE n={n}: sigma={s} rhs={rhs}", flush=True)
        if margin < 1e-3*max(1.0, float(s)):
            near.append((margin, n))
        if n >= 2 and margin < worst[0]:
            worst = (margin, n)
        if n >= 2:
            top10.append((margin, n))
            if len(top10) > 10:
                top10.pop()
    t2 = time.time()
    print(f"scan N={N}: {t2-t1:.1f}s", flush=True)
    print(f"float counterexamples: {ncounter}", flush=True)
    print(f"worst float margin: {worst[0]:.6g} at n={worst[1]}", flush=True)
    near.sort()
    print(f"near-misses flagged: {len(near)}; rechecking {min(len(near),recheck)} at 100 digits", flush=True)
    mp.mp.dps = 100
    g = mp.euler
    allpos = True
    minmargin = None
    for margin, n in near[:recheck]:
        Hn = mp.digamma(n+1) + g
        rhs = Hn + mp.e**Hn * mp.log(Hn)
        s = sigma[n]
        m = rhs - s
        if minmargin is None or m < minmargin:
            minmargin = m
        if n >= 2 and m <= 0:
            allpos = False
            print(f"  100-digit COUNTEREXAMPLE n={n}: sigma={s} rhs={rhs} margin={m}", flush=True)
    print(f"min 100-digit margin among rechecked: {minmargin}", flush=True)
    print(f"ALL RECHECKED MARGINS POSITIVE: {allpos}", flush=True)
    top10.sort()
    print('10 smallest margins (n>=2):', flush=True)
    for m_, n_ in top10:
        print(f'  n={n_}: margin={m_:.6g}', flush=True)
    ok = (ncounter == 0) and allpos
    print(f"VERDICT: {'NO COUNTEREXAMPLE in [1,%d] (RH survives bounded)' % N if ok else 'COUNTEREXAMPLE FOUND (RH DISPROVEN)'}", flush=True)

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    main(N)
