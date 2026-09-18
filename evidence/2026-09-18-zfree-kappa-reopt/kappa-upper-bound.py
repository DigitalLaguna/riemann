import mpmath as mp
mp.mp.dps = 60

# Paper's kappa_m (eq 18), f(x) = 1/(1+x)
kap = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
       mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
def p(x):
    s = mp.mpf(0)
    for m, c in enumerate(kap):
        s += c * x**m
    return s
def f(x):
    return 1/(1+x)

# E_paper = max_{x in [0,1]} |p(x) - f(x)|  (dense scan + refine)
N = 200000
best = mp.mpf(0); bestx = mp.mpf(0)
for i in range(N+1):
    x = mp.mpf(i)/N
    e = abs(p(x) - f(x))
    if e > best:
        best = e; bestx = x
# refine around bestx with golden-section-ish local scan
lo = max(mp.mpf(0), bestx - mp.mpf(3)/N); hi = min(mp.mpf(1), bestx + mp.mpf(3)/N)
for _ in range(60):
    m1 = lo + (hi-lo)*mp.mpf('0.381966'); m2 = lo + (hi-lo)*mp.mpf('0.618034')
    if abs(p(m1)-f(m1)) > abs(p(m2)-f(m2)): hi = m2
    else: lo = m1
E_paper = max(abs(p(lo)-f(lo)), abs(p(hi)-f(hi)), abs(p((lo+hi)/2)-f((lo+hi)/2)))
bestx = (lo+hi)/2

kappa_paper = p(mp.mpf(1))
f1 = f(mp.mpf(1))  # = 1/2

# TRIVIAL UPPER BOUND: |p(1)-f(1)| <= E_paper  =>  kappa = p(1) <= f(1) + E_paper
kappa_ub = f1 + E_paper

kappa_req = mp.mpf('0.521015891482995')

print("E_paper (max |p-f| on [0,1]) =", mp.nstr(E_paper, 18), " at x =", mp.nstr(bestx, 6))
print("  (tick-266 repro-run.txt had 0.00408988417329 at x=0.97819)")
print("kappa_paper = p(1)          =", mp.nstr(kappa_paper, 18), " (= 433/859 =", mp.nstr(mp.mpf(433)/859,18), ")")
print("f(1) = 1/2                  =", mp.nstr(f1, 18))
print("|kappa_paper - f(1)|        =", mp.nstr(abs(kappa_paper - f1), 18), " (<= E_paper:", mp.nstr(abs(kappa_paper-f1) <= E_paper,1), ")")
print()
print("TRIVIAL UPPER BOUND on kappa under ||p-f||_inf <= E_paper:")
print("  kappa <= f(1) + E_paper   =", mp.nstr(kappa_ub, 18))
print("  kappa_required            =", mp.nstr(kappa_req, 18))
print("  kappa_ub < kappa_required  =", mp.nstr(kappa_ub < kappa_req, 1))
print()
print("VERDICT: to reach kappa > 0.521015891482995 need |p(1)-f(1)| >=", mp.nstr(kappa_req - f1, 18))
print("  which is", mp.nstr((kappa_req - f1)/E_paper, 4), "x the paper's E_paper =", mp.nstr(E_paper, 12))
