import mpmath as mp, math, sys, time
t0=time.time()
mp.mp.dps = 60
N_FULL = 10**6          # full-scan upper bound (reduction + witness in this range)
N_CA   = 10**8          # CA-only upper bound
ROBIN_N0 = 5040        # Robin's inequality is for n > 5040

# ---------- primes ----------
def primes_upto(N):
    s = bytearray([1])*(N+1)
    s[0]=s[1]=0
    for i in range(2, int(N**0.5)+1):
        if s[i]:
            s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(N+1) if s[i]]
PR = primes_upto(200000)   # enough: CA numbers <=1e8 have small prime factors

# ---------- CA generation via Wikipedia eps-sweep ----------
def e_p(p, eps):
    # floor( ln(1 + (p-1)/(p^(1+eps) - p)) / ln p )
    val = mp.log(1 + (p-1)/(mp.power(p, 1+eps) - p)) / mp.log(p)
    return int(mp.floor(val))

def s_of_eps(eps):
    n = 1
    for p in PR:
        a = e_p(p, eps)
        if a == 0:
            break
        n *= p**a
    return n

# sweep eps from 1.0 down to 0.008, fine grid, collect distinct s(eps)
eps_hi, eps_lo = mp.mpf('1.0'), mp.mpf('0.008')
steps = 200000
seen = {}
prev = None
for i in range(steps+1):
    eps = eps_hi - (eps_hi-eps_lo)*mp.mpf(i)/mp.mpf(steps)
    n = s_of_eps(eps)
    if n != prev:
        seen[n] = True
        prev = n
ca_gen = sorted(seen.keys())
ca_gen_le1e8 = [n for n in ca_gen if n <= N_CA]
ca_gen_le1e6 = [n for n in ca_gen if n <= N_FULL]
print(f"[gen] distinct s(eps) values collected: {len(ca_gen)}; <=1e8: {len(ca_gen_le1e8)}; <=1e6: {len(ca_gen_le1e6)}")

# ---------- reference CA list from OEIS ----------
ca_ref = []
for line in open('b004394.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    parts=line.split()
    if len(parts)>=2 and parts[1].isdigit():
        ca_ref.append(int(parts[1]))
ca_ref_le1e8 = [n for n in ca_ref if n <= N_CA]
ca_ref_le1e6 = [n for n in ca_ref if n <= N_FULL]
print(f"[ref] OEIS CA <=1e8: {len(ca_ref_le1e8)}; <=1e6: {len(ca_ref_le1e6)}")

# F1: generated == OEIS for CA <= 1e6
F1 = (ca_gen_le1e6 == ca_ref_le1e6)
print(f"[F1] generated CA<=1e6 == OEIS CA<=1e6 : {F1}")
if not F1:
    gs=set(ca_gen_le1e6); rs=set(ca_ref_le1e6)
    print("   only-in-gen:", sorted(gs-rs)[:20])
    print("   only-in-ref:", sorted(rs-gs)[:20])
# also compare <=1e8 (informational)
F1b = (ca_gen_le1e8 == ca_ref_le1e8)
print(f"[F1b] generated CA<=1e8 == OEIS CA<=1e8 : {F1b}")
if not F1b:
    gs=set(ca_gen_le1e8); rs=set(ca_ref_le1e8)
    print("   only-in-gen:", sorted(gs-rs)[:20])
    print("   only-in-ref:", sorted(rs-gs)[:20])

# ---------- sigma sieve (exact integers) up to N_FULL ----------
sigma = [0]*(N_FULL+1)
for d in range(1, N_FULL+1):
    for m in range(d, N_FULL+1, d):
        sigma[m] += d
print(f"[sigma] sieve done, sigma[1000000]={sigma[1000000]}")

# F3: sigma == OEIS A000203 for n <= 10000
oeis_sigma = {}
for line in open('b000203.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    parts=line.split()
    if len(parts)>=2 and parts[0].isdigit() and parts[1].isdigit():
        oeis_sigma[int(parts[0])] = int(parts[1])
mism = [n for n in range(1,10001) if n in oeis_sigma and sigma[n]!=oeis_sigma[n]]
F3 = (len(mism)==0)
print(f"[F3] sigma==OEIS A000203 for n<=10000 : {F3} (mismatches={len(mism)} {mism[:5]})")

# F5: hand values
F5 = (sigma[12]==28 and sigma[5040]==19344)
print(f"[F5] sigma(12)={sigma[12]} (exp 28), sigma(5040)={sigma[5040]} (exp 19344) : {F5}")

# ---------- sigma for CA numbers > 1e6 (by factoring) ----------
def sigma_factor(n):
    m=n; res=1
    for p in PR:
        if p*p>m: break
        if m%p==0:
            s=1; pk=1
            while m%p==0:
                m//=p; pk*=p; s+=pk
            res*=s
    if m>1:
        res*=(1+m)
    return res

# ---------- R(n) = sigma(n)/(e^gamma * n * log log n), high precision ----------
EG = mp.e**mp.euler
def R_hp(n, sig):
    # returns R(n) as mp.mpf at 60 digits
    return mp.mpf(sig)/(EG*mp.mpf(n)*mp.log(mp.log(mp.mpf(n))))

# ---------- main: CA numbers > 5040, up to 1e8 ----------
ca_main = [n for n in ca_ref_le1e8 if n > ROBIN_N0]   # use OEIS ref (validated by F1)
results = []
for n in ca_main:
    sig = sigma[n] if n <= N_FULL else sigma_factor(n)
    r = R_hp(n, sig)
    results.append((n, sig, r))
results.sort(key=lambda x: -x[2])
print(f"\n[main] CA numbers >5040 and <=1e8: {len(ca_main)}")
print("[main] top 12 near-misses (largest R(n)=sigma/(e^gamma n loglog n)):")
for n,sig,r in results[:12]:
    print(f"   n={n:>10}  sigma={sig:>12}  R={mp.nstr(r,15)}  (1-R={mp.nstr(1-r,6)})")

# F6 witness: any R(n) >= 1 among CA numbers >5040 <=1e8?
hit_ca = [ (n,sig,r) for n,sig,r in results if r >= 1 ]
print(f"\n[F6-CA] CA witness R(n)>=1 among CA>5040<=1e8 : {len(hit_ca)} {hit_ca[:3]}")

# ---------- full float scan [5041, 1e6] for F2 reduction + F6 double-check ----------
import math as _m
eg_f = _m.exp(_m.euler if hasattr(_m,'euler') else 0.5772156649015328606)
# compute e^gamma in double
eg_f = _m.exp(0.57721566490153286060651209)
def R_float(n):
    return sigma[n]/(eg_f*n*_m.log(_m.log(n)))
best_n=None; best_r=-1
top=[]
for n in range(ROBIN_N0+1, N_FULL+1):
    r=R_float(n)
    if r>best_r:
        best_r=r; best_n=n
    top.append((r,n))
top.sort(reverse=True)
print(f"\n[F2] full float scan [5041,1e6]: argmax R at n={best_n}, R={best_r:.12f}")
ca_set=set(ca_ref)
print(f"[F2] argmax n={best_n} is CA? {best_n in ca_set}")
print("[F2] top 10 float near-misses (n, R, is_CA):")
for r,n in top[:10]:
    print(f"   n={n:>8} R={r:.12f} CA={n in ca_set}")
# F6 double-check in [5041,1e6] via float (margin to 1)
max_r_full = top[0][0]
print(f"[F6-full] max R over [5041,1e6] (float) = {max_r_full:.12f}; margin to 1 = {1-max_r_full:.3e}")

# F6 rigorous: recompute top-10 float candidates at 60 digits
print("[F6-rig] top-10 candidates at 60 digits:")
f6_hit=[]
for r,n in top[:10]:
    rr=R_hp(n, sigma[n])
    flag = "HIT>=1" if rr>=1 else ""
    if rr>=1: f6_hit.append(n)
    print(f"   n={n:>8} R={mp.nstr(rr,15)} {flag}")
print(f"[F6-rig] rigorous hits among top-10: {f6_hit}")

# ---------- F4: Robin explicit bound (2.2) ----------
# sigma(n) < e^gamma*n*log log n + 0.6482*n/log log n  for n>=3, n<=1e6
viol4=[]
for n in range(3, N_FULL+1):
    if n<=1: continue
    ll=_m.log(_m.log(n))
    if ll<=0: continue
    rhs=eg_f*n*ll + 0.6482*n/ll
    if sigma[n] >= rhs:
        viol4.append(n)
print(f"\n[F4] Robin explicit bound (2.2) violations in [3,1e6]: {len(viol4)} {viol4[:10]}")

print(f"\n[time] {time.time()-t0:.1f}s")
print("SUMMARY F1=%s F1b=%s F3=%s F5=%s F2_argmax_CA=%s F6_CA_hits=%d F6_full_margin=%.3e F4_viol=%d"%(
    F1,F1b,F3,F5,(best_n in ca_set),len(hit_ca),(1-max_r_full),len(viol4)))
