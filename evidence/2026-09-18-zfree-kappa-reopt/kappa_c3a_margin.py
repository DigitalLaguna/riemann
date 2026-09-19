# C3a margin check at the exact K used in the re-optimization (Kmax_c3a).
# k0term(kap, sigma) = sum_m kap[m] * digamma((sigma + (2sigma-1)m)/2 + 1)
# C3a (Lemma 12) requires max_{sigma in [sigma0,1)} k0term <= -0.041.
# We check the margin at K = 0.03830132421 (used) and K = 0.0383013242 (reduced).
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
def k0max(kap):
    best = mp.mpf('-inf')
    for i in range(400):
        sigma = sigma0 + (1-sigma0)*mp.mpf(i)/400
        v = k0term(kap, sigma)
        if v > best: best = v
    return best
def A_final(kap):
    a = mp.mpf(2919857)/mp.mpf(828465); w0 = mp.mpf('5.672787598')
    K = mp.mpf(16); T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12
    xT = mp.mpf('76.47'); c = mp.log(K + T0/H)
    def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
    def C2(eta): return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3
    den = a*kap**2*w0/2
    A = mp.mpf('0.2')
    for i in range(300):
        Anew = (C1(1-c/xT) + C2(A/xT) - mp.mpf('1e-7'))/den
        if abs(Anew-A) < mp.mpf('1e-45'): A = Anew; break
        A = Anew
    return A
A0_max = mp.mpf('0.392113247395366294')
for label, K in [("K_used=0.03830132421", mp.mpf('0.03830132421')),
                 ("K_red =0.0383013242 ", mp.mpf('0.0383013242'))]:
    kap = list(kap0); kap[6] = kap[6] + K
    kappa = sum(kap)
    k0m = k0max(kap)
    margin = k0m - mp.mpf('-0.041')   # <=0 means C3a holds
    Af = A_final(kappa)
    print(f"--- {label} ---")
    print(f"  kappa = {mp.nstr(kappa,15)}")
    print(f"  k0max = {mp.nstr(k0m,15)}  (bound -0.041)")
    print(f"  C3a margin (k0max - (-0.041)) = {mp.nstr(margin,15)}  C3a holds? {bool(margin <= 0)}")
    print(f"  A_final = {mp.nstr(Af,15)}  A_final < A0_max? {bool(Af < A0_max)}  (A0_max={mp.nstr(A0_max,15)})")
    print(f"  1/A_final = {mp.nstr(1/Af,12)}")
print("=== VERDICT ===")
