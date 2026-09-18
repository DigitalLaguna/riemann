import mpmath as mp
import time
t0=time.time()
mp.mp.dps = 40
theta = mp.mpf('1.1338')
sec2 = 1/mp.cos(theta)**2
cot  = mp.cos(theta)/mp.sin(theta)
tan  = mp.sin(theta)/mp.cos(theta)
u_max = 2*theta*cot
def w(u):
    if u < 0 or u > u_max: return mp.mpf(0)
    inner = (sec2*(theta*cot - u/2)*mp.cos(u*tan) + (2*theta*cot - u)
             + mp.sin(2*theta - u*tan)/mp.sin(2*theta)
             - 2*(1 + mp.sin(theta - u*tan)/mp.sin(theta)))
    return sec2*inner
w0 = w(0)
assert abs(w0-mp.mpf('5.672787598'))<mp.mpf('1e-6')
import numpy as np
NGL=80
nodes,weights = np.polynomial.legendre.leggauss(NGL)
gl_nodes=[mp.mpf(u_max)*(mp.mpf(x)+1)/2 for x in nodes]
gl_wts=[mp.mpf(u_max)/2*mp.mpf(wt) for wt in weights]
def W(z):
    r=mp.mpf(0)
    for x,wt in zip(gl_nodes,gl_wts):
        r += wt*mp.exp(-z*x)*w(x)
    return r
a0=mp.mpf(1); a1=mp.mpf(865534)/mp.mpf(497079)
eta0=mp.mpf('0.0071093'); sigma0=mp.mpf('0.9935164')
mu_min=(1-sigma0)/eta0 - mp.mpf('1e-10')
N=72
minD14=mp.mpf('inf'); minpt=None; count=0; neg=0
for i in range(N):
    if time.time()-t0>540: print("TIME GUARD hit at i=",i); break
    s = sigma0 + (1-sigma0-mp.mpf('1e-9'))*mp.mpf(i)/(N-1)
    for j in range(N):
        mu = mu_min + (1-mu_min)*mp.mpf(j)/(N-1)
        eta = (1-s)/mu
        if eta>eta0+mp.mpf('1e-12'): continue
        d6=(2*s-1)*mp.mpf(6)
        z1=s-1+eta; z2=s-eta; z3=s-1
        D14=a1*W((z1+d6)/eta)+a1*W((z2+d6)/eta)-a0*W((z3+d6)/eta)
        if D14<minD14: minD14=D14; minpt=(mp.nstr(s,8),mp.nstr(mu,8),mp.nstr(eta,10))
        if D14<0: neg+=1
        count+=1
print("grid points evaluated =", count)
print("min D14 =", mp.nstr(minD14,10), "at (s,mu,eta)=",minpt)
print("num points with D14<0 =", neg)
print("D14>=0 everywhere on grid ?", bool(neg==0))
print("elapsed s =", round(time.time()-t0,1))
