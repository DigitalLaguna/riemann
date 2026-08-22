import mpmath as mp, math
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
# superabundant numbers <= 1e8 from A004394
sa=[]
for line in open('b004394.txt'):
    line=line.strip()
    if not line or line.startswith('#'): continue
    p=line.split()
    if len(p)>=2 and p[1].isdigit(): sa.append(int(p[1]))
sa_le1e8=[n for n in sa if n<=10**8]
print("superabundant <=1e8:",len(sa_le1e8))
res=[]
for n in sa_le1e8:
    if n<=1: continue
    r=R_hp(n)
    res.append((n,sigma_factor(n),r))
res.sort(key=lambda x:-x[2])
print("top 15 superabundant near-misses R(n)=sigma/(e^gamma n loglog n):")
for n,sig,r in res[:15]:
    isCA = n in [2,6,12,60,120,360,2520,5040,55440,720720,1441440,4324320,21621600]
    print(f"  n={n:>10} sigma={sig:>12} R={mp.nstr(r,15)} 1-R={mp.nstr(1-r,6)} CA={isCA}")
print()
print("MAX R over superabundant <=1e8:",mp.nstr(res[0][2],15),"at n=",res[0][0])
print("any R>=1 (witness)?",[n for n,sig,r in res if r>=1])
# also: is the max over ALL n<=1e8 at this superabundant number? (proof: yes, see reduction)
# cross-check: full scan up to 1e6 already gave argmax 10080 R=0.985818611972329
print("R(10080) recompute:",mp.nstr(R_hp(10080),15))
