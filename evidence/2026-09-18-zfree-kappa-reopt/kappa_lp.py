import numpy as np, mpmath as mp
mp.mp.dps = 50

# ---- paper kappa_m (eq 18) ----
kap_paper = [mp.mpf(1), mp.mpf(-851)/859, mp.mpf(780)/859, mp.mpf(-525)/859,
             mp.mpf(171)/859, mp.mpf(28)/859, mp.mpf(-29)/859]
kap_paper_f = [float(k) for k in kap_paper]
M = 6
c0 = mp.mpf(151)/mp.mpf(153)
eps0 = mp.mpf(1)/mp.mpf(2000)

def b_coeffs(kap):
    # b_0=kap_0, b_m=kap_m+kap_{m-1} (1..M), b_{M+1}=kap_M
    b = [kap[0]]
    for m in range(1, M+1): b.append(kap[m]+kap[m-1])
    b.append(kap[M])
    return b  # length M+2 = 8

def B_y(y, kap, use_mp=False):
    b = b_coeffs(kap)
    s = mp.mpf(0) if use_mp else 0.0
    for m in range(1, M+2):
        bm = b[m]
        if use_mp:
            num = m + (eps0/m if bm <= 0 else -eps0/m)
            den = (c0*m)**2 + mp.mpf(y)**2 if bm <= 0 else mp.mpf(m)**2 + mp.mpf(y)**2
            s += bm * num / den
        else:
            bm_f = float(bm)
            num = m + (float(eps0)/m if bm_f <= 0 else -float(eps0)/m)
            den = (float(c0)*m)**2 + y*y if bm_f <= 0 else m*m + y*y
            s += bm_f * num / den
    return s

# ---- paper p(y)/q(y) (verbatim, line ~697) ----
def p_paper(y):
    return (4061245152630328137981*y**12 + 4077560173170236734684710*y**10
            - 104378137212291977844887868*y**8 - 4484512641017853031179075270*y**6
            + 135673322742635307737680349343*y**4 - 229732179325278720034298507440*y**2
            + 112359769561546903428467326544)
def q_paper(y):
    c0f = float(c0)
    return (4012454647232553285540000*(y**2+1)*(y**2+9)*(y**2+25)
            *(y**2+4*c0f**2)*(y**2+16*c0f**2)*(y**2+36*c0f**2)*(y**2+49*c0f**2))

print("=== VERIFY B(y) formula vs paper p(y)/q(y) ===")
maxrel = 0.0
for y in [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
    Bf = float(B_y(y, kap_paper, use_mp=True))
    Bp = p_paper(y)/q_paper(y)
    rel = abs(Bf-Bp)/max(abs(Bp),1e-30)
    maxrel = max(maxrel, rel)
    print("  y=%6.2f  B_formula=%.12f  B_paper=%.12f  rel=%.2e" % (y, Bf, Bp, rel))
print("  max rel diff =", maxrel)

# ---- simplex (max c.x s.t. Ax<=b, x>=0) ----
def simplex_max(c, A, b, tol=1e-10, itmax=200000):
    m, n = A.shape
    A2 = A.astype(float).copy(); b2 = b.astype(float).copy()
    for i in range(m):
        if b2[i] < 0: A2[i]*=-1; b2[i]*=-1
    T = np.zeros((m+1, n+m+1))
    T[:m,:n]=A2; T[:m,n:n+m]=np.eye(m); T[:m,-1]=b2; T[m,:n]=-c
    basis=list(range(n,n+m))
    for it in range(itmax):
        obj=T[m,:-1]; j=int(np.argmin(obj))
        if obj[j]>=-tol: break
        col=T[:m,j]; ratios=[]
        for i in range(m):
            if col[i]>tol: ratios.append((T[i,-1]/col[i],i))
        if not ratios: return 'unbounded', None, None
        ratios.sort(); i=ratios[0][1]; piv=T[i,j]
        T[i]=T[i]/piv
        for r in range(m+1):
            if r!=i: T[r]=T[r]-T[i]*T[r,j]
        basis[i]=j
    x=np.zeros(n+m)
    for i,bv in enumerate(basis): x[bv]=T[i,-1]
    return 'optimal', x[:n], T[m,-1]

# test simplex on bounded problem: max x s.t. x<=1, x>=0 -> 1
st,x,v = simplex_max(np.array([1.0]), np.array([[1.0]]), np.array([1.0]))
print("\n=== SIMPLEX TEST ===")
print("  max x s.t. x<=1: st=%s v=%.6f (expect optimal 1.0)" % (st, v))
# bounded 2-var: max x+y s.t. x+y<=1, x<=1, y<=1 -> 1
st,x,v = simplex_max(np.array([1.,1.]), np.array([[1.,1.],[1.,0.],[0.,1.]]), np.array([1.,1.,1.]))
print("  max x+y s.t. x+y<=1,x<=1,y<=1: st=%s v=%.6f (expect optimal 1.0)" % (st, v))
