import mpmath as mp
mp.mp.dps = 60
# ---- exact inputs (verbatim, machine-verified #33/#38/#40/#54) ----
a   = mp.mpf(2919857)/mp.mpf(828465)   # sum_{k>=1} a_k, line 1521/1896
w0  = mp.mpf('5.672787598')            # line 530
xT  = mp.mpf('76.47')
A0_max = mp.mpf('0.392113247395366294') # claim #54
kap_paper = mp.mpf(433)/mp.mpf(859)
kap_req   = mp.mpf('0.521015891482995') # tick 265 threshold
Kmax_c3a  = mp.mpf('0.03830132421')     # tick 268 (C3a) binding
kap_max   = kap_paper + Kmax_c3a        # 0.542375829449
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def C2(eta): return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3
c_mu = mp.log(mp.mpf(16)+mp.mpf(1)/mp.mpf(300))  # log(K+T0/H)
def A_final(kappa):
    den = a*kappa**2*w0/2
    A = mp.mpf('0.4')
    for i in range(300):
        Anew = (C1(1-c_mu/xT)+C2(A/xT)-mp.mpf('1e-7'))/den
        if abs(Anew-A) < mp.mpf('1e-45'): A=Anew; break
        A = Anew
    return A
# ---- A_final at threshold and at max allowed kappa ----
Af_req = A_final(kap_req)
Af_max = A_final(kap_max)
print("=== A_final re-optimization ===")
print("kappa_paper  =", mp.nstr(kap_paper,15))
print("kappa_required (A_final=A0_max) =", mp.nstr(kap_req,15))
print("kappa_max (C3a binding)         =", mp.nstr(kap_max,15))
print("A_final(kappa_req) =", mp.nstr(Af_req,15), " (should == A0_max)")
print("A_final(kappa_max) =", mp.nstr(Af_max,15))
print("A0_max             =", mp.nstr(A0_max,15))
A_eff_old = min(A_final(kap_paper), A0_max)
A_eff_new = min(Af_max, A0_max)
print("OLD effective A  =", mp.nstr(A_eff_old,15), " headline 1/A =", mp.nstr(1/A_eff_old,15))
print("NEW effective A  =", mp.nstr(A_eff_new,15), " headline 1/A =", mp.nstr(1/A_eff_new,15))
print("improvement in 1/A =", mp.nstr((1/A_eff_new-1/A_eff_old),12))
print("A_final(kappa_max) < A0_max ?", bool(Af_max < A0_max))
# ---- (C3b) Lemma 13 machine check for modified kappa (paper + K*x^6) ----
# Added term to LHS: K * sum_{k>=1} a_k Re W((s_k+delta_6-1)/eta)
# Use paper asymptotic Re W(z) = w(0) Re(z)/|z|^2 + O*(C|z|^3), C<51, |z|>1e10.
# Bound |Re W| <= w0*|Re z|/|z|^2 + 51/|z|^3.
H  = mp.mpf(3)*mp.mpf(10)**12
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
K = Kmax_c3a
worst = mp.mpf('0')
for i in range(25):
    s = sigma0 + (1-sigma0-mp.mpf('1e-9'))*mp.mpf(i)/24
    for j in range(25):
        eta = mp.mpf(1-s)/ (mp.mpf((1-sigma0)/eta0 - mp.mpf('1e-10')) + (1-mp.mpf((1-sigma0)/eta0 - mp.mpf('1e-10')))*mp.mpf(j)/24)
        if eta > eta0+mp.mpf('1e-12'): continue
        d6 = (2*s-1)*mp.mpf(6)
        for k in range(1,17):
            z = (s + mp.j*k*H + d6 - 1)/eta   # t=H (min), worst case |z|
            reW = w0*abs((s+d6-1)/eta)/abs(z)**2 + mp.mpf(51)/abs(z)**3
            if reW > worst: worst = reW
added_bound = K*a*worst
margin_c3b = mp.mpf('1e-10')*eta0
print("=== (C3b) Lemma 13 check (modified kappa, K=%.10f) ===" % K)
print("max |Re W| bound (asymptotic, t=H) =", mp.nstr(worst,6))
print("added term bound K*a*max|ReW|       =", mp.nstr(added_bound,6))
print("RHS margin 1e-10*eta0               =", mp.nstr(margin_c3b,6))
print("added < margin ?", bool(added_bound < margin_c3b))
print("ratio margin/added =", mp.nstr(margin_c3b/added_bound,4))
