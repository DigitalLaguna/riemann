import numpy as np, mpmath as mp
mp.mp.dps = 50
M = 6
c0 = mp.mpf(151)/mp.mpf(153); c0f = float(c0)
eps0 = mp.mpf(1)/mp.mpf(2000); eps0f = float(eps0)
kap_paper_f = [1.0, -851/859, 780/859, -525/859, 171/859, 28/859, -29/859]

def b_coeffs_f(kap):
    b=[kap[0]]
    for m in range(1,M+1): b.append(kap[m]+kap[m-1])
    b.append(kap[M]); return b

# c_m(y) with paper signs fixed: sign of b_m for paper kap
b_paper = b_coeffs_f(kap_paper_f)
sign_paper = [1 if b>0 else -1 for b in b_paper]  # index 0..7
def c_m_y(m, y):
    # m in 1..7
    if sign_paper[m]==1:
        return (m - eps0f/m)/(m*m + y*y)
    else:
        return (m + eps0f/m)/((c0f*m)**2 + y*y)

def B_y_f(y, kap):
    b = b_coeffs_f(kap)
    s=0.0
    for m in range(1,M+2):
        s += b[m]*c_m_y(m,y)
    return s

def simplex_max(c, A, b, tol=1e-10, itmax=200000):
    m,n=A.shape
    A2=A.astype(float).copy(); b2=b.astype(float).copy()
    for i in range(m):
        if b2[i]<0: A2[i]*=-1; b2[i]*=-1
    T=np.zeros((m+1,n+m+1))
    T[:m,:n]=A2; T[:m,n:n+m]=np.eye(m); T[:m,-1]=b2; T[m,:n]=-c
    basis=list(range(n,n+m))
    for it in range(itmax):
        obj=T[m,:-1]; j=int(np.argmin(obj))
        if obj[j]>=-tol: break
        col=T[:m,j]; ratios=[]
        for i in range(m):
            if col[i]>tol: ratios.append((T[i,-1]/col[i],i))
        if not ratios: return 'unbounded',None,None
        ratios.sort(); i=ratios[0][1]; piv=T[i,j]
        T[i]=T[i]/piv
        for r in range(m+1):
            if r!=i: T[r]=T[r]-T[i]*T[r,j]
        basis[i]=j
    x=np.zeros(n+m)
    for i,bv in enumerate(basis): x[bv]=T[i,-1]
    return 'optimal',x[:n],T[m,-1]

# ---- build LP: vars = kap_1..kap_6 ----
# (C1) p(x)=1+sum kap_m x^m >= eps  ->  -sum kap_m x^m <= 1-eps
eps_C1 = 1e-4
X = np.arange(0.01, 1.001, 0.01)
A=[]; b=[]
for xi in X:
    row = np.array([xi**m for m in range(1,7)])
    A.append(-row); b.append(1.0-eps_C1)
# (C2) B(y)>=0 -> sum_m b_m c_m(y) >= 0 -> -sum_m b_m c_m(y) <= 0
# b_m linear in kap: b1=k1+1,b2=k2+k1,...,b7=k6
# B(y) = k1(c1+c2)+k2(c2+c3)+k3(c3+c4)+k4(c4+c5)+k5(c5+c6)+k6(c6+c7) + c1
# => [c1+c2, c2+c3, c3+c4, c4+c5, c5+c6, c6+c7].k  >= -c1
# => -[...].k <= c1
Y = np.arange(0.0, 50.001, 0.1)
for y in Y:
    cm = [c_m_y(m,y) for m in range(1,8)]  # cm[0]=c_1 .. cm[6]=c_7
    coef = np.array([cm[0]+cm[1], cm[1]+cm[2], cm[2]+cm[3], cm[3]+cm[4], cm[4]+cm[5], cm[5]+cm[6]])
    A.append(-coef); b.append(cm[0])  # -coef.k <= cm[0]  i.e. coef.k >= -cm[0]
A=np.array(A); b=np.array(b)
cobj=np.ones(6)
st,x,v = simplex_max(cobj,A,b)
print("=== LP: max kap = 1+sum kap_m  s.t. (C1) p(x)>=eps, (C2) B(y)>=0 ===")
print("status =", st)
if st=='optimal':
    kap = [1.0]+list(x)
    kapsum = sum(kap)
    print("kap_m =", ["%.6f"%k for k in kap])
    print("kappa = sum kap_m = %.9f" % kapsum)
    print("paper kappa = %.9f" % sum(kap_paper_f))
    print("threshold   = 0.521015891482995")
    print("kappa > threshold? %s" % (kapsum > 0.521015891482995))
    # verify on FINE grids
    Xf = np.arange(0.001,1.0001,0.001)
    pmin = min(1.0+sum(kap[m]*xi**m for m in range(1,7)) for xi in Xf)
    Yf = np.arange(0.0,100.001,0.05)
    Bmin = min(B_y_f(y,kap) for y in Yf)
    b_new = b_coeffs_f(kap)
    signs_new = [1 if bb>0 else -1 for bb in b_new]
    print("fine-grid min p(x) = %.6e (need >0)" % pmin)
    print("fine-grid min B(y) = %.6e (need >=0)" % Bmin)
    print("signs paper =", sign_paper[1:])
    print("signs new   =", signs_new[1:])
    print("signs match? %s" % (sign_paper[1:]==signs_new[1:]))
else:
    print("LP is", st)
