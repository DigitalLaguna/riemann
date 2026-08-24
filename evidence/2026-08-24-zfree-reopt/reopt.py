import mpmath as mp
mp.mp.dps = 60

# ---- exact inputs from the paper (verbatim, machine-verified in #33/#38) ----
a   = mp.mpf(2919857)/mp.mpf(828465)   # line 1896: a = sum a_k
kap = mp.mpf(433)/mp.mpf(859)          # line 1896: kappa = sum kappa_m
w0  = mp.mpf('5.672787598')            # line 530, verified claim #33
K   = mp.mpf(16)                        # line 535
T0  = mp.mpf(10)**10                    # line 532
H   = mp.mpf(3)*mp.mpf(10)**12          # line 163
xH  = mp.log(H)                         # log H
xT  = mp.mpf('76.47')                   # Lemma 1 top endpoint exp(76.47)
A0  = 1/mp.mpf('4.8596')                # table line 545: Lemma 1 A0

# C1, C2 (Lemma 14 / line 2068, 2527)
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def C2(eta):return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3

den_paper = a*kap*w0/2      # (a kappa w(0)/2)  [paper's final line]
den_corr  = a*kap**2*w0/2   # (a kappa^2 w(0)/2) [corrected, claim #38]

c_mu_sharp = mp.log(K + T0/H)   # = log(16 + 1/300); paper rounds up to 2.78
print("c_mu_sharp = log(K+T0/H) =", mp.nstr(c_mu_sharp,12), " (paper uses 2.78)")
print("den_paper =", mp.nstr(den_paper,12))
print("den_corr  =", mp.nstr(den_corr,12))
print("A0 = 1/4.8596 =", mp.nstr(A0,12))

# ---- Case 1: paper's final line (c_mu=2.78, eta=1/(6 x), denom_paper) ----
def final_line(c_mu, eta_of_x, denom, x):
    return (C1(1-c_mu/x) + C2(eta_of_x(x)) - mp.mpf('1e-7'))/denom

# paper: eta = 1/(6 x)
B_paper = final_line(mp.mpf('2.78'), lambda x: 1/(mp.mpf(6)*x), den_paper, xT)
print("\nCASE 1 (paper): B =", mp.nstr(B_paper,12), " headline 1/B =", mp.nstr(1/B_paper,12))
print("  target B_paper=0.2042607196  match:", mp.nstr(abs(B_paper-mp.mpf('0.2042607196'))<mp.mpf('1e-6'),1))

# ---- Case 2: corrected final line (c_mu=2.78, eta=1/(6 x), denom_corr) ----
B_corr = final_line(mp.mpf('2.78'), lambda x: 1/(mp.mpf(6)*x), den_corr, xT)
print("\nCASE 2 (corrected, no fixed pt): B =", mp.nstr(B_corr,12), " headline 1/B =", mp.nstr(1/B_corr,12))
print("  target B_corr=0.4052193028  match:", mp.nstr(abs(B_corr-mp.mpf('0.4052193028'))<mp.mpf('1e-6'),1))

# ---- Case 3: re-optimized (sharp c_mu, eta=A/x fixed point, denom_corr) ----
# A* = [C1(1-c_mu_sharp/xT) + C2(A*/xT) - 1e-7]/den_corr   (min at xT, verify below)
A = A0
for i in range(200):
    Anew = (C1(1-c_mu_sharp/xT) + C2(A/xT) - mp.mpf('1e-7'))/den_corr
    if abs(Anew-A) < mp.mpf('1e-40'): A=Anew; break
    A = Anew
print("\nCASE 3 (reopt fixed point): A* =", mp.nstr(A,12), " headline 1/A* =", mp.nstr(1/A,12))
print("  iterations:", i, " converged:", mp.nstr(abs(Anew-A)<mp.mpf('1e-40'),1))

# ---- Monotonicity: is the numerator decreasing on [xH, xT]? (min at xT) ----
def num(c_mu, eta_of_x, x):
    return C1(1-c_mu/x) + C2(eta_of_x(x)) - mp.mpf('1e-7')
def check_decreasing(c_mu, eta_of_x, label):
    xs = [xH + (xT-xH)*mp.mpf(k)/200 for k in range(201)]
    vals = [num(c_mu, eta_of_x, x) for x in xs]
    dec = all(vals[k] >= vals[k+1] for k in range(200))
    print(f"  {label}: decreasing on [xH,xT] =", dec,
          " min-at-xT value =", mp.nstr(vals[-1],10), " max-at-xH =", mp.nstr(vals[0],10))
print("\nMonotonicity (numerator, min should be at xT):")
check_decreasing(mp.mpf('2.78'), lambda x: 1/(mp.mpf(6)*x), "case1 paper")
check_decreasing(c_mu_sharp, lambda x: A/x, "case3 reopt")

# ---- A0 constraint: effective constant = min(A_final, A0) ----
print("\nA0 constraint (lemmas require A <= A0 = 1/4.8596):")
for label, Af in [("paper",B_paper),("corrected",B_corr),("reopt",A)]:
    eff = min(Af, A0)
    print(f"  {label:10s} A_final={mp.nstr(Af,10)}  A0={mp.nstr(A0,10)}  effective A={mp.nstr(eff,10)}  headline 1/A={mp.nstr(1/eff,10)}")

# ---- Where does A0 = 1/4.8596 come from? Test: paper's own fixed point ----
# A = [C1(1-2.78/x) + C2(A/x) - 1e-7]/den_paper  at x=xT  (paper formula, missing kappa, sharp c_eta)
A = A0
for i in range(300):
    Anew = (C1(1-mp.mpf('2.78')/xT) + C2(A/xT) - mp.mpf('1e-7'))/den_paper
    if abs(Anew-A) < mp.mpf('1e-40'): A=Anew; break
    A = Anew
print("\nPaper's own fixed point (missing kappa, sharp c_eta): A =", mp.nstr(A,12), " headline 1/A =", mp.nstr(1/A,12))
print("  vs table A0 headline 4.8596  ->  A0 is the paper's fixed point:", mp.nstr(abs(1/A-mp.mpf('4.8596'))<mp.mpf('1e-3'),1))
