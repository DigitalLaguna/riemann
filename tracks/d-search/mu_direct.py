#!/usr/bin/env python3
"""Independent mu check at the Mertens 1e11 record location.

run3.txt (segmented exact-integer sieve, N=1e11) reports
  max |M(x)| for x <= 1e11: 94909, first at x = 99481473379, M = -94909
plus a top-10 |M(x)| list. Equal M values at two x's imply the sum of mu
over the interval between them is 0; a drop of 1 implies a sum of -1.
This script recomputes mu(n) for n in [99481473374, 99481473568] by
independent trial division (primes <= 316228 = sqrt(1e11)) and checks
every implication of the top-10 list.

Falsification (pre-registered, tick 136): any FAIL line means the record
location is suspect (x-indexing or mu bug at the record).
"""
import sys

def sieve_primes(limit):
    bs = bytearray([1]) * (limit + 1)
    bs[0] = bs[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if bs[i]:
            bs[i * i::i] = bytearray(len(bs[i * i::i]))
    return [i for i in range(limit + 1) if bs[i]]

PRIMES = sieve_primes(316228)

def mu(n):
    """Mobius by trial division over PRIMES. 0 if not squarefree."""
    m, k = n, 0
    for p in PRIMES:
        if p * p > m:
            break
        if m % p == 0:
            m //= p
            k += 1
            if m % p == 0:
                return 0
    if m > 1:
        k += 1
    return -1 if k & 1 else 1

LO, HI = 99481473374, 99481473568
mus = {n: mu(n) for n in range(LO, HI + 1)}

# M values verbatim from run3.txt top-10 list
M = {
    99481473379: -94909,
    99481473380: -94909,
    99481473419: -94909,
    99481473420: -94909,
    99481473374: -94908,
    99481473375: -94908,
    99481473376: -94908,
    99481473377: -94908,
    99481473402: -94908,
    99481473568: -94908,
}

def summu(a, b):
    """sum of mu(n) for a < n <= b"""
    return sum(mus[n] for n in range(a + 1, b + 1))

ok = True
def check(name, cond):
    global ok
    print(f"{name}: {'PASS' if cond else 'FAIL'}")
    ok = ok and cond

check("mu(99481473375)=0  [M(374)=M(375)=-94908]", mus[99481473375] == 0)
check("mu(99481473376)=0  [M(375)=M(376)=-94908]", mus[99481473376] == 0)
check("mu(99481473377)=0  [M(376)=M(377)=-94908]", mus[99481473377] == 0)
check("mu(99481473378)+mu(99481473379)=-1  [M(377)=-94908 -> M(379)=-94909]",
      mus[99481473378] + mus[99481473379] == -1)
check("mu(99481473380)=0  [M(379)=M(380)=-94909]", mus[99481473380] == 0)
check("sum mu(381..419)=0  [M(380)=M(419)=-94909]", summu(99481473380, 99481473419) == 0)
check("mu(99481473420)=0  [M(419)=M(420)=-94909]", mus[99481473420] == 0)
check("sum mu(375..402)=0  [M(374)=M(402)=-94908]", summu(99481473374, 99481473402) == 0)
check("sum mu(403..568)=0  [M(402)=M(568)=-94908]", summu(99481473402, 99481473568) == 0)

print("mu(99481473378) =", mus[99481473378])
print("mu(99481473379) =", mus[99481473379])
print("VERDICT:", "ALL PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
