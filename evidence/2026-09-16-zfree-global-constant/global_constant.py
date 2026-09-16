import mpmath as mp
mp.mp.dps = 50
# A(t) = effective "A" in sigma > 1 - A(t)/log t, per t.
# HB (Heath-Brown / Lemma 1) range: 3 <= t <= exp(T_LB), A = A_HB (constant).
# Littlewood (3): t >= 3, A_LW(t) = loglog t / K_LW (increasing in t).
# Global C = 1 / min_t A(t) = 1 / min(A_HB, A_LW(T_LB)).
def global_C(A_HB, T_LB, K_LW):
    a_lb = mp.log(mp.log(mp.e**T_LB)) / K_LW   # = log(T_LB)/K_LW
    a_min = min(A_HB, a_lb)
    return 1/a_min, a_min, a_lb
# values from ledger #40/#54/#55 and paper
A_paper_L1  = 1/mp.mpf('4.896')          # paper Lemma 1 A
A0_paper    = 1/mp.mpf('4.8596')         # paper A0 constraint (Lemma 2 4.8594 rounded up)
A_final     = mp.mpf('0.420483467794')   # #40 reopt Lemma 1
A0_max      = mp.mpf('0.392113247395366294')  # #54 pinned
T_L1, T_L2  = mp.mpf('76.47'), mp.mpf('56.693')
K_pub, K_th = mp.mpf('21.233'), mp.mpf('19.62')  # published / thesis Littlewood
cases = {
 'paper Thm1 (A=1/4.896, T=76.47, K=21.233)': (A_paper_L1, T_L1, K_pub),
 'reopt + pub LW (A=0.392113, T=76.47, K=21.233)': (A0_max, T_L1, K_pub),
 'reopt + thesis LW (A=0.392113, T=76.47, K=19.62)': (A0_max, T_L1, K_th),
 'paper Thm2 (A=1/4.8594, T=56.693, K=19.62)': (1/mp.mpf('4.8594'), T_L2, K_th),
 'reopt L2 + thesis LW (A=0.392113, T=56.693, K=19.62)': (A0_max, T_L2, K_th),
}
print("case | global C | min A | A_LW at T_LB")
for name,(a,t,k) in cases.items():
    C,amin,alb = global_C(a,t,k)
    print(f"{name}: C={mp.nstr(C,12)} minA={mp.nstr(amin,12)} A_LW(T_LB)={mp.nstr(alb,12)}")
# numerical cross-check of min over a log grid for the reopt+pub case
a,t,k = A0_max, T_L1, K_pub
mn = mp.inf
for i in range(0,200000):
    u = mp.log(3) + (mp.log(mp.e**t)-mp.log(3))*i/199999   # u=log t in [log3, t]
    tt = mp.e**u
    A = a if u <= t else mp.log(u)/k
    if A < mn: mn = A
print("numerical min A (reopt+pub):", mp.nstr(mn,12), "-> C =", mp.nstr(1/mn,12))
# where does A_LW(t) reach A0_max (crossover for reopt+pub and reopt+thesis)?
for k,name in [(K_pub,'pub'),(K_th,'thesis')]:
    # solve loglog t / k = A0_max  ->  log t = e^(A0_max*k)
    u = mp.e**(A0_max*k)
    print(f"crossover reopt vs {name} LW: log t = {mp.nstr(u,10)} (t = exp({mp.nstr(u,10)}))")
