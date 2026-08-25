#!/usr/bin/env python3
"""Close the scope gap for claim #46: the claim states A0_max is maximized
over (0,pi/2) at theta*=0.057151961, but the tick-215 scan covered only
[0.05, 1.56]. This scans (0, 0.05] to confirm A0_max(theta) < A0_max* there.
F-test (pre-registered): DEAD if max_{theta in (0,0.05]} A0_max(theta) >=
0.396708119308 (i.e. the true maximizer is below 0.05, not at 0.0572).
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

target=mp.mpf('0.396708119308')
print("=== C(L,L;th)/w0(th) at FIXED L=70.6 (theta->0 limit probe) ===")
Lfix=mp.mpf('70.6')
for th in ['0.05','0.01','0.001','0.0001']:
    t=mp.mpf(th)
    print(f"  th={th}  C/w0={mp.nstr(C(Lfix,Lfix,t)/w0(t),8)}")
print("\n=== A0_max(theta) scan on (0, 0.05] ===")
best=mp.mpf('0'); bestth=None
for th in ['0.0001','0.0005','0.001','0.002','0.003','0.005','0.0075','0.01',
           '0.015','0.02','0.025','0.03','0.035','0.04','0.045','0.05']:
    t=mp.mpf(th); a=A0_max(t)
    print(f"  theta={th:>8}  A0_max={mp.nstr(a,12)}  A0_g={mp.nstr(A0_g(t),12)}  A0_tan={mp.nstr(A0_tan(t),10)}")
    if a>best: best=a; bestth=th
print(f"\nmax on (0,0.05]: A0_max={mp.nstr(best,12)} at theta={bestth}")
print(f"target (theta*=0.0572) = {mp.nstr(target,12)}")
print(f"max < target? {best<target}")
