import mpmath as mp
mp.mp.dps = 60
import numpy as np

# ---- paper's kappa_m (eq 18, verbatim) ----
kap_m = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
         mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
kap_paper = sum(kap_m)
print("kappa_paper = sum(kappa_m) =", mp.nstr(kap_paper,15), " (paper: 433/859 =", mp.nstr(mp.mpf(433)/859,15), ")")
print("  match 433/859:", mp.nstr(abs(kap_paper-mp.mpf(433)/859)<mp.mpf('1e-30'),1))

# ---- p(x) = sum kappa_m x^m ; target 1/(1+x) ----
def p(x):
    s = mp.mpf(0)
    for m,km in enumerate(kap_m):
        s += km * x**m
    return s
# L-infinity error on a fine grid
xs = [mp.mpf(i)/200000 for i in range(200001)]
errs = [abs(p(x) - 1/(1+x)) for x in xs]
E_paper = max(errs)
x_at_E = xs[errs.index(E_paper)]
print("\nE_paper = max_{x in [0,1]} |p(x) - 1/(1+x)| =", mp.nstr(E_paper,12), " at x =", mp.nstr(x_at_E,6))

# ---- A_final (reproduction gate): reopt.py CASE 3 formula ----
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

Af = A_final(kap_paper)
print("\nREPRODUCTION GATE:")
print("  A_final(kappa_paper) =", mp.nstr(Af,15))
print("  target 0.420483467794  match:", mp.nstr(abs(Af-mp.mpf('0.420483467794'))<mp.mpf('1e-9'),1))
print("  headline 1/A_final =", mp.nstr(1/Af,12))

# ---- what kappa is needed for A_final < A0_max ? ----
A0_max = mp.mpf('0.392113247395366294')
# solve A_final(kap) = A0_max for kap  (bisection)
lo, hi = kap_paper, mp.mpf('0.6')
for _ in range(200):
    mid = (lo+hi)/2
    if A_final(mid) > A0_max: lo = mid
    else: hi = mid
kap_need = (lo+hi)/2
print("\n  A0_max =", mp.nstr(A0_max,15))
print("  kappa needed for A_final < A0_max:", mp.nstr(kap_need,12), " (paper kappa =", mp.nstr(kap_paper,12), ")")
print("  required relative increase in kappa:", mp.nstr(kap_need/kap_paper-1,6))
