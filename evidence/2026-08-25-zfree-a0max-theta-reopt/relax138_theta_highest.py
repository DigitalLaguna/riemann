#!/usr/bin/env python3
"""Close the upper-end scope gap for claim #46: confirm A0_max(theta) <
A0_max* = 0.396708119308 on (1.5077, pi/2), which the tick-215 upward scan
(grid ended at 1.5077) did not cover.
F-test (pre-registered): DEAD if max_{theta in (1.5077, pi/2)} A0_max >= 0.396708119308.
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
print("=== A0_max(theta) scan on (1.5077, pi/2) ===")
best=mp.mpf('0'); bestth=None
for th in ['1.51','1.52','1.53','1.54','1.55','1.555','1.56','1.565','1.568','1.569','1.57']:
    t=mp.mpf(th); a=A0_max(t)
    print(f"  theta={th:>7}  A0_max={mp.nstr(a,12)}  A0_g={mp.nstr(A0_g(t),12)}  A0_tan={mp.nstr(A0_tan(t),10)}")
    if a>best: best=a; bestth=th
print(f"\nmax on (1.5077, pi/2): A0_max={mp.nstr(best,12)} at theta={bestth}")
print(f"target (theta*=0.0572) = {mp.nstr(target,12)}")
print(f"max < target? {best<target}")
