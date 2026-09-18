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
assert abs(w0-mp.mpf('5.672787598'))<mp.mpf('1e-6'), w0
sigma0 = mp.mpf('0.9935164'); eta0 = mp.mpf('0.0071093')
kp = [mp.mpf(1), -mp.mpf(851)/859, mp.mpf(780)/859, -mp.mpf(525)/859,
      mp.mpf(171)/859, mp.mpf(28)/859, -mp.mpf(29)/859]
M = 6
def dm(m, km):
    return (2*sigma0-1)*m if km < 0 else mp.mpf(m)
# ---- (C4) Lemma 11: w(eta0 u) sum kappa_m e^{-d_m u} >= kappa w0 on [0,59] ----
def c4_margin(u, kappas):
    kap = sum(kappas)
    s = mp.mpf(0)
    for m,km in enumerate(kappas):
        s += km*mp.e**(-dm(m,km)*u)
    return w(eta0*u)*s - kap*w0
def c4_min(kappas):
    return min(c4_margin(mp.mpf(i)/200, kappas) for i in range(59*200+1))
def c4_ok(K):
    k = kp[:]; k[6]+=K
    return c4_min(k) >= 0
# ---- (C3a) Lemma 12 k=0: S(sigma)=sum kappa_m * 0.5*psi((sigma+(2sigma-1)m)/2+1) <= -0.041 ----
def c3a_S(sigma, kappas):
    s = mp.mpf(0)
    for m,km in enumerate(kappas):
        s += km*mp.mpf('0.5')*mp.digamma((sigma+(2*sigma-1)*m)/2+1)
    return s
def c3a_max(kappas):
    return max(c3a_S(sigma0+(1-sigma0-mp.mpf('1e-9'))*mp.mpf(i)/2000, kappas) for i in range(2001))
def c3a_ok(K):
    k = kp[:]; k[6]+=K
    return c3a_max(k) <= -mp.mpf('0.041')
def bisect(ok, lo, hi, it=70):
    for _ in range(it):
        mid=(lo+hi)/2
        if ok(mid): lo=mid
        else: hi=mid
    return lo
# paper baselines
print("PAPER (C4) min margin =", mp.nstr(c4_min(kp),8))
print("PAPER (C3a) max S     =", mp.nstr(c3a_max(kp),8))
Kmax_c3a = bisect(c3a_ok, mp.mpf(0), mp.mpf('0.2'))
Kmax_c4  = bisect(c4_ok,  mp.mpf(0), mp.mpf('0.2'))
print("Kmax (C3a) =", mp.nstr(Kmax_c3a,12))
print("Kmax (C4)  =", mp.nstr(Kmax_c4,12))
Kbind = min(Kmax_c3a, Kmax_c4)
print("K binding  =", mp.nstr(Kbind,12), " (C3a binds)" if Kmax_c3a<Kmax_c4 else " (C4 binds)")
kap_max = sum(kp)+Kbind
print("kappa_max  =", mp.nstr(kap_max,12), " required 0.521015891482995")
print("kappa_max > required ?", bool(kap_max > mp.mpf('0.521015891482995')))
# margin detail at binding K for the binding constraint
k = kp[:]; k[6]+=Kbind
if Kmax_c3a<=Kmax_c4:
    print("at Kbind (C3a) max S =", mp.nstr(c3a_max(k),8))
else:
    print("at Kbind (C4) min margin =", mp.nstr(c4_min(k),8))
