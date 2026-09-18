import numpy as np
from tradeoff import simplex_max

# Test 1: max x1 - x2 s.t. x1-x2<=1, x1+x2<=3, x1,x2>=0 -> expect 1
v,x=simplex_max(np.array([1.,-1.]), np.array([[1.,-1.],[1.,1.]]), np.array([1.,3.]))
print("T1 val=%.4f x=%s (expect 1, [1,0])"%(v,x))

# Test 2: tradeoff with n=1 (q=c1*x), E=0.01. Bounded: q(1)=c1<=g(1)+E=-0.49
g=lambda x:-x/(1.0+x)
N=50; X=np.linspace(0,1,N); GX=np.array([g(x) for x in X])
E=0.01
A=[];b=[]
for xi,gxi in zip(X,GX):
    A.append([xi,-xi]); b.append(gxi+E)
    A.append([-xi,xi]); b.append(E-gxi)
A=np.array(A);b=np.array(b)
v,x=simplex_max(np.array([1.,-1.]),A,b)
print("T2 (n=1,E=0.01) val=%.6f (expect <= -0.49) x=%s"%(v,x))
# brute force n=1: max c1 s.t. |c1 x - g(x)|<=E all x. c1 <= g(x)+E over x>0 -> c1 <= min_x (g(x)+E)/x
xs=np.linspace(1e-6,1,100001)
c1max=min((g(x)+E)/x for x in xs)
print("  brute c1max=%.6f"%c1max)
