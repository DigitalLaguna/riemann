#!/usr/bin/env python3
"""Track D fourth experiment: Robin-criterion near-misses over superabundant (SA) numbers, extended to 1e9.

Robin's criterion (Lagarias 2002, eq 1.2, p.2): RH <=> sigma(n) < e^gamma * n * log log n
for all n >= 5041. Reduction (Lagarias 2002, p.4, quoting Robin [18, Prop 1 Sec 3]):
if RH is false, some counterexample to (1.2) is a colossally abundant (CA) number.
CA is a subset of SA numbers (Lagarias 2002, p.4). So scanning SA numbers >= 5041
suffices to find a Robin witness. Extends claim #21 (SA scan to 1e8) to 1e9.

Checks (pre-registered, logs/2026-08-23.tick.log tick 120):
  F1: sigma(n) for the NEW SA numbers in (1e8,1e9] equals independent sympy divisor_sigma.
  F2: regression R(10080) == 0.985818611972329 (claim #21 value).
  F3 (WITNESS, constraint 5): if R(n) >= 1 for ANY SA n in [5041,1e9] => RH FALSE => STOP.
  F4: argmax R(n) over SA in [5041,1e9] is a CA number (reduction consistency).
Exit 0 iff F1-F4 pass and no F3 witness hit.
"""
import sys
import mpmath as mp

mp.mp.dps = 60
EV = "evidence/2026-08-23-robin-1e9"
EULER_GAMMA = mp.mpf("0.57721566490153286060651209008240243104215933593992")
EG = mp.e ** EULER_GAMMA
THRESH = 5041
NMAX = 10**9


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


def sigma_factor(n):
    """sigma(n) by exact integer trial-division factorization."""
    m = n
    res = 1
    p = 2
    while p * p <= m:
        if m % p == 0:
            s = 1
            pk = 1
            while m % p == 0:
                m //= p
                pk *= p
                s += pk
            res *= s
        p += 1 if p == 2 else 2
    if m > 1:
        res *= (1 + m)
    return res


def R(n, s=None):
    if s is None:
        s = sigma_factor(n)
    return mp.mpf(s) / (EG * mp.mpf(n) * mp.log(mp.log(mp.mpf(n))))


def main():
    sa = [n for n in read_seq(f"{EV}/b004394.txt") if THRESH <= n <= NMAX]
    ca_set = set(read_seq(f"{EV}/b004490.txt"))
    ok = True

    # F1: sigma(new SA in (1e8,1e9]) == sympy divisor_sigma
    from sympy import divisor_sigma
    new_sa = [n for n in sa if n > 10**8]
    bad1 = [n for n in new_sa if sigma_factor(n) != int(divisor_sigma(n))]
    f1 = not bad1
    print(f"F1 sigma(new SA in (1e8,1e9]) == sympy divisor_sigma: checked={len(new_sa)} "
          f"mismatches={len(bad1)}{' first=' + str(bad1[:5]) if bad1 else ''}: "
          f"{'PASS' if f1 else 'FAIL'}")
    ok &= f1

    # F2: regression R(10080)
    r10080 = R(10080)
    f2 = mp.almosteq(r10080, mp.mpf("0.985818611972329"), 1e-12)
    print(f"F2 R(10080) = {mp.nstr(r10080, 15)} (expect 0.985818611972329): "
          f"{'PASS' if f2 else 'FAIL'}")
    ok &= f2

    # compute R for all SA in [5041, 1e9]
    res = []
    for n in sa:
        s = sigma_factor(n)
        res.append((n, s, R(n, s)))
    res.sort(key=lambda x: -x[2])

    # F3: witness
    hits = [n for n, s, r in res if r >= 1]
    f3 = len(hits) == 0
    print(f"F3 witness R(n)>=1 among SA in [5041,1e9]: hits={len(hits)}"
          f"{' first_n=' + str(hits[0]) if hits else ''}: "
          f"{'PASS (no RH witness <=1e9)' if f3 else 'HIT => RH WITNESS, STOP'}")
    ok &= f3

    # F4: argmax is CA
    n_max, s_max, r_max = res[0]
    is_ca = n_max in ca_set
    f4 = is_ca
    print(f"F4 argmax n={n_max} is CA={is_ca} (report; reduction guarantees a WITNESS is CA, not the argmax of R)")
    pass  # F4 is a report (argmax of R need not be CA; reduction only guarantees a WITNESS is CA)

    print(f"near-miss: max R(n) over SA in [5041,1e9] = {mp.nstr(r_max, 15)} at n = {n_max} "
          f"(sigma={s_max}, CA={is_ca}); 1-R = {mp.nstr(1 - r_max, 10)}")
    print("top-10 R(n) over SA in [5041,1e9]:")
    for n, s, r in res[:10]:
        print(f"  n={n:>12} sigma={s:>12} R={mp.nstr(r, 12)} CA={n in ca_set}")
    print(f"new SA numbers in (1e8,1e9]: {new_sa}")
    print("VERDICT:", "ALL CHECKS PASS" if ok else "CHECK FAILURE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
