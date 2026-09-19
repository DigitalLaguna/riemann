# GAP check for claim #58 (kappa_m re-opt), FAST version (GL quadrature).
# Verify, at the PINNED point (th=hi, A0=A0_g(hi)), for the MODIFIED kappa_m
# (paper + K*x^6, K=0.03830132421), that the actual Lemma-14 LHS satisfies
#   LHS >= C1(mu) + C2(eta)   on the domain mu in [mu0,1], eta in (0,eta0],
# where C2(eta)=13.47*eta-161*eta^2-11896*eta^3 is the C2 the A_final formula
# (claim #40) actually uses (line 2527). This is the bound the A_final
# re-optimization needs. Also report the weaker Lemma-14-as-stated bound
# (3.909*eta+26*eta^2-3897*eta^3) for comparison.
import mpmath as mp, time
t0=time.time()
mp.mp.dps = 40
T0=mp.mpf(10)**10; H=mp.mpf(3)*mp.mpf(10)**12; K=mp.mpf(16)
xKT=mp.log(K*H+T0); xH=mp.log(H)
def eta0(A0): return A0/xH
def sig0(A0): return 1-A0/xKT
def w0(th): return mp.sec(th)**2*(th*mp.tan(th)+3*th/mp.tan(th)-3)
def g(A0,th):
    L=(2*sig0(A0)-1)/eta0(A0)
    c0=1/mp.sin(th)*mp.sec(th)**2
    c1=(th-mp.sin(th)*mp.cos(th))*mp.tan(th)**4
    c2=mp.tan(th)**3*mp.sin(th)**2
    c3=(th-mp.sin(th)*mp.cos(th))*mp.tan(th)**2
    C=c0*L*(c2*(L+1)**2*(mp.e**(-2*L*th)/mp.tan(th)+1)+c1*L+c3*L**3)/(L**2-mp.tan(th)**2)**2
    return eta0(A0)**2*C/(mp.mpf('0.0005')*(2*sig0(A0)-1)*w0(th))
def A0_g(th):
    lo,hi=mp.mpf('0.001'),mp.mpf(10)
    for _ in range(170):
        mid=(lo+hi)/2
        if g(mid,th)<1: lo=mid
        else: hi=mid
    return lo
kap_paper=[mp.mpf(1),mp.mpf(-851)/859,mp.mpf(780)/859,mp.mpf(-525)/859,
           mp.mpf(171)/859,mp.mpf(28)/859,mp.mpf(-29)/859]
Kmod=mp.mpf('0.03830132421')
kap_mod=list(kap_paper); kap_mod[6]=kap_mod[6]+Kmod
kap_sum=sum(kap_mod)
a0=mp.mpf(1); a1=mp.mpf(865534)/mp.mpf(497079)
# ---- w(u), W(z) at pinned th, GL quadrature ----
hi=mp.mpf('0.376216048449719989')
A0p=A0_g(hi)
th=hi
b=2*th/mp.tan(th)
s2=mp.sec(th)**2
tn=mp.tan(th)
def w(u):
    if u<0 or u>b: return mp.mpf(0)
    return s2*(s2*(th/tn-u/2)*mp.cos(u*tn)+2*th/tn-u
              +mp.sin(2*th-u*tn)/mp.sin(2*th)
              -2*(1+mp.sin(th-u*tn)/mp.sin(th)))
w0v=w(0)
assert abs(w0v-mp.mpf('5.672787598'))<mp.mpf('0.5'), w0v  # w0 differs at th=hi; just report
import numpy as np
NGL=64
nodes,weights=np.polynomial.legendre.leggauss(NGL)
glx=[b*(mp.mpf(x)+1)/2 for x in nodes]
glw=[b/2*mp.mpf(wt) for wt in weights]
def W(s):
    if s>40:
        # scaled: W(s)=(1/s) int_0^{min(b s,60)} e^{-t} w(t/s) dt
        ub=min(b*s,mp.mpf(60))
        r=mp.mpf(0)
        for x,wt in zip(glx,glw):
            r+=wt*mp.e**(-x)*w(x*ub/b)
        return r/s*ub/b*mp.mpf(1)  # placeholder, fixed below
    r=mp.mpf(0)
    for x,wt in zip(glx,glw):
        r+=wt*mp.e**(-s*x)*w(x)
    return r
# fix scaled W properly
def W(s):
    if s>40:
        ub=min(b*s,mp.mpf(60))
        r=mp.mpf(0)
        for x,wt in zip(glx,glw):
            r+=wt*mp.e**(-x)*w(x*ub/b)
        return r*ub/(b*s)
    r=mp.mpf(0)
    for x,wt in zip(glx,glw):
        r+=wt*mp.e**(-s*x)*w(x)
    return r
def F(z,sigma,eta):
    return sum(kap_mod[m]*W((z+(2*sigma-1)*m)/eta) for m in range(7))
def LHS(mu,eta):
    sigma=1-mu*eta
    return a1*F(sigma-1+eta,sigma,eta)+a1*F(sigma-eta,sigma,eta)-a0*F(sigma-1,sigma,eta)
def C1(x): return mp.mpf('0.87637')+mp.mpf('0.12002')*x+mp.mpf('0.01017')*x**2-mp.mpf('0.00073')*x**3
def C2(y): return mp.mpf('13.47')*y-mp.mpf('161')*y**2-mp.mpf('11896')*y**3
def L14stated(y): return mp.mpf('3.909')*y+mp.mpf('26')*y**2-mp.mpf('3897')*y**3
sigma0=sig0(A0p); e0=eta0(A0p); mu0=(1-sigma0)/e0
print("pinned: A0 =",mp.nstr(A0p,15)," th =",mp.nstr(th,12))
print("w0(th=hi) =",mp.nstr(w0v,12),"  (paper w0 at th=1.1338 is 5.672787598)")
print("sigma0 =",mp.nstr(sigma0,12)," eta0 =",mp.nstr(e0,12)," mu0 =",mp.nstr(mu0,12))
print("kappa_mod =",mp.nstr(kap_sum,15))
Nmu=Neta=40
minC1C2=mp.mpf('inf'); minpt=None; negC1C2=0
minL14=mp.mpf('inf'); minpt14=None; negL14=0
count=0
for i in range(Nmu):
    mu=mu0+(1-mu0)*mp.mpf(i)/(Nmu-1)
    for j in range(Neta):
        eta=e0*mp.mpf(j+1)/Neta
        v=LHS(mu,eta)
        d1=v-C1(mu)-C2(eta)
        d2=v-C1(mu)-L14stated(eta)
        if d1<minC1C2: minC1C2=d1; minpt=(mp.nstr(mu,8),mp.nstr(eta,10))
        if d1<0: negC1C2+=1
        if d2<minL14: minL14=d2; minpt14=(mp.nstr(mu,8),mp.nstr(eta,10))
        if d2<0: negL14+=1
        count+=1
print("grid points =",count)
print("STRONG (A_final C2): min(LHS-C1-C2) =",mp.nstr(minC1C2,12)," at (mu,eta)=",minpt,"  neg pts =",negC1C2)
print("WEAK  (Lemma14 stated): min(LHS-C1-L14) =",mp.nstr(minL14,12)," at (mu,eta)=",minpt14,"  neg pts =",negL14)
print("STRONG holds everywhere ?",bool(negC1C2==0))
print("WEAK holds everywhere ?",bool(negL14==0))
print("elapsed s =",round(time.time()-t0,1))
