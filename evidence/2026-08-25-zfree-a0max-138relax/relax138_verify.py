import mpmath as mp
mp.mp.dps = 60
theta = mp.mpf('1.1338')
T0    = mp.mpf(10)**10
H     = mp.mpf(3)*mp.mpf(10)**12
K     = mp.mpf(16)
xH    = mp.log(H); xKT = mp.log(K*H + T0)
eps0  = mp.mpf(1)/mp.mpf(2000)
w0    = mp.sec(theta)**2*(theta*mp.tan(theta) + 3*theta/mp.tan(theta) - 3)
def eta0(A0): return A0/xH
def sig0(A0): return 1 - A0/xKT
def L(A0):    return (2*sig0(A0)-1)/eta0(A0)
c0 = 1/mp.sin(theta) * mp.sec(theta)**2
c1 = (theta - mp.sin(theta)*mp.cos(theta)) * mp.tan(theta)**4
c2 = mp.tan(theta)**3 * mp.sin(theta)**2
c3 = (theta - mp.sin(theta)*mp.cos(theta)) * mp.tan(theta)**2
def C(nu, r):
    num = c2*(r+1)**2*(mp.e**(-2*nu*theta)/mp.tan(theta) + 1) + c1*r + c3*r**3
    return c0*r*num/(r**2 - mp.tan(theta)**2)**2

A0_new = mp.mpf('0.324204954225')   # relaxed A0_max (g=1)
A0_cur = 1/mp.mpf('4.896')
A0_old = mp.mpf('0.205470026688')   # paper 138 wall (claim #42)

print(f"=== VERIFY all constraints at A0_new = {mp.nstr(A0_new,12)} ===")
print(f"  (L = {mp.nstr(L(A0_new),10)}, eta0 = {mp.nstr(eta0(A0_new),10)}, sigma0 = {mp.nstr(sig0(A0_new),10)})")

# 1. relaxed Lemma 5 main: g(A0) < 1  (this is the binding one, g=1 at A0_new)
g = eta0(A0_new)**2 * C(L(A0_new), L(A0_new)) / (eps0*(2*sig0(A0_new)-1)*w0)
print(f"[1] relaxed Lemma5 g(A0_new) = {mp.nstr(g,10)}  (binding: g=1 by construction)")

# 2. old C(138,138) internal (from #44): eta0^2 C(138,138) < eps0(2sigma0-1)w0
lhs2 = eta0(A0_new)**2 * C(138,138); rhs2 = eps0*(2*sig0(A0_new)-1)*w0
print(f"[2] C(138,138) internal: LHS={mp.nstr(lhs2,10)} RHS={mp.nstr(rhs2,10)} holds? {lhs2<rhs2}")

# 3. B(y)>0: independent of A0 (verified in #44: p has no real roots, p(0)>0)
print(f"[3] B(y)>0: A0-independent (verified #44)  holds? True")

# 4. eq(22) W0-term: eta0^2 [C(-1,T0/eta0)+C(0,T0/eta0)] < 5.7 T0
rT = T0/eta0(A0_new)
lhs4 = eta0(A0_new)**2 * (C(-1,rT)+C(0,rT)); rhs4 = mp.mpf('5.7')*T0
print(f"[4] eq22 W0-term: LHS={mp.nstr(lhs4,10)} RHS={mp.nstr(rhs4,10)} ratio={mp.nstr(lhs4/rhs4,4)} holds? {lhs4<rhs4}")

# 5. Lemma 6 A-range: A0 > 1/6
print(f"[5] Lemma6 A0>1/6: {mp.nstr(A0_new,10)} > 0.16667? {A0_new > 1/mp.mpf(6)}")

# 6. Lemma 14 x1 (m=1): (2sigma0-1) > mu0*eta0, mu0=(1-sigma0)/eta0 - 1e-10
mu0 = (1-sig0(A0_new))/eta0(A0_new) - mp.mpf('1e-10')
x1 = (2*sig0(A0_new)-1) - mu0*eta0(A0_new)
print(f"[6] Lemma14 x1(m=1) = {mp.nstr(x1,10)} > 0? {x1>0}")

# 7. Lemma 13: 51*eta0^2/H^2 < 5e-13
lhs7 = 51*eta0(A0_new)**2/H**2
print(f"[7] Lemma13: 51*eta0^2/H^2 = {mp.nstr(lhs7,4)} < 5e-13? {lhs7 < mp.mpf('5e-13')}")

print("\n=== RESULT ===")
allhold = (lhs2<rhs2) and (lhs4<rhs4) and (A0_new>1/mp.mpf(6)) and (x1>0) and (lhs7<mp.mpf('5e-13'))
print(f"all non-binding constraints hold at A0_new? {allhold}")
print(f"NEW A0_max = {mp.nstr(A0_new,12)}  ->  constant = 1/A0_max = {mp.nstr(1/A0_new,10)}")
print(f"  old (paper 138 wall, #42): 1/{mp.nstr(A0_old,10)} = {mp.nstr(1/A0_old,10)}")
print(f"  target (full reopt, #40):  1/0.420483467794 = {mp.nstr(1/mp.mpf('0.420483467794'),10)}")
