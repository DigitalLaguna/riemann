# Diagnostic: is Z(t)=e^{iθ}ζ(1/2+it) real? Does adding terms to the bare RS
# sum reduce the error (truncation) or not (remainder)?
import mpmath as mp
mp.mp.dps = 50

def theta_exact(t):
    return mp.arg(mp.gamma(mp.mpf(1)/4 + mp.j*t/2)) - (t/2)*mp.log(mp.pi)

def rs(t, N):
    th = theta_exact(t)
    s = mp.mpf(0)
    for n in range(1, N+1):
        s += mp.cos(th - t*mp.log(n)) / mp.sqrt(n)
    return 2*s

for t in [mp.mpf(10), mp.mpf(100), mp.mpf(1000), mp.mpf(10000), mp.mpf(100000)]:
    z = mp.zeta(mp.mpf(1)/2 + mp.j*t)
    th = theta_exact(t)
    Z = mp.e**(mp.j*th)*z
    N0 = int(mp.floor(mp.sqrt(t/(2*mp.pi))))
    print(f"t={float(t):<8.0f} Z={float(mp.re(Z)):.12f} Im(Z)={float(mp.im(Z)):.2e} N0={N0}")
    for k in [0, 1, 2, 5]:
        N = N0 + k
        S = rs(t, N)
        print(f"   N={N:<4} S={float(S):.12f} err={float(abs(Z-S)):.3e}")
