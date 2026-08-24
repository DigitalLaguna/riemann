#!/usr/bin/env python3
"""Track D: Robin-criterion near-misses over superabundant (SA) numbers in [1e9, 1e10].

Extends the SA scan of robin_sa_1e9.py (claim #23, [5041,1e9]) to [1e9,1e10].
Purpose: (1) witness check F3 (R(n)>=1 => RH false, constraint 5), (2) provide
the F3b regression reference (12-sig-digit display of the SA max R) for the
full scan robin_full_scan.py [1e9,1e10) launched the same tick.

Robin's criterion (Lagarias 2002, eq 1.2, p.2): RH <=> sigma(n) < e^gamma*n*log log n
for all n >= 5041. A counterexample, if any, is CA (hence SA), so the SA scan
finds a witness if one exists in the range.

SA list: OEIS A004394 b-file (evidence/2026-08-23-robin-1e9/b004394.txt),
plain 'n value' lines only (the file's compressed tail extends to 10^1200,
not needed here).

Checks (pre-registered, logs/2026-08-24.tick.log tick 167):
  F1: sigma(n) for the SA numbers in [1e9,1e10] == sympy divisor_sigma.
  F2: regression — the SA max in (1e8,1e9] reproduces claim #23's 12-sig-digit
      display 0.968152104902 at n=367567200 (guards the R() formula).
  F3 (WITNESS, constraint 5): R(n) >= 1 for ANY SA n in [1e9,1e10] => RH FALSE => STOP.
Exit 0 iff F1-F3 pass and no F3 witness hit.
"""
import sys
import mpmath as mp
from sympy import divisor_sigma

mp.mp.dps = 60
EULER_GAMMA = mp.mpf("0.57721566490153286060651209008240243104215933593992")
EG = mp.e ** EULER_GAMMA
A, B = 10**9, 10**10
BFILE = "evidence/2026-08-23-robin-1e9/b004394.txt"


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


def R(n, s):
    return mp.mpf(s) / (EG * mp.mpf(n) * mp.log(mp.log(mp.mpf(n))))


def main():
    sa = [n for n in read_seq(BFILE) if A <= n <= B]
    ok = True

    bad1 = [n for n in sa if sigma_factor(n) != int(divisor_sigma(n))]
    f1 = not bad1
    print(f"F1 sigma(SA in [1e9,1e10]) == sympy divisor_sigma: checked={len(sa)} "
          f"mismatches={len(bad1)}{' first=' + str(bad1[:5]) if bad1 else ''}: "
          f"{'PASS' if f1 else 'FAIL'}")
    ok &= f1

    sa_prev = [n for n in read_seq(BFILE) if 10**8 < n <= 10**9]
    prev = max(((n, sigma_factor(n), R(n, sigma_factor(n))) for n in sa_prev),
               key=lambda x: x[2])
    f2 = mp.nstr(prev[2], 12) == "0.968152104902" and prev[0] == 367567200
    print(f"F2 regression (1e8,1e9] SA max: n={prev[0]} display={mp.nstr(prev[2],12)} "
          f"(expect 0.968152104902 at 367567200): {'PASS' if f2 else 'FAIL'}")
    ok &= f2

    res = []
    for n in sa:
        s = sigma_factor(n)
        res.append((n, s, R(n, s)))
    res.sort(key=lambda x: -x[2])

    hits = [n for n, s, r in res if r >= 1]
    f3 = len(hits) == 0
    print(f"F3 witness R(n)>=1 among SA in [1e9,1e10]: hits={len(hits)}"
          f"{' first_n=' + str(hits[0]) if hits else ''}: "
          f"{'PASS (no RH witness in [1e9,1e10])' if f3 else 'HIT => RH WITNESS, STOP'}")
    ok &= f3

    n_max, s_max, r_max = res[0]
    print(f"SA near-miss [1e9,1e10]: max R = {mp.nstr(r_max, 16)} at n = {n_max} "
          f"(sigma={s_max}); 1-R = {mp.nstr(1 - r_max, 10)}")
    print(f"F3b reference for full scan: 12-sig-digit display = {mp.nstr(r_max, 12)}")
    print("all SA in [1e9,1e10]:")
    for n, s, r in res:
        print(f"  n={n:>12} sigma={s:>14} R={mp.nstr(r, 12)}")
    nxt = [n for n in read_seq(BFILE) if n > B]
    print(f"next SA after 1e10: {nxt[0] if nxt else 'n/a'}")
    print("VERDICT:", "ALL CHECKS PASS" if ok else "CHECK FAILURE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
