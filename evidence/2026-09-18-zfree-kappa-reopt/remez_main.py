import numpy as np, mpmath as mp
from remez import remez
mp.mp.dps = 40

g = lambda x: -x/(1.0+x)
# L-infinity minimizer of g on [0,1] by span{x..x^6}
c, E, xs, it = remez(g, 6, 0.0, 1.0, [0.1,0.25,0.4,0.55,0.7,0.85,0.97], grid_n=200001)
kappa_minimax = 1.0 + sum(c)   # p(1) = 1 + q(1)
print("L-infinity minimizer (n=6, zero const term):")
print("  coeffs c[1..6] =", np.array2string(c, precision=12))
print("  E_minimax =", "%.12f"%E, " iters=", it)
print("  extremal pts =", np.array2string(xs, precision=6))
print("  kappa_minimax = 1+sum(c) =", "%.12f"%kappa_minimax)

# paper
kap_paper = 433/859
print("\npaper kappa =", "%.12f"%kap_paper)
print("  delta (minimax - paper) =", "%.6e"%(kappa_minimax-kap_paper))
print("  minimax better kappa?", kappa_minimax > kap_paper)

# A_final with kappa_minimax
a = mp.mpf(2919857)/mp.mpf(828465); w0 = mp.mpf('5.672787598')
xT = mp.mpf('76.47'); c_mu_sharp = mp.log(mp.mpf(16)+mp.mpf(10)**10/(mp.mpf(3)*mp.mpf(10)**12))
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def C2(eta):return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3
def A_final(kap):
    den = a*mp.mpf(kap)**2*w0/2
    A = mp.mpf('0.2')
    for i in range(300):
        Anew = (C1(1-c_mu_sharp/xT) + C2(A/xT) - mp.mpf('1e-7'))/den
        if abs(Anew-A) < mp.mpf('1e-45'): A=Anew; break
        A=Anew
    return A
A0_max = mp.mpf('0.392113247395366294')
Af_mm = A_final(kappa_minimax)
print("\nA_final(kappa_minimax) =", mp.nstr(Af_mm,15), "  (< A0_max?", mp.nstr(Af_mm<A0_max,1), ")")
print("A_final(kappa_paper)   =", mp.nstr(A_final(kap_paper),15))
