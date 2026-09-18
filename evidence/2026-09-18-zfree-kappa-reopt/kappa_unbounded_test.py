import numpy as np, mpmath as mp
mp.mp.dps=50
M=6; c0f=float(mp.mpf(151)/mp.mpf(153)); eps0f=float(mp.mpf(1)/mp.mpf(2000))
kap_paper_f=[1.0,-851/859,780/859,-525/859,171/859,28/859,-29/859]
def b_coeffs_f(kap):
    b=[kap[0]]
    for m in range(1,M+1): b.append(kap[m]+kap[m-1])
    b.append(kap[M]); return b
b_paper=b_coeffs_f(kap_paper_f)
sign_paper=[1 if b>0 else -1 for b in b_paper]
def c_m_y(m,y):
    if sign_paper[m]==1: return (m-eps0f/m)/(m*m+y*y)
    else: return (m+eps0f/m)/((c0f*m)**2+y*y)
def B_y_f(y,kap):
    b=b_coeffs_f(kap); s=0.0
    for m in range(1,M+2): s+=b[m]*c_m_y(m,y)
    return s
def check(kap,label):
    Xf=np.arange(0.001,1.0001,0.001)
    pmin=min(1.0+sum(kap[m]*xi**m for m in range(1,7)) for xi in Xf)
    Yf=np.arange(0.0,100.001,0.05)
    Bmin=min(B_y_f(y,kap) for y in Yf)
    print("%s: kappa=%.6f  min p(x)=%.3e  min B(y)=%.3e  (C1 ok:%s) (C2 ok:%s)"
          %(label,sum(kap),pmin,Bmin,pmin>0,Bmin>=0))
check(kap_paper_f,"paper")
# increase kappa_6 a lot (direction that raises kappa)
for K in [2,5,10,50]:
    kap=kap_paper_f[:]; kap[6]=kap_paper_f[6]+K
    check(kap,"k6+=%d"%K)
# direction: add K*x^6 to p (raises kappa by K, keeps p>0)
for K in [2,5,10]:
    kap=kap_paper_f[:]; kap[6]=kap_paper_f[6]+K
    check(kap,"p+Kx6 K=%d"%K)
