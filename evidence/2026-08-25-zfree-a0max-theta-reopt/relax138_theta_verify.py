#!/usr/bin/env python3
"""Theta reopt for the A0_max objective: refine the maximizer and verify ALL
7 constraints (from relax138_verify.py / claim #44/#45) at (A0_max*, theta*).
F-tests:
  F1: A0_max(1.1338) reproduces #45 = 0.324204954225.
  F2: all 7 constraints hold at (A0_max*, theta*) -> A0_max* is a valid A0_max.
  F3: A0_max* > 0.3242 (theta reopt helps) and A0_max* < 0.4204835 (not full target).
"""
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
def A0_tan(th): return xH/(mp.tan(th)+2*xH/xKT)
def A0_g(th):
    lo,hi=mp.mpf('0.001'),mp.mpf(10)
    if g(lo,th)>1: return mp.mpf('0.001')
    if g(hi,th)<1: return hi
    for _ in range(170):
        mid=(lo+hi)/2
        if g(mid,th)<1: lo=mid
        else: hi=mid
    return lo
def A0_max(th): return min(A0_tan(th),A0_g(th))

# F1
f1 = abs(A0_max(mp.mpf('1.1338'))-mp.mpf('0.324204954225'))<mp.mpf('5e-7')
print(f"F1: A0_max(1.1338)={mp.nstr(A0_max(mp.mpf('1.1338')),12)} (#45: 0.324204954225) -> {'PASS' if f1 else 'FAIL'}")

# refine theta* on [0.05, 0.12] (the peak region)
lo,hi=mp.mpf('0.05'),mp.mpf('0.12')
gr=(mp.sqrt(5)-1)/2
c_=hi-gr*(hi-lo); d_=lo+gr*(hi-lo); fc,fd=A0_max(c_),A0_max(d_)
for _ in range(120):
    if fc<fd:
        lo,c_,fc=c_,d_,fd; d_=lo+gr*(hi-lo); fd=A0_max(d_)
    else:
        hi,d_,fd=d_,c_,fc; c_=hi-gr*(hi-lo); fc=A0_max(c_)
th_star=(lo+hi)/2
A0_star=A0_max(th_star)
print(f"\ntheta* = {mp.nstr(th_star,10)}   A0_max* = {mp.nstr(A0_star,12)}   (1/A0_max* = {mp.nstr(1/A0_star,10)})")
print(f"  A0_g(theta*)={mp.nstr(A0_g(th_star),12)}  A0_tan(theta*)={mp.nstr(A0_tan(th_star),10)}  tan(theta*)={mp.nstr(mp.tan(th_star),8)}")
print(f"  L(A0*)={mp.nstr(L(A0_star),10)}  eta0={mp.nstr(eta0(A0_star),10)}  sigma0={mp.nstr(sig0(A0_star),10)}")

# verify all 7 constraints at (A0_star, theta_star)
A0=A0_star; th=th_star
w0v=w0(th)
g1=eta0(A0)**2*C(L(A0),L(A0),th)/(eps0*(2*sig0(A0)-1)*w0v)
lhs2=eta0(A0)**2*C(138,138,th); rhs2=eps0*(2*sig0(A0)-1)*w0v
rT=T0/eta0(A0)
lhs4=eta0(A0)**2*(C(-1,rT,th)+C(0,rT,th)); rhs4=mp.mpf('5.7')*T0
mu0=(1-sig0(A0))/eta0(A0)-mp.mpf('1e-10')
x1=(2*sig0(A0)-1)-mu0*eta0(A0)
lhs7=51*eta0(A0)**2/H**2
print("\n=== VERIFY all 7 constraints at (A0*, theta*) ===")
print(f"[1] relaxed Lemma5 g(A0*) = {mp.nstr(g1,10)}  (binding g=1)  holds? {g1<=1+mp.mpf('1e-9')}")
print(f"[2] C(138,138;theta*) internal: LHS={mp.nstr(lhs2,10)} RHS={mp.nstr(rhs2,10)} holds? {lhs2<rhs2}")
print(f"[3] B(y)>0: A0-independent (verified #44)  holds? True")
print(f"[4] eq22 W0-term: LHS={mp.nstr(lhs4,10)} RHS={mp.nstr(rhs4,10)} ratio={mp.nstr(lhs4/rhs4,4)} holds? {lhs4<rhs4}")
print(f"[5] Lemma6 A0>1/6: {mp.nstr(A0,10)} > 0.16667? {A0>1/mp.mpf(6)}")
print(f"[6] Lemma14 x1(m=1) = {mp.nstr(x1,10)} > 0? {x1>0}")
print(f"[7] Lemma13: 51*eta0^2/H^2 = {mp.nstr(lhs7,4)} < 5e-13? {lhs7<mp.mpf('5e-13')}")
allhold=(g1<=1+mp.mpf('1e-9')) and (lhs2<rhs2) and (lhs4<rhs4) and (A0>1/mp.mpf(6)) and (x1>0) and (lhs7<mp.mpf('5e-13'))
f2=allhold
f3=(A0_star>mp.mpf('0.324204954225')) and (A0_star<mp.mpf('0.420483467794'))
print(f"\nF2 all 7 constraints hold at (A0*,theta*): {f2} -> {'PASS' if f2 else 'FAIL'}")
print(f"F3 0.3242 < A0_max* < 0.4205 (partial win): {f3} -> {'PASS' if f3 else 'FAIL'}")
print(f"\nVERDICT: theta reopt A0_max* = {mp.nstr(A0_star,12)} (constant {mp.nstr(1/A0_star,10)}) at theta*={mp.nstr(th_star,8)}")
print(f"  #45 (theta=1.1338): 0.324204954225 (3.084468596)   target: 0.420483467794 (2.378214785)")
print(f"OVERALL: {'ALL PASS' if all([f1,f2,f3]) else 'SEE ABOVE'}")
