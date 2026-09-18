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
sigma0 = mp.mpf('0.9935164'); eta0 = mp.mpf('0.0071093')
kp = [mp.mpf(1), -mp.mpf(851)/859, mp.mpf(780)/859, -mp.mpf(525)/859,
      mp.mpf(171)/859, mp.mpf(28)/859, -mp.mpf(29)/859]
def dm(m, km): return (2*sigma0-1)*m if km < 0 else mp.mpf(m)
def S(sigma, kappas):
    return sum(km*mp.mpf('0.5')*mp.digamma((sigma+(2*sigma-1)*m)/2+1) for m,km in enumerate(kappas))
def Smax(kappas, N=4000):
    best=(-mp.inf, None)
    for i in range(N+1):
        sigma=sigma0+(1-sigma0-mp.mpf('1e-9'))*mp.mpf(i)/N
        v=S(sigma,kappas)
        if v>best[0]: best=(v,sigma)
    return best
def c4_margin(u,kappas):
    kap=sum(kappas); s=sum(km*mp.e**(-dm(m,km)*u) for m,km in enumerate(kappas))
    return w(eta0*u)*s-kap*w0
def c4min(kappas, N=12000):
    best=(mp.inf, None)
    for i in range(1,N+1):  # skip u=0 (margin=0 exactly)
        u=mp.mpf(59*i)/N
        v=c4_margin(u,kappas)
        if v<best[0]: best=(v,u)
    return best
print("PAPER: max S =", mp.nstr(Smax(kp)[0],10), "at sigma=", mp.nstr(Smax(kp)[1],8))
print("PAPER: 2*maxS =", mp.nstr(2*Smax(kp)[0],10), " (tick268 formula)")
print("PAPER: (C4) min margin(u>0) =", mp.nstr(c4min(kp)[0],10), "at u=", mp.nstr(c4min(kp)[1],6))
for K in [mp.mpf('0.002454'), mp.mpf('0.00878'), mp.mpf('0.0383')]:
    k=kp[:]; k[6]+=K
    ms,ss=Smax(k); mc,uc=c4min(k)
    print(f"K={mp.nstr(K,6)}: maxS={mp.nstr(ms,10)}@sig{mp.nstr(ss,6)} | C4min={mp.nstr(mc,10)}@u{mp.nstr(uc,5)} | kappa={mp.nstr(sum(k),10)}")
