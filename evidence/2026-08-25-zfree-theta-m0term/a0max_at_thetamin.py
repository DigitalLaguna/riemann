# A0_max at the best feasible theta under the m=0 term Taylor bound constraint
# theta >= theta_min = 0.980175494979204. A0_max(th) is decreasing for th>0.0572,
# so the best feasible theta is the boundary theta_min.
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

theta_min = mp.mpf('0.980175494979204')
for th,lab in [(mp.mpf('1.1338'),'paper theta=1.1338'),
               (theta_min,'theta_min=0.9802 (best feasible)'),
               (mp.mpf('0.057151961'),'theta* #46 (infeasible)')]:
    a=A0_max(th)
    print(f"{lab}: A0_max={mp.nstr(a,12)}  1/A0_max={mp.nstr(1/a,10)}  "
          f"[A0_tan={mp.nstr(A0_tan(th),10)} A0_g={mp.nstr(A0_g(th),12)}]")
