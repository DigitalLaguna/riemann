# verify_m0term.py — m=0-term theta constraint, full verification (claim #47)
# BTY-2026 (arXiv:2603.21490 v1) line 2210: m=0 Taylor bound asserted on
# [0, 2*theta*cot(theta)] -> theta >= theta_min. Functions identical to
# relax138_theta_verify.py (claim #46) — see diff in tick 219 log.
import mpmath as mp
mp.mp.dps = 60
T0=mp.mpf(10)**10; H=mp.mpf(3)*mp.mpf(10)**12; K=mp.mpf(16)
xH=mp.log(H); xKT=mp.log(K*H+T0); eps0=mp.mpf(1)/mp.mpf(2000)
def eta0(A0): return A0/xH
def sig0(A0): return 1-A0/xKT
def L(A0): return (2*sig0(A0)-1)/eta0(A0)
def w0(th): return mp.sec(th)**2*(th*mp.tan(th)+3*th/mp.tan(th)-3)
def C(nu,r,th):
    c0=1/mp.sin(th)*mp.sec(th)**2
    c1=(th-mp.sin(th)*mp.cos(th))*mp.tan(th)**4
    c2=mp.tan(th)**3*mp.sin(th)**2
    c3=(th-mp.sin(th)*mp.cos(th))*mp.tan(th)**2
    num=c2*(r+1)**2*(mp.e**(-2*nu*th)/mp.tan(th)+1)+c1*r+c3*r**3
    return c0*r*num/(r**2-mp.tan(th)**2)**2
def g(A0,th): return eta0(A0)**2*C(L(A0),L(A0),th)/(eps0*(2*sig0(A0)-1)*w0(th))
def ratio2(A0,th): return eta0(A0)**2*C(138,138,th)/(eps0*(2*sig0(A0)-1)*w0(th))
def A0_tan(th): return xH/(mp.tan(th)+2*xH/xKT)
def bisect(f,lo,hi,n=170):
    for _ in range(n):
        mid=(lo+hi)/2
        if f(mid)<0: lo=mid
        else: hi=mid
    return (lo+hi)/2
def A0_g(th):
    if g(mp.mpf('0.001'),th)>1: return mp.mpf('0.001')
    if g(mp.mpf('10'),th)<1: return mp.mpf('10')
    return bisect(lambda A: g(A,th)-1, mp.mpf('0.001'), mp.mpf('10'))
def A0_r2(th):
    if ratio2(mp.mpf('0.001'),th)>1: return mp.mpf('0.001')
    if ratio2(mp.mpf('10'),th)<1: return mp.mpf('10')
    return bisect(lambda A: ratio2(A,th)-1, mp.mpf('0.001'), mp.mpf('10'))

# --- Part 1: x_max and theta_min from scratch ---
def R(x): return mp.e**x - (1 + x + x**2/2 + x**3/6)
xs=[mp.mpf(i)/1000 for i in range(5001)]
cross=next((x for x in xs if R(x)-x**4/18>0), None)
a,b=cross-mp.mpf(1)/1000,cross
for _ in range(80):
    m=(a+b)/2
    if R(m)-m**4/18>0: b=m
    else: a=m
x_max=(a+b)/2
f=lambda th: 2*th/mp.tan(th)-x_max
lo,hi=mp.mpf('0.1'),mp.mpf('1.5')
for _ in range(100):
    m=(lo+hi)/2
    if f(m)>0: lo=m
    else: hi=m
theta_min=(lo+hi)/2
print(f"V1 x_max = {mp.nstr(x_max,15)}  (hardcoded 1.31432746286474) match? {abs(x_max-mp.mpf('1.31432746286474'))<mp.mpf('1e-12')}")
print(f"V1 theta_min = {mp.nstr(theta_min,15)}  (hardcoded 0.980175494979204) match? {abs(theta_min-mp.mpf('0.980175494979204'))<mp.mpf('1e-12')}")
print(f"V1 2*theta_min*cot(theta_min) = {mp.nstr(2*theta_min/mp.tan(theta_min),15)}")

# --- Part 2: m=0 bound at theta_min (must HOLD) and at theta* #46 (must FAIL) ---
def maxviol(th,n=200001):
    bnd=2*th/mp.tan(th); mx=mp.mpf(-1); mx_x=mp.mpf(0)
    for i in range(n):
        x=bnd*i/(n-1)
        v=R(x)-x**4/18
        if v>mx: mx=v; mx_x=x
    return bnd,mx,mx_x
b1,m1,m1x=maxviol(theta_min)
b2,m2,m2x=maxviol(mp.mpf('0.057151961'))
print(f"V2 bound at theta_min: range [0,{mp.nstr(b1,12)}] max[R-x^4/18] = {mp.nstr(m1,12)} at x={mp.nstr(m1x,12)} -> {'HOLDS' if m1<=0 else 'FAILS'}")
print(f"V2 bound at theta* #46: range [0,{mp.nstr(b2,12)}] max[R-x^4/18] = {mp.nstr(m2,12)} at x={mp.nstr(m2x,12)} -> {'HOLDS' if m2<=0 else 'FAILS'}")

# --- Part 3: A0_max at theta_min under the 7-constraint set ---
th=theta_min
ag=A0_g(th); ar2=A0_r2(th); atan=A0_tan(th)
A0=min(atan,ag,ar2)
print(f"V3 at theta_min: A0_g={mp.nstr(ag,12)} A0_r2(C138 internal)={mp.nstr(ar2,12)} A0_tan={mp.nstr(atan,10)}")
print(f"V3 A0_max(theta_min) = {mp.nstr(A0,12)}  constant = {mp.nstr(1/A0,10)}")
# all 7 constraints at (A0, theta_min)
w0v=w0(th)
c1v=eta0(A0)**2*C(L(A0),L(A0),th)/(eps0*(2*sig0(A0)-1)*w0v)
lhs2=eta0(A0)**2*C(138,138,th); rhs2=eps0*(2*sig0(A0)-1)*w0v
rT=T0/eta0(A0)
lhs4=eta0(A0)**2*(C(-1,rT,th)+C(0,rT,th)); rhs4=mp.mpf('5.7')*T0
mu0=(1-sig0(A0))/eta0(A0)-mp.mpf('1e-10')
x1=(2*sig0(A0)-1)-mu0*eta0(A0)
lhs7=51*eta0(A0)**2/H**2
print(f"[1] g(A0,theta_min) = {mp.nstr(c1v,10)} holds? {c1v<=1+mp.mpf('1e-9')}")
print(f"[2] C(138,138) internal: LHS={mp.nstr(lhs2,10)} RHS={mp.nstr(rhs2,10)} ratio={mp.nstr(lhs2/rhs2,8)} holds? {lhs2<rhs2}")
print(f"[3] B(y)>0: A0-independent (verified #44)  holds? True")
print(f"[4] eq22 W0-term: LHS={mp.nstr(lhs4,10)} RHS={mp.nstr(rhs4,10)} ratio={mp.nstr(lhs4/rhs4,6)} holds? {lhs4<rhs4}")
print(f"[5] Lemma6 A0>1/6: {mp.nstr(A0,10)} > 0.16667? {A0>1/mp.mpf(6)}")
print(f"[6] Lemma14 x1(m=1) = {mp.nstr(x1,10)} > 0? {x1>0}")
print(f"[7] Lemma13: 51*eta0^2/H^2 = {mp.nstr(lhs7,4)} < 5e-13? {lhs7<mp.mpf('5e-13')}")
allhold=(c1v<=1+mp.mpf('1e-9')) and (lhs2<rhs2) and (lhs4<rhs4) and (A0>1/mp.mpf(6)) and (x1>0) and (lhs7<mp.mpf('5e-13'))
print(f"V3 all 7 constraints hold at (A0_max(theta_min), theta_min): {allhold}")

# --- Part 4: scan A0_max_full(theta) on [theta_min, pi/2) ---
def A0_max_full(th):
    return min(A0_tan(th), A0_g(th), A0_r2(th))
N=2001
lo,hi=theta_min, mp.pi/2-mp.mpf('1e-4')
mx=mp.mpf(-1); mx_th=lo
for i in range(N):
    th_i=lo+(hi-lo)*i/(N-1)
    v=A0_max_full(th_i)
    if v>mx: mx=v; mx_th=th_i
print(f"V4 scan [theta_min, pi/2) N={N}: max A0_max_full = {mp.nstr(mx,12)} at theta = {mp.nstr(mx_th,12)}")
print(f"V4 max at left endpoint theta_min? {abs(mx_th-theta_min)<mp.mpf('1e-3')}  value matches A0_max(theta_min)? {abs(mx-A0)<mp.mpf('1e-6')}")
print(f"V4 A0_r2(theta_min) > A0_g(theta_min) (C138 non-binding at boundary)? {ar2>ag}")

# --- Part 5: bracket + verdict ---
bracket=(A0>mp.mpf('0.324204954225')) and (A0<mp.mpf('0.396708119308'))
print(f"V5 bracket 0.324204954225 < A0_max < 0.396708119308: {bracket}")
ok=all([abs(x_max-mp.mpf('1.31432746286474'))<mp.mpf('1e-12'),
        abs(theta_min-mp.mpf('0.980175494979204'))<mp.mpf('1e-12'),
        m1<=0, m2>0, allhold,
        abs(mx_th-theta_min)<mp.mpf('1e-3'), abs(mx-A0)<mp.mpf('1e-6'), bracket])
print(f"\nVERDICT: m=0-term constraint theta >= theta_min = {mp.nstr(theta_min,15)}; A0_max = {mp.nstr(A0,12)} (constant {mp.nstr(1/A0,10)}) at theta = theta_min")
print(f"  #45 (theta=1.1338): 0.324204954225 (3.084468596)   #46 infeasible: 0.396708119308 (2.520744979)   target #40: 0.420483467794 (2.378214785)")
print(f"OVERALL: {'ALL PASS' if ok else 'SEE ABOVE'}")
