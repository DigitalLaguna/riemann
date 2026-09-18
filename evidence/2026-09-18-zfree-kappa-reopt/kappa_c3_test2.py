import mpmath as mp
mp.mp.dps = 50
M=6
kap0=[mp.mpf(1),mp.mpf(-851)/859,mp.mpf(780)/859,mp.mpf(-525)/859,mp.mpf(171)/859,mp.mpf(28)/859,mp.mpf(-29)/859]
sigma0=mp.mpf('0.9935164')
def delta_m(m,sigma): return (2*sigma-1)*m
def k0term(kap,sigma):
    s=mp.mpf(0)
    for m in range(M+1):
        dm=delta_m(m,sigma)
        s+=kap[m]*mp.digamma((sigma+dm)/2+1)
    return s
# max over sigma in [sigma0, 1) of k0term
def k0max(kap):
    best=mp.mpf('-inf')
    for i in range(200):
        sigma=sigma0+(1-sigma0)*mp.mpf(i)/200
        v=k0term(kap,sigma)
        if v>best: best=v
    return best
print("paper kappa: k0max =", mp.nstr(k0max(kap0),12), " (paper bound -0.041)")
# find max K such that k0max <= -0.041
lo=mp.mpf(0); hi=mp.mpf('0.1')
for _ in range(40):
    mid=(lo+hi)/2
    kap=kap0[:]; kap[6]=kap[6]+mid
    if k0max(kap)<=mp.mpf('-0.041'): lo=mid
    else: hi=mid
Kmax=(lo+hi)/2
kap=kap0[:]; kap[6]=kap[6]+Kmax
kappa=sum(kap)
print("Kmax (Lemma12 k=0 only) =", mp.nstr(Kmax,10))
print("kappa at Kmax =", mp.nstr(kappa,12))
print("kappa_required = 0.521015891482995")
print("kappa at Kmax > kappa_required ?", kappa>mp.mpf('0.521015891482995'))
