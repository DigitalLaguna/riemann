# c2_exact.py — exact rational construction of B(y) = P(u)/Q(u) for the
# corrected kappa_m (kappa_6 += K, K = 0.0382944246562725), C2 step of
# Lemma 5 (bellotti-trudgian-yang-2026, arXiv:2603.21490 v1, line 696:
# "It suffices to verify that B(y) >= 0 for all y in R").
#
# B(y) = sum_{m=1}^{7} b_m N_m / (d_m + y^2),  u = y^2,  B(y) = P(u)/Q(u),
# Q(u) = prod_m (d_m + u) > 0 for u >= 0  =>  B(y) >= 0 for all y in R
# <=> P(u) > 0 for all u >= 0.
#
# The form of N_m is DERIVED EXACTLY from the paper's explicit p(y)/q(y)
# (line ~697), not guessed from the garbled pdftotext:
#   N_m^eff := P_paper(0) * d_m / (Q_paper(0) * b_m)   (must be constant)
# and the polynomial identity P_paper(u) = sum_m b_m N_m^eff prod_{j!=m}(d_j+u)
# is checked exactly.
from fractions import Fraction as F
import mpmath as mp

c0 = F(151, 153)
eps0 = F(1, 2000)
K = F(382944246562725, 10**16)

kap_paper = [F(1), F(-851,859), F(780,859), F(-525,859), F(171,859), F(28,859), F(-29,859)]
kap = list(kap_paper); kap[6] = kap[6] + K
print("kappa_paper = %s = %.15f" % (sum(kap_paper), float(sum(kap_paper))))
print("kappa       = %s = %.15f" % (sum(kap), float(sum(kap))))

def b_coeffs(kap):
    b = [kap[0]]
    for m in range(1, 7): b.append(kap[m] + kap[m-1])
    b.append(kap[6])
    return b

def pmul(p, q):
    r = [F(0)]*(len(p)+len(q)-1)
    for i,pi in enumerate(p):
        for j,qj in enumerate(q):
            r[i+j] += pi*qj
    return r

def padd(p, q):
    n = max(len(p), len(q)); r = [F(0)]*n
    for i in range(n):
        r[i] += (p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)
    return r

def peval(p, u):
    r = F(0)
    for c in reversed(p): r = r*u + c
    return r

# ---------- paper kappa: derive N_m exactly from paper p(y) ----------
C = F(4012454647232553285540000)
p_paper_u = [F(112359769561546903428467326544), F(-229732179325278720034298507440),
             F(135673322742635307737680349343), F(-4484512641017853031179075270),
             F(-104378137212291977844887868), F(4077560173170236734684710),
             F(4061245152630328137981)]
div_ok = all(c % C == 0 for c in p_paper_u)
print("C divides all p_paper coeffs exactly? %s" % div_ok)
P_paper = [c // C for c in p_paper_u] if div_ok else None

bp = b_coeffs(kap_paper)
posp = [m for m in range(1,8) if bp[m] > 0]
negp = [m for m in range(1,8) if bp[m] <= 0]
print("paper signs: pos=%s neg=%s" % (posp, negp))
dp = {}
for m in range(1,8):
    dp[m] = F(m*m) if m in posp else (c0*F(m))**2
Qp = [F(1)]
for m in range(1,8): Qp = pmul(Qp, [F(1), dp[m]])

if P_paper is not None:
    # derive N_m^eff = P_paper(0)*d_m/(Q_paper(0)*b_m)
    N_eff = {}
    for m in range(1,8):
        N_eff[m] = peval(P_paper, F(0)) * dp[m] / (peval(Qp, F(0)) * bp[m])
    print("derived N_m^eff (paper kappa):")
    for m in range(1,8):
        cands = {
            "m-eps/m": F(m) - eps0/F(m),
            "(m-eps/m)^2": (F(m) - eps0/F(m))**2,
            "m+eps/m": F(m) + eps0/F(m),
            "(m+eps/m)^2": (F(m) + eps0/F(m))**2,
        }
        match = [k for k,v in cands.items() if v == N_eff[m]]
        print("  m=%d: N_eff = %s = %.12f  match=%s" % (m, N_eff[m], float(N_eff[m]), match))
    # exact polynomial identity check
    P_check = [F(0)]*len(Qp)
    for m in range(1,8):
        R = [F(1)]
        for j in range(1,8):
            if j != m: R = pmul(R, [F(1), dp[j]])
        P_check = padd(P_check, [ri*bp[m]*N_eff[m] for ri in R])
    print("polynomial identity P_paper == sum b_m N_eff prod_{j!=m}? %s" % (P_check == P_paper))

# ---------- corrected kappa ----------
b = b_coeffs(kap)
pos = [m for m in range(1,8) if b[m] > 0]
neg = [m for m in range(1,8) if b[m] <= 0]
print("corrected signs: pos=%s neg=%s" % (pos, neg))
for m in range(1,8):
    print("  b_%d = %s = %.15f" % (m, b[m], float(b[m])))

# use the DERIVED N_m form (must match one of the candidates; assert below)
N = {}; d = {}
for m in range(1,8):
    if m in pos:
        N[m] = F(m) - eps0/F(m); d[m] = F(m*m)
    else:
        N[m] = F(m) + eps0/F(m); d[m] = (c0*F(m))**2
# sanity: derived N_eff must equal these for the paper kappa
if P_paper is not None:
    same = all(N_eff[m] == (F(m)-eps0/F(m) if m in posp else F(m)+eps0/F(m)) for m in range(1,8))
    print("derived N_eff == unsquared m+/-eps/m form? %s" % same)

Q = [F(1)]
for m in range(1,8): Q = pmul(Q, [F(1), d[m]])
P = [F(0)]*len(Q)
for m in range(1,8):
    R = [F(1)]
    for j in range(1,8):
        if j != m: R = pmul(R, [F(1), d[j]])
    P = padd(P, [ri*b[m]*N[m] for ri in R])

print("deg P = %d, deg Q = %d" % (len(P)-1, len(Q)-1))
for i in range(len(P)):
    print("a_%d = %s = %.15f" % (i, P[i], float(P[i])))
a6 = P[6]
S = sum(abs(P[i]) for i in range(6))
U = -(-S // a6) + 1   # ceil(S/a6) + 1
print("a_6 = %s = %.15f (>0: %s)" % (a6, float(a6), a6 > 0))
print("S = sum_{k<6}|a_k| = %s = %.15f" % (S, float(S)))
print("S/a_6 = %.15f   U = %d   a_6*U - S = %s = %.15f" % (float(S/a6), U, a6*U - S, float(a6*U - S)))
print("P(0) = %s = %.15f   Q(0) = %s = %.15f" % (P[0], float(P[0]), Q[0], float(Q[0])))
print("B(0) = P(0)/Q(0) = %s = %.15f" % (P[0]/Q[0], float(P[0]/Q[0])))

# consistency: P(u)/Q(u) == sum b_m N_m/(d_m+u) at sample u (exact)
ok = True
for u in [F(0), F(1,4), F(1), F(4), F(25), F(100), F(10000)]:
    lhs = peval(P, u)/peval(Q, u)
    rhs = sum(b[m]*N[m]/(d[m]+u) for m in range(1,8))
    if lhs != rhs: ok = False; print("  MISMATCH at u=%s" % u)
print("consistency P/Q == sum b_m N_m/(d_m+u) at 7 sample u? %s" % ok)

# ---------- mpmath diagnostic (NOTE-level, sizes the Arb bisection) ----------
mp.mp.dps = 50
def B_y(y):
    s = mp.mpf(0)
    for m in range(1,8):
        bm = mp.mpf(str(b[m]))
        if m in pos:
            s += bm*(mp.mpf(m) - mp.mpf('0.0005')/mp.mpf(m))/(mp.mpf(m)**2 + y*y)
        else:
            s += bm*(mp.mpf(m) + mp.mpf('0.0005')/mp.mpf(m))/((mp.mpf('151/153')*mp.mpf(m))**2 + y*y)
    return s
best = None; besty = mp.mpf(0)
y = mp.mpf(0)
while y <= 500:
    v = B_y(y)
    if best is None or v < best: best, besty = v, y
    y += mp.mpf('0.01')
# refine
lo = max(0, besty - mp.mpf('0.5')); y = lo
while y <= besty + mp.mpf('0.5'):
    v = B_y(y)
    if v < best: best, besty = v, y
    y += mp.mpf('1e-5')
u_star = besty**2
P_at = peval(P, F(int(u_star)))  # rough (integer u)
print("diag: min B_correct on [0,500] ~ %.12f at y ~ %.6f (u ~ %.4f)" % (float(best), float(besty), float(u_star)))
print("diag: P(u_star) ~ %.6f  (B*Q at u_star)" % (float(best)*float(peval(Q, F(int(u_star))))))
