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
    if u < 0 or u > u_max:
        return mp.mpf(0)
    inner = (sec2*(theta*cot - u/2)*mp.cos(u*tan) + (2*theta*cot - u)
             + mp.sin(2*theta - u*tan)/mp.sin(2*theta)   # csc(2theta) per LaTeX source
             - 2*(1 + mp.sin(theta - u*tan)/mp.sin(theta)))
    return sec2*inner
w0 = w(0)
ok = abs(w0-mp.mpf('5.672787598'))<mp.mpf('1e-6')
print("w(0) computed =", mp.nstr(w0,12), " paper 5.672787598  match:", ok)
assert ok, "w(0) does not match paper"
# GL quadrature for W(z)=int_0^{u_max} e^{-zu} w(u) du
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
kap=[mp.mpf(1),mp.mpf(-851)/859,mp.mpf(780)/859,mp.mpf(-525)/859,
     mp.mpf(171)/859,mp.mpf(28)/859,mp.mpf(-29)/859]
M=6; a0=mp.mpf(1); a1=mp.mpf(865534)/mp.mpf(497079)
eta0=mp.mpf('0.0071093'); sigma0=mp.mpf('0.9935164')
mu_min=(1-sigma0)/eta0 - mp.mpf('1e-10')
def delta(m,s): return (2*s-1)*m
def F(z,s,eta):
    r=mp.mpf(0)
    for m in range(M+1):
        r += kap[m]*W((z+delta(m,s))/eta)
    return r
def C1(x): return mp.mpf('0.87637')+mp.mpf('0.12002')*x+mp.mpf('0.01017')*x**2-mp.mpf('0.00073')*x**3
kappa_paper=sum(kap); kappa_req=mp.mpf('0.521015891482995'); Kmax_c3a=mp.mpf('0.03830132421')
print("kappa_paper =", mp.nstr(kappa_paper,12))
N=48
worst_K=mp.mpf('inf'); worst=None; min_margin=mp.mpf('inf'); min_margin_pt=None; count=0
for i in range(N):
    if time.time()-t0>480: print("TIME GUARD hit"); break
    s = sigma0 + (1-sigma0-mp.mpf('1e-9'))*mp.mpf(i)/(N-1)
    for j in range(N):
        mu = mu_min + (1-mu_min)*mp.mpf(j)/(N-1)
        eta = (1-s)/mu
        if eta>eta0+mp.mpf('1e-12'): continue
        z1=s-1+eta; z2=s-eta; z3=s-1
        LHS=a1*F(z1,s,eta)+a1*F(z2,s,eta)-a0*F(z3,s,eta)
        RHS=C1(mu)+mp.mpf('3.909')*eta+mp.mpf('26')*eta**2-mp.mpf('3897')*eta**3
        margin=LHS-RHS
        if margin<min_margin: min_margin=margin; min_margin_pt=(mp.nstr(s,8),mp.nstr(mu,8),mp.nstr(eta,10))
        d6=delta(6,s)
        D14=a1*W((z1+d6)/eta)+a1*W((z2+d6)/eta)-a0*W((z3+d6)/eta)
        K_allowed = mp.mpf('inf') if D14>=0 else margin/(-D14)
        if K_allowed<worst_K:
            worst_K=K_allowed; worst=(mp.nstr(s,8),mp.nstr(mu,8),mp.nstr(eta,10),mp.nstr(margin,8),mp.nstr(D14,8))
        count+=1
print("grid points evaluated =", count)
print("min margin14 (paper kappa) =", mp.nstr(min_margin,8), "at (s,mu,eta)=",min_margin_pt)
print("worst Lemma14 K_allowed =", mp.nstr(worst_K,10), "at (s,mu,eta,margin,D14)=",worst)
Kmax = min(worst_K, Kmax_c3a)
kappa_max = kappa_paper + Kmax
print("Kmax_c3a =", mp.nstr(Kmax_c3a,10))
print("K_max (min of C3a, C3c) =", mp.nstr(Kmax,10))
print("kappa_max =", mp.nstr(kappa_max,12))
print("kappa_required =", mp.nstr(kappa_req,12))
print("kappa_max > kappa_required ?", bool(kappa_max>kappa_req))
print("elapsed s =", round(time.time()-t0,1))
