import mpmath as mp
mp.mp.dps = 50
theta = mp.mpf('1.1338')
sec2 = 1/mp.cos(theta)**2
cot  = mp.cos(theta)/mp.sin(theta)
tan  = mp.sin(theta)/mp.cos(theta)
u_max = 2*theta*cot
def w(u):
    if u < 0 or u > u_max: return mp.mpf(0)
    inner = (sec2*(theta*cot - u/2)*mp.cos(u*tan) + (2*theta*cot - u)
             + mp.sin(2*theta - u*tan)/mp.sin(2*theta)
             - 2*(1 + mp.sin(theta - u*tan)/mp.sin(theta)))
    return sec2*inner
w0 = w(0)
assert abs(w0-mp.mpf('5.672787598'))<mp.mpf('1e-6')
eta0 = mp.mpf('0.0071093'); sigma0 = mp.mpf('0.9935164')
kap = [mp.mpf(1),mp.mpf(-851)/859,mp.mpf(780)/859,mp.mpf(-525)/859,
       mp.mpf(171)/859,mp.mpf(28)/859,mp.mpf(-29)/859]
M=6
def dlist(kap):
    return [mp.mpf(m) if kap[m]>=0 else (2*sigma0-1)*mp.mpf(m) for m in range(M+1)]
def margin11(kap):
    d = dlist(kap); kapsum = sum(kap)
    R = kapsum**2 * w0
    worst = mp.mpf('inf'); worstu=None
    N=600
    for i in range(N+1):
        u = mp.mpf(59)*mp.mpf(i)/N
        L = w(eta0*u)*sum(kap[m]*mp.exp(-d[m]*u) for m in range(M+1))
        mgn = L - R
        if mgn < worst: worst=mgn; worstu=mp.nstr(u,6)
    return worst, worstu, kapsum
# paper
wp, up, kp = margin11(kap)
print("=== Lemma 11: f(u) >= kappa*f(0), 0<=u<=59 ===")
print("PAPER kappa_m: min margin =", mp.nstr(wp,10), "at u=",up, " kappa=",mp.nstr(kp,12))
# modified: add K to kappa_6
for K in [mp.mpf('0.017'), mp.mpf('0.03376'), mp.mpf('0.03830132421')]:
    kap2 = list(kap); kap2[6] = kap2[6]+K
    wm, um, km = margin11(kap2)
    print("K=%.10f  kappa_6=%.8f  kappa=%.12f  min margin11=%s at u=%s  SATISFIED=%s"
          % (K, kap2[6], km, mp.nstr(wm,10), um, bool(wm>=0)))
