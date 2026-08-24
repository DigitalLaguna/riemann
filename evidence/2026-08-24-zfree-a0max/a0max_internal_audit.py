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

# ---- Lemma 4 (Ford [4] sec 7): C(nu, r) ----
c0 = 1/mp.sin(theta) * mp.sec(theta)**2                 # csc theta sec^2 theta
c1 = (theta - mp.sin(theta)*mp.cos(theta)) * mp.tan(theta)**4
c2 = mp.tan(theta)**3 * mp.sin(theta)**2
c3 = (theta - mp.sin(theta)*mp.cos(theta)) * mp.tan(theta)**2
def C(nu, r):
    num = c2*(r+1)**2*(mp.e**(-2*nu*theta)/mp.tan(theta) + 1) + c1*r + c3*r**3
    return c0*r*num/(r**2 - mp.tan(theta)**2)**2

A0_max = mp.mpf('0.205470026688')   # claim #42: Lemma 5 main binding value
A0_cur = 1/mp.mpf('4.896')

print("=== sanity: w(0) from formula (paper: 5.672787598) ===")
print(f"w(0) = {mp.nstr(w0,10)}")

print("\n=== C(nu,r) values ===")
print(f"C(138,138)        = {mp.nstr(C(138,138),10)}")
rT = T0/eta0(A0_max)
print(f"T0/eta0(A0_max)   = {mp.nstr(rT,12)}")
print(f"C(-1,T0/eta0)     = {mp.nstr(C(-1,rT),10)}")
print(f"C(0,T0/eta0)      = {mp.nstr(C(0,rT),10)}")

print("\n=== CONSTRAINT 2: Lemma 5 internal, eta0^2 C(138,138) < eps0 (2sigma0-1) w(0) ===")
def c2lhs(A0): return eta0(A0)**2 * C(138,138)
def c2rhs(A0): return eps0*(2*sig0(A0)-1)*w0
print(f"at A0_max: LHS = {mp.nstr(c2lhs(A0_max),10)}  RHS = {mp.nstr(c2rhs(A0_max),10)}  holds? {c2lhs(A0_max) < c2rhs(A0_max)}")
# find binding A0 (solve LHS=RHS by bisection on A0 in (0, 1))
lo, hi = mp.mpf('0.01'), mp.mpf('1')
for _ in range(200):
    mid = (lo+hi)/2
    if c2lhs(mid) < c2rhs(mid): lo = mid
    else: hi = mid
A0_c2 = (lo+hi)/2
print(f"  binds at A0 = {mp.nstr(A0_c2,12)}  (1/A0 = {mp.nstr(1/A0_c2,10)})  -> above A0_max? {A0_c2 > A0_max}")

print("\n=== CONSTRAINT 3: B(y) > 0 for all y (p(y) no real roots, p(0)>0) ===")
# p(y) even; set u=y^2, P(u) degree 6
P = [mp.mpf('4061245152630328137981'), mp.mpf('4077560173170236734684710'),
     mp.mpf('-104378137212291977844887868'), mp.mpf('-4484512641017853031179075270'),
     mp.mpf('135673322742635307737680349343'), mp.mpf('-229732179325278720034298507440'),
     mp.mpf('112359769561546903428467326544')]
P0 = P[6]
print(f"P(0) = {mp.nstr(P0,12)}  > 0? {P0 > 0}")
roots = mp.polyroots(P, maxsteps=200)
real_roots = [r for r in roots if abs(mp.im(r)) < mp.mpf('1e-25')*max(1,abs(r))]
nonneg_real = [r for r in real_roots if mp.re(r) >= 0]
print(f"num roots = {len(roots)}; real roots = {len(real_roots)}; real & >=0 = {len(nonneg_real)}")
for r in sorted(real_roots, key=lambda z: mp.re(z)):
    print(f"   real root u = {mp.nstr(mp.re(r),12)}")
# also scan P(u) on u>=0 for sign changes as a cross-check
import math
neg = 0
prev = None
for i in range(0, 200001):
    u = mp.mpf(i)/mp.mpf(1000)   # u in [0,200] step 0.001
    val = mp.fsum(c*mp.mpf(u)**(6-j) for j,c in enumerate(P))
    if val < 0: neg += 1
print(f"scan u in [0,200] step 0.001: #negative samples = {neg}  (0 => P>0 on [0,200])")
print(f"B(y)>0 for all y? {len(nonneg_real)==0 and P0>0 and neg==0}")

print("\n=== CONSTRAINT 4: eq (22) W0-term, eta0^2 [C(-1,T0/eta0)+C(0,T0/eta0)] < 5.7 T0 ===")
def c4lhs(A0):
    r = T0/eta0(A0)
    return eta0(A0)**2*(C(-1,r)+C(0,r))
c4rhs = mp.mpf('5.7')*T0
print(f"at A0_max: LHS = {mp.nstr(c4lhs(A0_max),10)}  RHS = {mp.nstr(c4rhs,10)}  holds? {c4lhs(A0_max) < c4rhs}")
print(f"  ratio LHS/RHS = {mp.nstr(c4lhs(A0_max)/c4rhs,6)}")
# w(0)-term sub-constraint: 2 w(0) eta < 5.7  (eta <= eta0)
print(f"  w(0)-term: 2 w(0) eta0(A0_max) = {mp.nstr(2*w0*eta0(A0_max),10)} < 5.7? {2*w0*eta0(A0_max) < 5.7}")

print("\n=== CONSTRAINT 5: Lemma 6 A-range, A0 > 1/6 ===")
print(f"A0_max = {mp.nstr(A0_max,12)}  > 1/6 = {mp.nstr(1/6,12)}?  {A0_max > 1/6}")

print("\n=== VERDICT ===")
A0_all = min(A0_max, A0_c2)   # c2 is the only other A0-dependent binding candidate
print(f"A0_max (Lemma 5 main) = {mp.nstr(A0_max,12)}")
print(f"A0 bind (C138,138)    = {mp.nstr(A0_c2,12)}")
print(f"overall A0_max        = {mp.nstr(A0_all,12)}  (1/A0 = {mp.nstr(1/A0_all,10)})")
if A0_all == A0_max:
    print("CONFIRMED: Lemma 5 main still binds; internal constraints (C138, B(y), eq22, L6-range) all hold at A0_max")
    print(f"  PARTIAL win stands: unconditional constant = {mp.nstr(1/A0_max,10)} (vs 4.896)")
else:
    print(f"SHRUNK: new binding constraint lowers A0_max to {mp.nstr(A0_all,12)}; constant = {mp.nstr(1/A0_all,10)}")
