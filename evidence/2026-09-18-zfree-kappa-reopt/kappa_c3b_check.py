import mpmath as mp
mp.mp.dps = 50
# Paper kappa_m (eq 18)
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
# a_k: a0=1, a1=865534/497079, sum_{k>=1} a_k = 2919857/828465
a0 = mp.mpf(1)
a1 = mp.mpf(865534)/mp.mpf(497079)
a = mp.mpf(2919857)/mp.mpf(828465)   # sum_{k>=1} a_k
kappa_paper = sum(kap_paper)
kappa_req = mp.mpf('0.521015891482995')
Kmax_c3a = mp.mpf('0.03830132421')

def sum_pos(kap):
    return sum(k for k in kap if k > 0)

def check(K, label):
    kap = list(kap_paper)
    kap[6] = kap[6] + K
    sp = sum_pos(kap)
    budget = a * sp
    kappa = sum(kap)
    print(f"[{label}] K={mp.nstr(K,12)}  kappa_6={mp.nstr(kap[6],12)}")
    print(f"  sum_pos = {mp.nstr(sp,15)}")
    print(f"  a = {mp.nstr(a,15)}")
    print(f"  budget = a*sum_pos = {mp.nstr(budget,15)}  (need <= 10)")
    print(f"  budget <= 10 ? {bool(budget <= 10)}   margin = {mp.nstr(10-budget,15)}")
    print(f"  kappa = {mp.nstr(kappa,15)}  (need > {mp.nstr(kappa_req,15)})")
    print(f"  kappa > kappa_req ? {bool(kappa > kappa_req)}")
    return bool(budget <= 10) and bool(kappa > kappa_req)

print("=== Lemma 13 (C3b) budget check: a*sum(positive kappa_m) <= 10 ===")
print()
print("--- paper kappa (K=0) ---")
check(mp.mpf(0), "paper")
print()
print("--- K = Kmax_c3a (C3a binding limit) ---")
ok1 = check(Kmax_c3a, "Kmax_c3a")
print()
print("--- K = 0.017 (mid-range) ---")
check(mp.mpf('0.017'), "K=0.017")
print()
print("--- K = 0.038 (just below C3a limit) ---")
check(mp.mpf('0.038'), "K=0.038")
print()
print("=== VERDICT ===")
print(f"(C3b) Lemma 13 satisfied at K=Kmax_c3a ? {ok1}")
print(f"=> (C3b) does NOT kill the idea (budget has margin {mp.nstr(10-a*sum_pos([k if i!=6 else k+Kmax_c3a for i,k in enumerate(kap_paper)]),12)})")
