import numpy as np, mpmath as mp
from lp2 import lp_max
mp.mp.dps = 40

g = lambda x: -x/(1.0+x)
N = 400
X = np.linspace(0.0, 1.0, N)
GX = np.array([g(x) for x in X])

def build(E):
    A=[]; b=[]
    for xi,gxi in zip(X,GX):
        row=np.zeros(6)
        for m in range(1,7):
            row[m-1]=xi**m
        A.append(row); b.append(gxi+E)
        A.append([-r for r in row]); b.append(E-gxi)
    return np.array(A), np.array(b)

cobj=np.ones(6)

# A_final formula (repro_gate.py)
a=mp.mpf(2919857)/mp.mpf(828465); w0=mp.mpf('5.672787598'); xT=mp.mpf('76.47')
c_mu=mp.log(mp.mpf(16)+mp.mpf(10)**10/(mp.mpf(3)*mp.mpf(10)**12))
def C1(mu): return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3
def C2(eta):return mp.mpf('13.47')*eta-mp.mpf('161')*eta**2-mp.mpf('11896')*eta**3
def Af(kap):
    den=a*mp.mpf(kap)**2*w0/2; A=mp.mpf('0.2')
    for i in range(300):
        An=(C1(1-c_mu/xT)+C2(A/xT)-mp.mpf('1e-7'))/den
        if abs(An-A)<mp.mpf('1e-45'): A=An; break
        A=An
    return A
A0_max=mp.mpf('0.392113247395366294')

print("E          max_q1      kappa=1+q1   trueE      A_final    <A0_max?")
for E in [0.0040899,0.005,0.008,0.01,0.015,0.02,0.021015891483,0.025,0.03,0.05]:
    A,b=build(E)
    st,x,v=lp_max(cobj,A,b)
    if st!='optimal':
        print("E=%.9f  %s"%(E,st)); continue
    q1=v; kap=1.0+q1
    cf=x
    fine=np.linspace(0,1,200001)
    qf=np.zeros_like(fine)
    for m in range(6): qf+=cf[m]*fine**(m+1)
    trueE=max(np.abs(qf-np.array([g(t) for t in fine])))
    print("E=%.9f  q1=%.9f  kap=%.9f  trueE=%.9f  Af=%.9f  <A0max:%s"%(
        E,q1,kap,trueE,float(Af(kap)), Af(kap)<A0_max))
