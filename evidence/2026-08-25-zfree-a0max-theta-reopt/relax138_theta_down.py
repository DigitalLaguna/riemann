#!/usr/bin/env python3
"""Downward theta scan: is theta=1.1338 the GLOBAL A0_max maximizer, or only
the max on [1.1338, 1.56]? Scan theta in [0.5, 1.1338].
F-test: if max_{theta in [0.5,1.1338]} A0_max(theta) <= 0.324204954225, then
theta=1.1338 is the global maximizer and theta reopt is a DEAD END for the wall.
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
    lo,hi=mp.mpf('0.01'),mp.mpf(10)
    if g(lo,th)>1: return mp.mpf('0.01')
    if g(hi,th)<1: return hi
    for _ in range(150):
        mid=(lo+hi)/2
        if g(mid,th)<1: lo=mid
        else: hi=mid
    return lo
def A0_max(th): return min(A0_tan(th),A0_g(th))
print("theta      A0_max       A0_g         A0_tan       w0           C(L,L)")
best_th,best_A0=None,mp.mpf('-1')
for i in range(120):
    th=mp.mpf('0.5')+(mp.mpf('1.1338')-mp.mpf('0.5'))*mp.mpf(i)/mp.mpf(119)
    A0m=A0_max(th)
    if A0m>best_A0: best_A0,best_th=A0m,th
    if i%12==0:
        print(f"{mp.nstr(th,6):<10} {mp.nstr(A0m,10):<12} {mp.nstr(A0_g(th),10):<12} {mp.nstr(A0_tan(th),10):<12} {mp.nstr(w0(th),10):<12} {mp.nstr(C(L(A0m),L(A0m),th),10)}")
print(f"\nmax on [0.5,1.1338]: theta*={mp.nstr(best_th,6)}  A0_max={mp.nstr(best_A0,12)}")
print(f"#45 value = 0.324204954225")
print(f"GLOBAL max (combining [0.5,1.1338] and [1.1338,1.56]) is at theta=1.1338: {best_A0 <= mp.mpf('0.324204954225')+mp.mpf('1e-9')}")
