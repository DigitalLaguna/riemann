#!/usr/bin/env python3
"""Track E (tick 177/179): Lagarias inequality on superabundant numbers (macarevey-2026).

Paper: B_n = (H_n + e^{H_n} log H_n)/n strictly increasing (Cor 2.1) => if the
Lagarias inequality has counterexamples, the least one is superabundant (Thm 3.1).
So verifying the inequality on SA numbers <= 1e10 extends claim #10 (all n <= 1e6).

This script runs the pre-registered tests F3 (witness, constraint 5) and F4
(sigma cross-check) from logs/2026-08-24.tick.log TICK 177:

F3: margin(n) = H_n + e^{H_n} log H_n - sigma(n) at 100 digits for ALL b-file
    SA n <= 1e10; margin(n) <= 1e-80 for any n >= 2 => RH FALSE => STOP,
    write disproof_candidate.md, page owner. (Same 100-digit method + 1e-80
    threshold as claim #10, tracks/e-rh/lagarias_check.py.)
F4: sigma(n) for the SA n <= 1e10: sympy.divisor_sigma == independent
    trial-division factorization (exact). DEAD on any mismatch.

Input: evidence/2026-08-24-lagarias-sa/a004394.txt (OEIS A004394 b-file,
fetched tick 178; plain-integer entries, "index value" lines).
SCOPE NOTE: F3/F4 are conditional on b-file completeness (F2/F2b, pending) and
on Cor 2.1 (F1a/F1b, pending). The claim this produces is scoped to "the 55
b-file SA entries <= 1e10".
"""
import sys, time
import mpmath as mp
from sympy import divisor_sigma

BFILE = "evidence/2026-08-24-lagarias-sa/a004394.txt"
BOUND = 10**10
THRESH = mp.mpf('1e-80')

def parse_bfile(path, bound):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            idx, val = line.split()
            if not val.isdigit():
                continue
            v = int(val)
            if v <= bound:
                out.append(v)
    return out

def sigma_trial(n):
    """Exact sigma(n) by trial division (independent of sympy)."""
    m, res, p, d = n, 1, n, 2
    while d * d <= p:
        if p % d == 0:
            sp, k = 1, 1
            while p % d == 0:
                p //= d
                k *= d
                sp += k
            res *= sp
        d += 1 if d == 2 else 2
    if p > 1:
        res *= (1 + p)
    assert res > 0
    return res

def main():
    t0 = time.time()
    sa = parse_bfile(BFILE, BOUND)
    assert sa[0] == 1, f"b-file first entry {sa[0]} != 1"
    assert all(a < b for a, b in zip(sa, sa[1:])), "b-file not strictly increasing"
    print(f"b-file SA entries <= {BOUND}: {len(sa)}; first={sa[0]} last={sa[-1]}")
    print(f"last 5: {sa[-5:]}")

    # F4: sigma cross-check (exact)
    sig = {}
    mism = []
    for n in sa:
        s1 = sigma_trial(n)
        s2 = int(divisor_sigma(n))
        sig[n] = s1
        if s1 != s2:
            mism.append((n, s1, s2))
    print(f"F4: sigma cross-check (trial division vs sympy) {len(sa)}/{len(sa)}; "
          f"mismatches: {len(mism)}")
    for n, a, b in mism[:5]:
        print(f"  MISMATCH n={n}: trial={a} sympy={b}")
    f4 = "PASS" if not mism else "DEAD"

    # F3: 100-digit margins (witness test)
    mp.mp.dps = 100
    g, e = mp.euler, mp.e
    counter, minmargin, minn = [], None, None
    for n in sa:
        Hn = mp.digamma(n + 1) + g
        m = Hn + e**Hn * mp.log(Hn) - sig[n]
        if n >= 2:
            if minmargin is None or m < minmargin:
                minmargin, minn = m, n
            if m <= THRESH:
                counter.append((n, sig[n], m))
    # extra safety: re-evaluate the argmin margin at 150 dps
    mp.mp.dps = 150
    Hn = mp.digamma(minn + 1) + mp.euler
    m150 = Hn + mp.e**Hn * mp.log(Hn) - sig[minn]
    print(f"F3: min margin (n>=2): {minmargin} at n={minn}")
    print(f"F3: argmin margin re-evaluated at 150 dps: {m150}")
    if counter:
        for n, s, m in counter[:10]:
            print(f"WITNESS n={n}: sigma={s} margin={m}")
        print(f"VERDICT F3: WITNESS FOUND (RH DISPROVEN) — {len(counter)} in SA <= {BOUND}")
    else:
        print(f"VERDICT F3: NO WITNESS among {len(sa)} SA n <= {BOUND} "
              f"(all margins > 1e-80 at 100 digits)")
    print(f"VERDICT F4: {f4}")
    print(f"total {time.time()-t0:.1f}s")

if __name__ == '__main__':
    main()
