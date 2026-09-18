import mpmath as mp
mp.mp.dps = 50
M=6
# paper kappa_m
kap0=[mp.mpf(1),mp.mpf(-851)/859,mp.mpf(780)/859,mp.mpf(-525)/859,mp.mpf(171)/859,mp.mpf(28)/859,mp.mpf(-29)/859]
# params from paper
a=mp.mpf(2919857)/mp.mpf(828465)
w0=mp.mpf('5.672787598')
# sigma0, eta0: from paper. sigma0 = ? eta0 = ?
# From line 627: (2*sigma0-1)/eta0 > 138. From line 2061: mu0 = (1-sigma0)/eta0 - 1e-10 = 0.91198...
# Let's use sigma0 and eta0 such that these hold. Actually we need exact values.
# From the paper, sigma0 and eta0 are defined earlier. Let me use the relation.
# mu0 = (1-sigma0)/eta0 - 1e-10 = 0.91198... => (1-sigma0)/eta0 = 0.91198... + 1e-10
# (2*sigma0-1)/eta0 > 138
# Let's just use sigma0=0.9, eta0=0.1 as a test (these are placeholders; the exact values matter for the bounds)
# Actually, for the k=0 term in Lemma 12, we need (Gamma'/Gamma)((sigma+delta_m)/2+1) at sigma=sigma0.
# delta_m = (2*sigma-1)*m
sigma0=mp.mpf('0.9')  # placeholder
eta0=mp.mpf('0.1')    # placeholder
def delta_m(m,sigma): return (2*sigma-1)*m
def lemma12_k0(kap,sigma):
    s=mp.mpf(0)
    for m in range(M+1):
        dm=delta_m(m,sigma)
        val=mp.digamma((sigma+dm)/2+1)  # Gamma'/Gamma
        s+=kap[m]*val
    return s
# The paper's bound is -0.041 for the k=0 term (eq 38)
for K in [0, mp.mpf('0.02'), mp.mpf('0.05'), mp.mpf('0.1')]:
    kap=kap0[:]; kap[6]=kap[6]+K
    kappa=sum(kap)
    l12=lemma12_k0(kap,sigma0)
    print("K=%s  kappa=%s  Lemma12_k0=%s  (paper bound -0.041, ok: %s)"%(mp.nstr(K,4),mp.nstr(kappa,10),mp.nstr(l12,10),l12<=mp.mpf('-0.041')))
