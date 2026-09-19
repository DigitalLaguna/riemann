# Finer-grid C3a: locate true Kmax (max K s.t. max_sigma k0term <= -0.041).
import mpmath as mp
mp.mp.dps = 60
M = 6
kap0 = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
        mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
sigma0 = mp.mpf('0.9935164')
def k0term(kap, sigma):
    s = mp.mpf(0)
    for m in range(M+1):
        dm = (2*sigma-1)*m
        s += kap[m]*mp.digamma((sigma+dm)/2 + 1)
    return s
def k0max(kap, N=2000):
    best = mp.mpf('-inf'); bestsig = None
    for i in range(N+1):
        sigma = sigma0 + (1-sigma0)*mp.mpf(i)/N
        v = k0term(kap, sigma)
        if v > best: best = v; bestsig = sigma
    return best, bestsig
# bisection for Kmax with fine grid
lo = mp.mpf(0); hi = mp.mpf('0.1')
for _ in range(60):
    mid = (lo+hi)/2
    kap = list(kap0); kap[6] = kap[6] + mid
    v, _ = k0max(kap)
    if v <= mp.mpf('-0.041'): lo = mid
    else: hi = mid
Kmax = (lo+hi)/2
v, sig = k0max(list(kap0)+[0]*0 and [kap0[0],kap0[1],kap0[2],kap0[3],kap0[4],kap0[5],kap0[6]+Kmax])
print("Kmax (2000-grid) =", mp.nstr(Kmax,15))
print("k0max at Kmax =", mp.nstr(v,15), " at sigma =", mp.nstr(sig,12))
# use K slightly below Kmax for a positive margin
for frac in [1.0, mp.mpf('0.9999'), mp.mpf('0.999')]:
    K = Kmax*frac
    kap = list(kap0); kap[6] = kap[6] + K
    kappa = sum(kap)
    v, sig = k0max(kap)
    margin = v - mp.mpf('-0.041')
    print(f"K={mp.nstr(K,12)} (frac={mp.nstr(frac,6)}): k0max={mp.nstr(v,15)} margin={mp.nstr(margin,15)} C3a holds? {bool(margin<=0)} kappa={mp.nstr(kappa,15)}")
