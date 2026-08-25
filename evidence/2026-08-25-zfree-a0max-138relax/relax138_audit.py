import mpmath as mp
mp.mp.dps = 60

# ---- exact inputs from BTY-2026 (arXiv:2603.21490), verbatim ----
theta = mp.mpf('1.1338')          # Lemma 4 para: "fix theta = 1.1338"
T0    = mp.mpf(10)**10            # line 532
H     = mp.mpf(3)*mp.mpf(10)**12  # line 163
K     = mp.mpf(16)                # line 535
xH    = mp.log(H)
xKT   = mp.log(K*H + T0)
eps0  = mp.mpf(1)/mp.mpf(2000)    # proof of Lemma 5: "with eps0 = 1/2000"
w0    = mp.sec(theta)**2*(theta*mp.tan(theta) + 3*theta/mp.tan(theta) - 3)  # = 5.672787598...

def eta0(A0): return A0/xH
def sig0(A0): return 1 - A0/xKT
def L(A0):    return (2*sig0(A0)-1)/eta0(A0)   # = xH/A0 - 2*xH/xKT

# ---- Lemma 4 (Ford [4] sec 7): C(nu, r) ----
c0 = 1/mp.sin(theta) * mp.sec(theta)**2                 # csc theta sec^2 theta
c1 = (theta - mp.sin(theta)*mp.cos(theta)) * mp.tan(theta)**4
c2 = mp.tan(theta)**3 * mp.sin(theta)**2
c3 = (theta - mp.sin(theta)*mp.cos(theta)) * mp.tan(theta)**2
def C(nu, r):
    num = c2*(r+1)**2*(mp.e**(-2*nu*theta)/mp.tan(theta) + 1) + c1*r + c3*r**3
    return c0*r*num/(r**2 - mp.tan(theta)**2)**2

A0_cur    = 1/mp.mpf('4.896')
A0_max    = mp.mpf('0.205470026688')   # claim #42: Lemma 5 main binding value
A0_target = mp.mpf('0.420483467794')   # claim #40 reopt A_final

print("=== sanity ===")
print(f"w(0) = {mp.nstr(w0,10)}  (paper: 5.672787598)")
print(f"C(138,138) = {mp.nstr(C(138,138),10)}  (#44: 21.57083788)")
print(f"L(A0_cur)  = {mp.nstr(L(A0_cur),10)}  (#42: 138.8363222)")

print("\n=== C(L,L) as L decreases below 138 ===")
for Lv in [138, 130, 100, 50, 20, 10, 5, 3, 2.5]:
    print(f"  L={Lv:<6} C(L,L) = {mp.nstr(C(Lv,Lv),10)}")

print("\n=== relaxed constraint g(A0) = eta0^2 C(L,L) / [eps0 (2sigma0-1) w0] < 1 ===")
def g(A0):
    return eta0(A0)**2 * C(L(A0), L(A0)) / (eps0*(2*sig0(A0)-1)*w0)

for A0v in [A0_cur, A0_max, mp.mpf('0.25'), mp.mpf('0.30'), mp.mpf('0.326015468165'),
            mp.mpf('0.35'), mp.mpf('0.40'), A0_target, mp.mpf('0.45'), mp.mpf('0.5')]:
    print(f"  A0={mp.nstr(A0v,10):<14} L={mp.nstr(L(A0v),10):<14} g={mp.nstr(g(A0v),10)}  g<1? {g(A0v)<1}")

# bisection for the max A0 with g(A0)=1, on [A0_max, 10]
lo, hi = A0_max, mp.mpf(10)
if g(lo) > 1:
    print("\n  NOTE: g(A0_max) > 1 -> relaxed constraint already fails at A0_max")
    A0_rel = None
elif g(hi) < 1:
    A0_rel = hi
    print("\n  NOTE: g(10) < 1 -> constraint holds up to A0=10 (not binding here)")
else:
    for _ in range(200):
        mid = (lo+hi)/2
        if g(mid) < 1: lo = mid
        else: hi = mid
    A0_rel = lo

print("\n=== VERDICT ===")
if A0_rel is None:
    print("A0_relaxed = None (g(A0_max)>1)  -> DEAD (relaxation buys nothing)")
else:
    print(f"A0_relaxed = {mp.nstr(A0_rel,12)}  (1/A0_relaxed = {mp.nstr(1/A0_rel,10)})")
    print(f"  A0_max (paper 138 wall) = {mp.nstr(A0_max,12)}")
    print(f"  A0_target (full reopt)  = {mp.nstr(A0_target,12)}")
    if A0_rel >= A0_target:
        print("  A0_relaxed >= target -> FULL reopt payoff: constant = 2.3782")
    elif A0_rel > A0_max:
        print(f"  A0_max < A0_relaxed < target -> PARTIAL win: constant = {mp.nstr(1/A0_rel,10)}")
    else:
        print("  A0_relaxed <= A0_max -> DEAD (relaxation buys nothing)")
