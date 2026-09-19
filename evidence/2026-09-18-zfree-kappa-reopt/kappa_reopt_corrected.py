# Corrected re-optimization: K = Kmax_fine*0.9999 (positive C3a margin).
import mpmath as mp
mp.mp.dps = 60
kap0 = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
        mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
Kmax_fine = mp.mpf('0.0382982544817207')
K = Kmax_fine*mp.mpf('0.9999')
kap = list(kap0); kap[6] = kap[6] + K
kappa = sum(kap)
a = mp.mpf(2919857)/mp.mpf(828465); w0 = mp.mpf('5.672787598')
Kc = mp.mpf(16); T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12
xT = mp.mpf('76.47'); c = mp.log(Kc + T0/H)
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def C2(eta): return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3
def A_final(kap):
    den = a*kap**2*w0/2; A = mp.mpf('0.2')
    for i in range(300):
        Anew = (C1(1-c/xT) + C2(A/xT) - mp.mpf('1e-7'))/den
        if abs(Anew-A) < mp.mpf('1e-45'): A = Anew; break
        A = Anew
    return A
A0_max = mp.mpf('0.392113247395366294')
Af = A_final(kappa)
print("=== Corrected re-optimization ===")
print(f"K = {mp.nstr(K,15)}  (Kmax_fine={mp.nstr(Kmax_fine,15)}, frac 0.9999)")
print(f"kappa_6 = {mp.nstr(kap[6],15)}")
print(f"kappa = {mp.nstr(kappa,15)}  (required > 0.521015891482995: {bool(kappa>mp.mpf('0.521015891482995'))})")
print(f"A_final = {mp.nstr(Af,15)}")
print(f"A0_max  = {mp.nstr(A0_max,15)}")
print(f"A_final < A0_max ? {bool(Af < A0_max)}")
print(f"effective constant = min(A_final,A0_max) = {mp.nstr(min(Af,A0_max),15)}")
print(f"headline 1/A_final = {mp.nstr(1/Af,12)}  (paper 2.55028364036)")
print("=== VERDICT ===")
if Af < A0_max:
    print("CORRECTED RE-OPTIMIZATION SUCCEEDS (positive C3a margin)")
    print(f"  new effective constant = {mp.nstr(Af,15)} (was 0.392113247395366)")
    print(f"  headline 1/A_final = {mp.nstr(1/Af,12)} (was 2.55028364036)")
else:
    print("CORRECTED RE-OPTIMIZATION FAILS")
