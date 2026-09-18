import mpmath as mp
mp.mp.dps = 80

# ---- exact paper constants ----
theta = mp.mpf('1.1338')
a0 = mp.mpf(1)
a1 = mp.mpf(865534)/mp.mpf(497079)
a  = mp.mpf(2919857)/mp.mpf(828465)
H  = mp.mpf(3)*mp.mpf(10)**12
K  = mp.mpf(16)
T0 = mp.mpf(10)**10
A0 = mp.mpf(1)/mp.mpf('4.896')          # claim #41: true Lemma-1 A0 (table typo)
eta0 = A0/mp.log(H)
sigma0 = 1 - A0/mp.log(K*H + T0)
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')
print("PARAMS (Lemma-1 row, A0=(4.896)^-1):")
print("  A0    =", mp.nstr(A0,12))
print("  eta0  =", mp.nstr(eta0,12), " (paper 0.0071093)")
print("  sigma0=", mp.nstr(sigma0,12), " (paper 0.9935164)")
print("  mu0   =", mp.nstr(mu0,12), " (paper 0.91198...)")

# ---- w(u) from Definition 1 ----
s2 = 1/mp.cos(theta)**2          # sec^2 theta
ct = mp.cot(theta)
tt = mp.tan(theta)
L  = 2*theta*ct                  # support endpoint 2 theta cot theta
def w(u):
    if u < 0 or u > L: return mp.mpf(0)
    return s2*( s2*(theta*ct - u/2)*mp.cos(u*tt)
                + 2*theta*ct - u
                + mp.sin(2*theta - u*tt)/mp.sin(2*theta)
                - 2*(1 + mp.sin(theta - u*tt)/mp.sin(theta)) )

# ---- verify w against paper constants ----
w0_paper = mp.mpf('5.672787598')
w0 = w(0)
print("\nVERIFY w:")
print("  w(0)      =", mp.nstr(w0,12), " paper 5.672787598  match:", abs(w0-w0_paper)<mp.mpf('1e-8'))
print("  support L =", mp.nstr(L,12), " (paper 2theta cot theta = 1.05923293)")

# c_n = int_0^L u^n (a1 e^{-u} - a0) w(u) du
def cn(n):
    return mp.quad(lambda u: u**n*(a1*mp.e**(-u)-a0)*w(u), [0, L])
c_paper = {0:mp.mpf('0.8763706262'),1:mp.mpf('0.1200272738'),2:mp.mpf('0.0203537951'),3:mp.mpf('0.0004382722')}
for n in range(4):
    cv = cn(n)
    print("  c%d      ="%n, mp.nstr(cv,12), " paper", mp.nstr(c_paper[n],12), " match:", abs(cv-c_paper[n])<mp.mpf('1e-8'))
