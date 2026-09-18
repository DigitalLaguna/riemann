import mpmath as mp
mp.mp.dps = 60

# ---- exact inputs from the paper (verbatim, machine-verified in #33/#38/#40) ----
a   = mp.mpf(2919857)/mp.mpf(828465)   # line 1896: a = sum a_k
kap = mp.mpf(433)/mp.mpf(859)          # line 1904: kappa = sum_{0<=m<=M} kappa_m
w0  = mp.mpf('5.672787598')            # line 530
K   = mp.mpf(16)                        # line 535
T0  = mp.mpf(10)**10                    # line 532
H   = mp.mpf(3)*mp.mpf(10)**12          # line 163
xT  = mp.mpf('76.47')                   # Lemma 1 top endpoint exp(76.47)
A0_max = mp.mpf('0.392113247395366294') # claim #54 (pinned A0_max)

# C1, C2 (Lemma 14 / line 2068, 2527)
def C1(mu):  return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def C2(eta): return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3

c_mu_sharp = mp.log(K + T0/H)   # = log(16 + 1/300) = 2.77279703387

def A_final(kappa):
    # fixed point: A = [C1(1-c_mu/xT) + C2(A/xT) - 1e-7] / (a*kappa^2*w0/2)
    den = a*kappa**2*w0/2
    A = mp.mpf('0.4')
    for i in range(300):
        Anew = (C1(1-c_mu_sharp/xT) + C2(A/xT) - mp.mpf('1e-7'))/den
        if abs(Anew-A) < mp.mpf('1e-45'): A=Anew; break
        A = Anew
    return A, i

# ---- REPRODUCTION GATE: paper's kappa_m -> A_final = 0.420483467794 (claim #40) ----
Af, it = A_final(kap)
target = mp.mpf('0.420483467794')
print("REPRODUCTION GATE (paper kappa_m, kappa = 433/859):")
print("  A_final(paper) =", mp.nstr(Af,15))
print("  target (#40)   =", mp.nstr(target,15))
print("  |diff|         =", mp.nstr(abs(Af-target),3))
print("  REPRODUCED     =", mp.nstr(abs(Af-target) < mp.mpf('1e-9'),1), " (iters", it, ")")

# ---- required kappa so that A_final = A0_max (threshold for improvement) ----
# A0_max = [C1(1-c_mu/xT) + C2(A0_max/xT) - 1e-7] / (a*kappa^2*w0/2)
num = C1(1-c_mu_sharp/xT) + C2(A0_max/xT) - mp.mpf('1e-7')
kap_req = mp.sqrt(num/(a*A0_max*w0/2))
print("\nTHRESHOLD (A_final = A0_max):")
print("  A0_max          =", mp.nstr(A0_max,15))
print("  kappa_paper     =", mp.nstr(kap,15))
print("  kappa_required  =", mp.nstr(kap_req,15))
print("  required increase =", mp.nstr((kap_req/kap-1)*100,4), "%")
print("  (need A_final < A0_max, i.e. kappa > kappa_required)")

# ---- sanity: A_final at paper kappa vs A0_max (is A_final binding?) ----
print("\nCURRENT STATE:")
print("  A_final(paper) =", mp.nstr(Af,12), " A0_max =", mp.nstr(A0_max,12))
print("  A_final > A0_max (A0_max binds) =", mp.nstr(Af > A0_max,1))
print("  effective A = min =", mp.nstr(min(Af,A0_max),12), " headline 1/A =", mp.nstr(1/min(Af,A0_max),12))
