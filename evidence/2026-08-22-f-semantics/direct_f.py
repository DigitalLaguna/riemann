#!/usr/bin/env python3
"""Direct high-precision evaluation of f_t(x+iy) at Polymath15 Table 1 row 2.
f_t = sum_{n<=N} b_n^t/n^{s_*} + gamma * sum_{n<=N} n^y b_n^t/n^{conj(s_*)+kappa}
with s_* = (1+y-ix)/2 + (t/2)*alpha((1+y-ix)/2), alpha(s) = 1/(2s)+1/(s-1)+0.5*Log(s/(2*pi)),
kappa = (t/2)*(alpha((1-y+ix)/2) - alpha((1+y+ix)/2)),
gamma = M_t((1-y+ix)/2)/M_t((1+y-ix)/2),
log M_0(s) = Log s + Log(s-1) - (s/2)log pi + log(sqrt(2*pi)/16) + (s/2-1/2)Log(s/2) - s/2,
M_t = exp(t/4*alpha(s)^2)*M_0.
b_n^t = exp(t/4*log^2 n). All per dbn/Writeup/debruijn.tex (alpha-form, sn-def,
kappa-def, lambda-def, ft-def, bn-def, M-def, logM).
"""
import mpmath as mp
mp.mp.dps = 70

# Table 1 row 2 (debruijn.tex table tab:table1)
t  = mp.mpf('0.186')
x  = mp.mpf('630783')
y  = mp.mpf('0.16733')
N  = mp.mpf('630783')

def Log(z): return mp.log(z)          # principal branch
def alpha(s): return 1/(2*s) + 1/(s-1) + 0.5*Log(s/(2*mp.pi))
def logM0(s): return Log(s) + Log(s-1) - (s/2)*mp.log(mp.pi) + mp.log(mp.sqrt(2*mp.pi)/16) + (s/2-0.5)*Log(s/2) - s/2
def logMt(s, t): return mp.exp(t/4*alpha(s)**2) + logM0(s)

w  = (1+y-1j*x)/2            # (1+y-ix)/2
w2 = (1-y+1j*x)/2            # (1-y+ix)/2  [conjugate of (1-y-ix)/2 = w]
w3 = (1+y+1j*x)/2            # (1+y+ix)/2  [for kappa]

s_star = w + (t/2)*alpha(w)
kappa  = (t/2)*(alpha(w2) - alpha(w3))
gamma  = mp.exp(logMt(w2, t) - logMt(w, t))
conj_s = mp.conj(s_star)

print(f"Re(s_*) = {mp.nstr(mp.re(s_star), 12)}")
print(f"Im(s_*) = {mp.nstr(mp.im(s_star), 12)}")
print(f"|gamma| = {mp.nstr(abs(gamma), 12)}")
print(f"Re(kappa) = {mp.nstr(mp.re(kappa), 12)}  Im(kappa) = {mp.nstr(mp.im(kappa), 12)}")

# direct sums, n = 1..N
s1 = mp.mpc(0)  # sum b_n^t / n^{s_*}
s2 = mp.mpc(0)  # sum n^y b_n^t / n^{conj(s_*)+kappa}
Nint = int(N)
for n in range(1, Nint+1):
    ln = mp.log(mp.mpf(n))
    bt = mp.exp(t/4*ln*ln)
    s1 += bt / mp.mpf(n)**s_star
    s2 += mp.mpf(n)**y * bt / mp.mpf(n)**(conj_s + kappa)

f = s1 + gamma*s2
print(f"|sum_beta|      = {mp.nstr(abs(s1), 12)}")
print(f"|gamma*sum_alpha| = {mp.nstr(abs(gamma*s2), 12)}")
print(f"|f| (direct)    = {mp.nstr(abs(f), 12)}")

# Euler factors (70 digits)
E3 = mp.mpc(1); E5 = mp.mpc(1)
for i, p in enumerate([2,3,5,7,11]):
    bpt = mp.exp(t/4*mp.log(mp.mpf(p))**2)
    E5 = E5*(1 - bpt/mp.mpf(p)**s_star)
    if i < 3:
        E3 = E3*(1 - bpt/mp.mpf(p)**s_star)
print(f"|E_{{t,5}}|  (primes 2,3,5)      = {mp.nstr(abs(E3), 12)}")
print(f"|E_{{t,11}}| (primes 2,3,5,7,11) = {mp.nstr(abs(E5), 12)}")
print(f"program bounds: m=0 -> -0.394278366241688 ; m=3 -> 0.466572104328199 ; m=5 -> 0.519046677344531")
print(f"paper table   = 0.0376 (final |f| bound, O-terms included)")
print("all lower bounds <= direct |f|: " + str(abs(E3) >= 0 and 0.466572104328199 <= abs(f) and 0.519046677344531 <= abs(f) and -0.394278366241688 <= abs(f) and 0.0376 <= abs(f)))
