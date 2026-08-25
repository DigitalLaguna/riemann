# Find theta_min such that 2*theta*cot(theta) = x_max = 1.31432746286474
# (the m=0 term Taylor bound R(x)<x^4/18 holds on [0, 2*theta*cot theta] iff
#  2*theta*cot(theta) <= x_max, i.e. theta >= theta_min since 2*theta*cot(theta)
#  decreases in theta on (0, pi/2)).
import mpmath as mp
mp.mp.dps = 60
x_max = mp.mpf('1.31432746286474')
f = lambda th: 2*th/mp.tan(th) - x_max
# 2*th*cot(th) -> 2 as th->0+, -> 0 as th->pi/2. So f(0+)=2-x_max>0, f(pi/2-)= -x_max<0.
# root in (0, pi/2).
lo, hi = mp.mpf('1e-6'), mp.mpf(1.5707963)
for _ in range(200):
    m = (lo+hi)/2
    if f(m) > 0: lo = m
    else: hi = m
theta_min = (lo+hi)/2
print("theta_min (2*theta*cot(theta)=x_max) =", mp.nstr(theta_min, 15))
print("check: 2*theta_min*cot(theta_min) =", mp.nstr(2*theta_min/mp.tan(theta_min), 15))
# sanity: at theta=1.1338 (paper) and theta* (claim #46)
for th, lab in [(mp.mpf('1.1338'),'paper'),(mp.mpf('0.057151961'),'theta* #46')]:
    print(f"{lab}: 2*th*cot(th)={mp.nstr(2*th/mp.tan(th),10)}  -> bound "
          f"{'HOLDS' if 2*th/mp.tan(th) <= x_max else 'FAILS'} (th {'>=' if th>=theta_min else '<'} theta_min)")
