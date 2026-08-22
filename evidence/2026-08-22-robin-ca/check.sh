#!/bin/bash
# Track D: Robin-criterion near-misses over superabundant/CA numbers, n<=1e8.
# Re-runs the computation and asserts the recorded values. Exit 0 = PASS.
set -e
cd "$(dirname "$0")"
python3 - <<'PY'
import mpmath as mp, math, sys
mp.mp.dps=60
EG=mp.e**mp.euler
def primes_upto(N):
    s=bytearray([1])*(N+1); s[0]=s[1]=0
    for i in range(2,int(N**0.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(N+1) if s[i]]
PR=primes_upto(200000)
def sigma_factor(n):
    m=n; res=1
    for p in PR:
        if p*p>m: break
        if m%p==0:
            s=1; pk=1
            while m%p==0:
                m//=p; pk*=p; s+=pk
            res*=s
    if m>1: res*=(1+m)
    return res
def R_hp(n):
    return mp.mpf(sigma_factor(n))/(EG*mp.mpf(n)*mp.log(mp.log(mp.mpf(n))))
ok=True
def chk(name,cond,detail=""):
    global ok
    print(("PASS" if cond else "FAIL"),name,detail)
    ok=ok and cond

# --- C1: CA generation (eps-sweep) == OEIS A004490 (excluding trivial 1) ---
def e_p(p,eps):
    return int(mp.floor(mp.log(1+(p-1)/(mp.power(p,1+eps)-p))/mp.log(p)))
def s_of_eps(eps):
    n=1
    for p in PR:
        a=e_p(p,eps)
        if a==0: break
        n*=p**a
    return n
eps_hi,eps_lo=mp.mpf('1.0'),mp.mpf('0.008'); steps=200000
seen=set(); prev=None
for i in range(steps+1):
    eps=eps_hi-(eps_hi-eps_lo)*mp.mpf(i)/mp.mpf(steps)
    n=s_of_eps(eps)
    if n!=prev: seen.add(n); prev=n
gen=sorted(x for x in seen if 1<x<=10**8)
ca=[]
for line in open('b004490.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    p=line.split()
    if len(p)>=2 and p[1].isdigit(): ca.append(int(p[1]))
ca_le1e8=[n for n in ca if n<=10**8]
chk("C1 CA-gen==A004490 (<=1e8, excl 1)", gen==ca_le1e8, f"gen={len(gen)} ref={len(ca_le1e8)}")

# --- C2: sigma sieve == OEIS A000203 for n<=10000 ---
N=10**6
sigma=[0]*(N+1)
for d in range(1,N+1):
    for m in range(d,N+1,d): sigma[m]+=d
oeis={}
for line in open('b000203.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    p=line.split()
    if len(p)>=2 and p[0].isdigit() and p[1].isdigit(): oeis[int(p[0])]=int(p[1])
mism=[n for n in range(1,10001) if n in oeis and sigma[n]!=oeis[n]]
chk("C2 sigma==A000203 (n<=10000)", len(mism)==0, f"mism={len(mism)}")
chk("C2b hand sigma(12)=28, sigma(5040)=19344", sigma[12]==28 and sigma[5040]==19344)

# --- C3: near-miss over superabundant 5040<n<=1e8 ---
sa=[]
for line in open('b004394.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    p=line.split()
    if len(p)>=2 and p[1].isdigit(): sa.append(int(p[1]))
sa_main=[n for n in sa if 5040<n<=10**8]
res=sorted(((n,sigma_factor(n),R_hp(n)) for n in sa_main), key=lambda x:-x[2])
n0,sig0,r0=res[0]
chk("C3 near-miss n=10080", n0==10080, f"n={n0}")
chk("C3b R(10080)=0.985818611972329 (12dp)", mp.nstr(r0,13)=="0.9858186119723", mp.nstr(r0,15))
chk("C3c sigma(10080)=39312", sig0==39312, f"sigma={sig0}")
# --- C4: no witness R(n)>=1 for superabundant 5040<n<=1e8 ---
hits=[n for n,sig,r in res if r>=1]
chk("C4 no witness R>=1 (superabundant 5040<n<=1e8)", len(hits)==0, f"hits={hits}")
# --- C5: full float scan [5041,1e6] argmax is 10080 and <1 (reduction sanity) ---
eg_f=math.exp(0.57721566490153286060651209)
best_n=None; best_r=-1
for n in range(5041,N+1):
    r=sigma[n]/(eg_f*n*math.log(math.log(n)))
    if r>best_r: best_r=r; best_n=n
chk("C5 full-scan[5041,1e6] argmax=10080", best_n==10080, f"n={best_n} R={best_r:.12f}")
chk("C5b full-scan max R<1 (margin)", best_r<1.0, f"margin={1-best_r:.3e}")
# --- C6: reduction proof sanity: R(n)<=R(s(n)) for sample n (s(n)=largest superabundant<=n) ---
sa_set=sorted(set(sa))
import bisect
def s_of(n):
    i=bisect.bisect_right(sa_set,n)-1
    return sa_set[i]
bad=0
for n in [5041,7000,10079,10080,50000,100000,999999,1000000]:
    if R_hp(n)>R_hp(s_of(n))+mp.mpf('1e-40'): bad+=1
chk("C6 reduction R(n)<=R(s(n)) sample", bad==0, f"violations={bad}")
print()
print("G(10080)=",mp.nstr(mp.mpf(sig0)/(mp.mpf(n0)*mp.log(mp.log(mp.mpf(n0)))),15))
print("e^gamma=",mp.nstr(EG,15))
print("VERDICT:", "ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
PY
