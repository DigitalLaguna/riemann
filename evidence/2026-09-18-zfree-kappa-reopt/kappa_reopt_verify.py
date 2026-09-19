import mpmath as mp
mp.mp.dps = 60
# paper kappa_m (eq 18)
kap_paper_list = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
                  mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
kap_paper = sum(kap_paper_list)
Kmax_c3a = mp.mpf('0.03830132421')
# optimized: kappa_6 += Kmax_c3a
kap_new_list = list(kap_paper_list)
kap_new_list[6] = kap_new_list[6] + Kmax_c3a
kap_new = sum(kap_new_list)

a   = mp.mpf(2919857)/mp.mpf(828465)
w0  = mp.mpf('5.672787598')
K   = mp.mpf(16); T0 = mp.mpf(10)**10; H = mp.mpf(3)*mp.mpf(10)**12
xT  = mp.mpf('76.47')
c_mu_sharp = mp.log(K + T0/H)
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def C2(eta):return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3
def A_final(kap):
    den = a*kap**2*w0/2
    A = mp.mpf('0.2')
    for i in range(300):
        Anew = (C1(1-c_mu_sharp/xT) + C2(A/xT) - mp.mpf('1e-7'))/den
        if abs(Anew-A) < mp.mpf('1e-45'): A=Anew; break
        A = Anew
    return A

A0_max = mp.mpf('0.392113247395366294')
Af_paper = A_final(kap_paper)
Af_new   = A_final(kap_new)
print("=== Re-optimization verification ===")
print(f"kap_paper = {mp.nstr(kap_paper,15)}")
print(f"kap_new   = {mp.nstr(kap_new,15)}  (kappa_6 = {mp.nstr(kap_new_list[6],15)})")
print(f"A_final(paper) = {mp.nstr(Af_paper,15)}  (target 0.420483467794)")
print(f"A_final(new)   = {mp.nstr(Af_new,15)}")
print(f"A0_max         = {mp.nstr(A0_max,15)}")
print()
print(f"A_final(new) < A0_max ? {bool(Af_new < A0_max)}")
print(f"improvement: A0_max - A_final(new) = {mp.nstr(A0_max - Af_new,15)}")
print(f"relative improvement: {mp.nstr((A0_max-Af_new)/A0_max,6)}")
print()
print(f"effective region constant (new) = min(A_final(new), A0_max) = {mp.nstr(min(Af_new, A0_max),15)}")
print(f"effective region constant (paper) = min(A_final(paper), A0_max) = {mp.nstr(min(Af_paper, A0_max),15)}")
print()
print("=== VERDICT ===")
if Af_new < A0_max:
    print("RE-OPTIMIZATION SUCCEEDS: A_final(new) < A0_max")
    print(f"  new effective constant = {mp.nstr(Af_new,15)} (was {mp.nstr(A0_max,15)})")
    print(f"  headline 1/A_final(new) = {mp.nstr(1/Af_new,12)} (was {mp.nstr(1/A0_max,12)})")
else:
    print("RE-OPTIMIZATION FAILS: A_final(new) >= A0_max")
