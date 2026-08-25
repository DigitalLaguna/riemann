#!/usr/bin/env python3
"""Low-theta scan: A0_max(theta) on [0.05, 0.55]. Find the global maximizer.
Target A0 = 0.420483467794 (full reopt, claim #40)."""
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
    for _ in range(160):
        mid=(lo+hi)/2
        if g(mid,th)<1: lo=mid
        else: hi=mid
    return lo
def A0_max(th): return min(A0_tan(th),A0_g(th))
print("theta      A0_max       A0_g         A0_tan       w0           C(L,L)     g(A0max)")
best_th,best_A0=None,mp.mpf('-1')
for i in range(200):
    th=mp.mpf('0.05')+(mp.mpf('0.55')-mp.mpf('0.05'))*mp.mpf(i)/mp.mpf(199)
    A0m=A0_max(th)
    if A0m>best_A0: best_A0,best_th=A0m,th
    if i%20==0:
        print(f"{mp.nstr(th,5):<10} {mp.nstr(A0m,10):<12} {mp.nstr(A0_g(th),10):<12} {mp.nstr(A0_tan(th),10):<12} {mp.nstr(w0(th),10):<12} {mp.nstr(C(L(A0m),L(A0m),th),10):<12} {mp.nstr(g(A0m,th),8)}")
print(f"\nmax on [0.05,0.55]: theta*={mp.nstr(best_th,8)}  A0_max={mp.nstr(best_A0,12)}  (1/A0_max={mp.nstr(1/best_A0,10)})")
print(f"target = 0.420483467794   #45 = 0.324204954225")
print(f"reaches target? {best_A0 >= mp.mpf('0.420483467794')}")
