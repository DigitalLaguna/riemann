import mpmath as mp
mp.mp.dps = 60

# ---- exact paper constants ----
theta = mp.mpf('1.1338')
a0 = mp.mpf(1)
a1 = mp.mpf(865534)/mp.mpf(497079)
H  = mp.mpf(3)*mp.mpf(10)**12
K  = mp.mpf(16)
T0 = mp.mpf(10)**10
A0 = mp.mpf(1)/mp.mpf('4.896')
eta0 = A0/mp.log(H)
sigma0 = 1 - A0/mp.log(K*H + T0)
mu0 = (1-sigma0)/eta0 - mp.mpf('1e-10')

s2 = 1/mp.cos(theta)**2
ct = mp.cot(theta); tt = mp.tan(theta)
L  = 2*theta*ct
def w(u):
    if u < 0 or u > L: return mp.mpf(0)
    return s2*( s2*(theta*ct - u/2)*mp.cos(u*tt)
                + 2*theta*ct - u
                + mp.sin(2*theta - u*tt)/mp.sin(2*theta)
                - 2*(1 + mp.sin(theta - u*tt)/mp.sin(theta)) )

# ---- W(z) = int_0^L e^{-zu} w(u) du, with convergence check ----
def W(z):
    f = lambda u: mp.e**(-z*u)*w(u)
    v1 = mp.quad(f, [0, L])
    mp.mp.dps = 90
    v2 = mp.quad(f, [0, L])
    mp.mp.dps = 60
    return v2, abs(v2-v1)

# paper kappa_m
kap0 = [mp.mpf(1),mp.mpf(-851)/859,mp.mpf(780)/859,mp.mpf(-525)/859,
        mp.mpf(171)/859,mp.mpf(28)/859,mp.mpf(-29)/859]
M = 6

def F(z, sigma, eta, kap):
    s = mp.mpf(0)
    for m in range(M+1):
        dm = (2*sigma-1)*m
        val, err = W((z+dm)/eta)
        s += kap[m]*val
    return s

def C1(mu):
    return mp.mpf('0.87637')+mp.mpf('0.12002')*mu+mp.mpf('0.01017')*mu**2-mp.mpf('0.00073')*mu**3

def LHS14(sigma, eta, kap):
    F1 = F(sigma-1+eta, sigma, eta, kap)
    F2 = F(sigma-eta,   sigma, eta, kap)
    F3 = F(sigma-1,     sigma, eta, kap)
    return a1*F1 + a1*F2 - a0*F3

def RHS14(sigma, eta):
    mu = (1-sigma)/eta
    return C1(mu) + mp.mpf('3.909')*eta + mp.mpf('26')*eta**2 - mp.mpf('3897')*eta**3

# ---- corner evaluation (sigma0, eta0) ----
print("=== CORNER (sigma0, eta0) ===")
for label, kap in [("paper kappa (K=0)", kap0)]:
    kap = kap[:]
    lhs = LHS14(sigma0, eta0, kap)
    rhs = RHS14(sigma0, eta0)
    print("  %s: LHS=%.15f RHS=%.15f margin=%.6e"%(label, lhs, rhs, lhs-rhs))

# add K to kappa_6
for Kadd in [0.016941386244345, 0.02, 0.03, 0.03830132421]:
    kap = kap0[:]; kap[6] += mp.mpf(str(Kadd))
    kappa = sum(kap)
    lhs = LHS14(sigma0, eta0, kap)
    rhs = RHS14(sigma0, eta0)
    print("  K=%s kappa=%.12f: LHS-RHS=%.6e  (required kappa>0.521015891482995)"%(
        mp.nstr(Kadd,6), kappa, lhs-rhs))
