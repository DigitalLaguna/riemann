import mpmath as mp
mp.mp.dps = 50
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

A0_rel = mp.mpf('0.324204954225')   # from relax138_audit.py (nu=r=L)
Lval = L(A0_rel)
print(f"A0={mp.nstr(A0_rel,10)}  L={mp.nstr(Lval,10)}  C(L,L)={mp.nstr(C(Lval,Lval),10)}")
print("\n2D scan: min C(nu,r) over nu,r in [tanθ, L]  (tanθ=%.4f)" % float(mp.tan(theta)))
best = (None, None, None)
N = 40
for i in range(N+1):
    nu = mp.tan(theta)*1.0001 + (Lval - mp.tan(theta))*i/N
    for j in range(N+1):
        r  = mp.tan(theta)*1.0001 + (Lval - mp.tan(theta))*j/N
        cv = C(nu, r)
        if best[2] is None or cv < best[2]:
            best = (nu, r, cv)
print(f"  grid min: nu={mp.nstr(best[0],8)} r={mp.nstr(best[1],8)} C={mp.nstr(best[2],10)}")
print(f"  C(L,L)   = {mp.nstr(C(Lval,Lval),10)}   (ratio gridmin/C(L,L) = {mp.nstr(best[2]/C(Lval,Lval),6)})")
# also check the boundary nu=L (best nu for any r)
best2 = (None, None)
for j in range(2001):
    r = mp.tan(theta)*1.0001 + (Lval - mp.tan(theta))*j/2000
    cv = C(Lval, r)
    if best2[2 if False else 0] is None or cv < best2[1]:
        best2 = (r, cv)
print(f"  min over r of C(L,r): r={mp.nstr(best2[0],8)} C={mp.nstr(best2[1],10)}")
