#!/usr/bin/env python3
"""Track D second experiment: Robin-criterion near-misses over colossally abundant numbers.

Robin's criterion (Lagarias 2002, eq 1.2, quoted): RH <=> sigma(n) < e^gamma * n * log log n
for all n >= 5041. Reduction (Lagarias 2002, p.334-336): if RH is false, some counterexample
to (1.2) is a colossally abundant (CA) number. So scanning CA numbers suffices to find a
Robin witness.

This script:
  - computes sigma(n) for all n <= N by exact-integer sieve;
  - generates CA numbers independently via Lagarias eq (2.3) eps-sweep;
  - runs pre-registered checks F1-F6 (logs/2026-08-22.tick.log, tick 112);
  - reports the Robin near-miss: max_{n>=5041} sigma(n)/(e^gamma*n*log log n) and where.
Exit 0 iff F1-F5 pass and no F6 witness hit.
"""
import math
import sys
import numpy as np

N = 10**6
EV = "evidence/2026-08-22-robin-ca"
EULER_GAMMA = 0.57721566490153286060651209008240243104215933593992
EG = math.exp(EULER_GAMMA)          # e^gamma
ROBIN_C = 0.6482                    # Robin explicit bound (2.2) constant
THRESH = 5041                       # Robin criterion threshold (eq 1.2)


def sieve_sigma(n):
    """sigma[k] = sum of divisors of k, exact int64, for k <= n."""
    sigma = np.zeros(n + 1, dtype=np.int64)
    for i in range(1, n + 1):
        sigma[i::i] += i
    return sigma


def primes_upto(n):
    is_p = np.ones(n + 1, dtype=bool)
    is_p[0] = is_p[1] = False
    for i in range(2, math.isqrt(n) + 1):
        if is_p[i]:
            is_p[i * i::i] = False
    return np.nonzero(is_p)[0].tolist()


def ca_epsweep(n_max, primes, eps_grid):
    """CA numbers via Lagarias eq (2.3): a_p(eps)=floor((log(p^{1+eps}-1)-log(p^eps-1))/log p)-1."""
    cas = set()
    for eps in eps_grid:
        num = 1
        for p in primes:
            logp = math.log(p)
            # log(expm1((1+eps)*logp)) - log(expm1(eps*logp))  ==  log(p^{1+eps}-1) - log(p^eps-1)
            a = math.floor((math.log(math.expm1((1 + eps) * logp))
                            - math.log(math.expm1(eps * logp))) / logp) - 1
            if a < 0:
                break
            num *= p ** a
            if num > n_max:
                break
        cas.add(num)
    return sorted(cas)


def main():
    sigma = sieve_sigma(N)
    ok = True

    # ---- F5: hand values -------------------------------------------------
    f5 = (int(sigma[12]) == 28) and (int(sigma[5040]) == 19344)
    print(f"F5 hand sigma(12)={int(sigma[12])} (exp 28), sigma(5040)={int(sigma[5040])} "
          f"(exp 19344): {'PASS' if f5 else 'FAIL'}")
    ok &= f5

    # ---- F3: sigma vs OEIS A000203 (n <= 10000) --------------------------
    ref = {}
    with open(f"{EV}/b000203.txt") as f:
        for line in f:
            if line.startswith("#") or not line.split():
                continue
            n, v = line.split()
            n = int(n)
            if n <= 10000:
                ref[n] = int(v)
    bad3 = [n for n in ref if int(sigma[n]) != ref[n]]
    f3 = not bad3
    print(f"F3 OEIS A000203 n<=10000: {len(ref)} values, mismatches={len(bad3)}"
          f"{' first=' + str(bad3[:5]) if bad3 else ''}: {'PASS' if f3 else 'FAIL'}")
    ok &= f3

    # ---- F4: Robin explicit bound (2.2), unconditional -------------------
    idx = np.arange(3, N + 1, dtype=np.float64)
    ll = np.log(np.log(idx))
    rhs = EG * idx * ll + ROBIN_C * idx / ll
    s = sigma[3:N + 1].astype(np.float64)
    viol4 = np.nonzero(s >= rhs)[0]
    f4 = len(viol4) == 0
    print(f"F4 Robin bound (2.2) n in [3,10^6]: violations={len(viol4)}"
          f"{' first_n=' + str(int(idx[viol4[0]])) if len(viol4) else ''}: "
          f"{'PASS' if f4 else 'FAIL'}")
    ok &= f4

    # ---- F1: CA list (eps-sweep) vs OEIS A004394 (n <= 10^6) -------------
    ca_oeis = []
    with open(f"{EV}/b004394.txt") as f:
        for line in f:
            if line.startswith("#") or not line.split():
                continue
            n = int(line.split()[0])
            if n <= N:
                ca_oeis.append(n)
            elif n > N:
                break
    primes = primes_upto(N)
    eps_grid = np.linspace(0.0005, 3.0, 40001)
    ca_gen = ca_epsweep(N, primes, eps_grid)
    f1 = ca_gen == ca_oeis
    print(f"F1 CA list <=10^6: OEIS={len(ca_oeis)}, eps-sweep={len(ca_gen)}, "
          f"equal={f1}"
          f"{' missing=' + str(set(ca_oeis) - set(ca_gen)) if not f1 else ''}"
          f"{' extra=' + str(set(ca_gen) - set(ca_oeis)) if not f1 else ''}: "
          f"{'PASS' if f1 else 'FAIL'}")
    ok &= f1
    ca_set = set(ca_oeis)

    # ---- Robin near-miss over n >= 5041 ----------------------------------
    m = np.arange(THRESH, N + 1, dtype=np.float64)
    llm = np.log(np.log(m))
    R = sigma[THRESH:N + 1].astype(np.float64) / (EG * m * llm)
    i_max = int(np.argmax(R))
    n_max = int(m[i_max])
    R_max = float(R[i_max])
    is_ca = n_max in ca_set
    print(f"near-miss: max R(n)=sigma/(e^gamma*n*loglog n) over n in [5041,10^6] "
          f"= {R_max:.12f} at n = {n_max} (CA={is_ca})")
    print(f"  ratio to bound e^gamma: sigma(n)/(n loglog n) = {R_max * EG:.12f} "
          f"vs e^gamma = {EG:.12f}  (fraction = {R_max:.6f})")

    # ---- F2: reduction check (argmax is a CA number) ---------------------
    # also report the best NON-CA value to show the gap is robust
    nonca_mask = np.array([int(x) not in ca_set for x in m])
    R_nonca = np.where(nonca_mask, R, -1.0)
    i_nc = int(np.argmax(R_nonca))
    n_nc = int(m[i_nc])
    R_nc = float(R_nonca[i_nc])
    f2 = is_ca
    print(f"F2 reduction check: argmax n={n_max} is CA={is_ca}; best non-CA R = {R_nc:.12f} "
          f"at n={n_nc}; gap = {R_max - R_nc:.3e}: {'PASS' if f2 else 'FAIL'}")
    ok &= f2

    # ---- F6: witness (R(n) >= 1 for any n >= 5041) -----------------------
    hit = np.nonzero(R >= 1.0)[0]
    f6 = len(hit) == 0
    print(f"F6 witness R(n)>=1 for n>=5041: hits={len(hit)}"
          f"{' first_n=' + str(int(m[hit[0]])) if len(hit) else ''}: "
          f"{'PASS (no RH witness <=10^6)' if f6 else 'HIT => RH WITNESS, STOP'}")
    ok &= f6

    # ---- top-10 R(n) locations -------------------------------------------
    top = np.argpartition(-R, 10)[:10]
    print("top-10 R(n) locations (n>=5041):")
    for i in sorted(top.tolist(), key=lambda i: (-float(R[i]), int(m[i]))):
        print(f"  n={int(m[i])} R={float(R[i]):.9f} CA={int(m[i]) in ca_set}")

    print("VERDICT:", "ALL CHECKS PASS" if ok else "CHECK FAILURE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
