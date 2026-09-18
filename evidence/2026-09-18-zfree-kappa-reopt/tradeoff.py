import numpy as np

def simplex_max(c, A, b, tol=1e-11):
    """max c^T x s.t. A x <= b, x >= 0. Returns (val, x) or (None,None)."""
    m, n = A.shape
    A2 = A.astype(float).copy(); b2 = b.astype(float).copy()
    for i in range(m):
        if b2[i] < 0: A2[i]*=-1; b2[i]*=-1
    T = np.zeros((m+1, n+m+1))
    T[:m,:n]=A2; T[:m,n:n+m]=np.eye(m); T[:m,-1]=b2; T[m,:n]=-c
    basis=list(range(n,n+m))
    for it in range(50000):
        obj=T[m,:-1]; j=int(np.argmin(obj))
        if obj[j]>=-tol: break
        col=T[:m,j]; ratios=[]
        for i in range(m):
            if col[i]>tol: ratios.append((T[i,-1]/col[i],i))
        if not ratios: return None,None
        ratios.sort(); i=ratios[0][1]; piv=T[i,j]
        T[i]=T[i]/piv
        for r in range(m+1):
            if r!=i: T[r]=T[r]-T[i]*T[r,j]
        basis[i]=j
    x=np.zeros(n+m)
    for i,bv in enumerate(basis): x[bv]=T[i,-1]
    return T[m,-1], x[:n]

# quick test: max x+y s.t. x+y<=1, x<=1, y>=0  -> val 1
v,x=simplex_max(np.array([1.,1.]), np.array([[1.,1.],[1.,0.],[0.,1.]]), np.array([1.,1.,1.]))
print("simplex test: val=%.4f (expect 1.0)"%v)

g=lambda x:-x/(1.0+x)
N=200
X=np.linspace(0.0,1.0,N)
GX=np.array([g(x) for x in X])
# vars: c1+..c6+, c1-..c6-  (12)
def build(E):
    A=[]; b=[]
    for xi,gxi in zip(X,GX):
        row=np.zeros(12)
        for m in range(1,7):
            row[m-1]=xi**m      # c_m^+
            row[6+m-1]=-xi**m   # c_m^-
        A.append(row); b.append(gxi+E)
        A.append([-r for r in row]); b.append(E-gxi)
    return np.array(A), np.array(b)
cobj=np.array([1.]*6+[-1.]*6)

print("\nE        max_q(1)   kappa=1+max_q(1)   A_final   <A0_max?")
A0_max=0.392113247395366294
import mpmath as mp
mp.mp.dps=40
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
for E in [0.0040899,0.005,0.008,0.01,0.015,0.02,0.021016,0.025,0.03,0.05]:
    A,b=build(E); v,x=simplex_max(cobj,A,b)
    if v is None:
        print("E=%.6f  UNBOUNDED/INFEASIBLE"%E); continue
    q1=v; kap=1.0+q1
    # verify true max error on fine grid
    cf=np.zeros(6)
    for m in range(6): cf[m]=x[m]-x[6+m]
    fine=np.linspace(0,1,200001)
    qf=cf[0]*fine+cf[1]*fine**2+cf[2]*fine**3+cf[3]*fine**4+cf[4]*fine**5+cf[5]*fine**6
    trueE=max(np.abs(qf-np.array([g(t) for t in fine])))
    print("E=%.6f  max_q1=%.6f  kappa=%.6f  trueE=%.6f  A_final=%.6f  <A0_max:%s"%(
        E,q1,kap,trueE,float(Af(kap)), Af(kap)<A0_max))
