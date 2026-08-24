import mpmath as mp
mp.mp.dps = 60

# ---- exact inputs from the paper (verbatim) ----
K   = mp.mpf(16)                 # line 535
T0  = mp.mpf(10)**10             # line 532
H   = mp.mpf(3)*mp.mpf(10)**12   # line 163
xH  = mp.log(H)                  # log H
xKT = mp.log(K*H + T0)           # log(KH+T0)
w0  = mp.mpf('5.672787598')      # line 530

def eta0(A0): return A0/xH
def sig0(A0): return 1 - A0/xKT
def mu0(A0):  return (1-sig0(A0))/eta0(A0) - mp.mpf('1e-10')

A0_cur = 1/mp.mpf('4.896')       # true A0 per claim #41
A0_target = mp.mpf('0.420483467794')  # claim #40 reopt A_final

print("=== baseline (A0 = 1/4.896, claim #41) ===")
print(f"logH = {mp.nstr(xH,12)}  log(KH+T0) = {mp.nstr(xKT,12)}")
print(f"eta0 = {mp.nstr(eta0(A0_cur),10)}  sigma0 = {mp.nstr(sig0(A0_cur),10)}  mu0 = {mp.nstr(mu0(A0_cur),10)}")
print(f"(2*sigma0-1)/eta0 = {mp.nstr((2*sig0(A0_cur)-1)/eta0(A0_cur),10)}  (paper: > 138)")

print("\n=== Lemma 5 constraint: (2*sigma0-1)/eta0 > 138 ===")
# (2*sig0-1)/eta0 = (1 - 2*A0/xKT)/(A0/xH) = xH/A0 - 2*xH/xKT
# binds when xH/A0 - 2*xH/xKT = 138  =>  A0 = xH/(138 + 2*xH/xKT)
A0_L5 = xH/(mp.mpf(138) + 2*xH/xKT)
print(f"A0 at which (2*sigma0-1)/eta0 = 138:  A0 = {mp.nstr(A0_L5,12)}  (1/A0 = {mp.nstr(1/A0_L5,10)})")
print(f"  current A0 = {mp.nstr(A0_cur,10)}  ->  margin = {mp.nstr(A0_L5-A0_cur,8)}  ({mp.nstr((A0_L5/A0_cur-1)*100,4)}%)")
print(f"  target A0  = {mp.nstr(A0_target,10)}  ->  Lemma 5 holds? {A0_target < A0_L5}")

print("\n=== Lemma 14 constraint: x1 = (2*sigma0-1)*m - mu0*eta0 > 0 (m=1) ===")
# binds when (2*sig0-1) = mu0*eta0  =>  1 - 2*A0/xKT = (xH/xKT - 1e-10)*(A0/xH)
# approx: 1 - 2*A0/xKT = A0/xKT  =>  A0 = xKT/3
A0_L14 = xKT/3
print(f"A0 at which x1(m=1) = 0 (approx):  A0 = {mp.nstr(A0_L14,12)}  (1/A0 = {mp.nstr(1/A0_L14,10)})")
print(f"  target A0 = {mp.nstr(A0_target,10)}  ->  Lemma 14 x1 holds? {A0_target < A0_L14}")

print("\n=== Lemma 13 constraint: 51*eta0^2/H^2 < 5e-13 (approx) ===")
# from |E| bound: 51*(H/eta0)^-3 < 1e-12*eta0/2  =>  51*eta0^2/H^2 < 5e-13
# eta0 = A0/xH  =>  51*(A0/xH)^2/H^2 < 5e-13  =>  A0 < sqrt(5e-13*H^2/51)*xH
A0_L13 = mp.sqrt(mp.mpf('5e-13')*H**2/mp.mpf(51))*xH
print(f"A0 at which Lemma 13 binds (approx):  A0 = {mp.nstr(A0_L13,12)}")
print(f"  target A0 = {mp.nstr(A0_target,10)}  ->  Lemma 13 holds? {A0_target < A0_L13}")

print("\n=== VERDICT ===")
A0_max = min(A0_L5, A0_L14, A0_L13, A0_target)
binding = 'Lemma 5' if A0_max==A0_L5 else ('Lemma 14' if A0_max==A0_L14 else ('Lemma 13' if A0_max==A0_L13 else 'final line'))
print(f"A0_max = {mp.nstr(A0_max,12)}  (binding: {binding})")
print(f"  current A0 = {mp.nstr(A0_cur,10)}  ->  improvement? {A0_max > A0_cur}")
print(f"  unconditional constant = 1/A0_max = {mp.nstr(1/A0_max,10)}  (vs current 4.896)")
if A0_max >= A0_target:
    print(f"  A0_max >= target 0.4204835 -> FULL reopt payoff: constant = 2.3782")
elif A0_max > A0_cur:
    print(f"  A0_cur < A0_max < target -> PARTIAL win: constant = {mp.nstr(1/A0_max,10)}")
else:
    print(f"  A0_max <= A0_cur -> NO improvement")
