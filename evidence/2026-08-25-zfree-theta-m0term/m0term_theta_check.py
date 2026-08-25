# m=0 term Taylor bound check across theta (BTY-2026, arXiv:2603.21490 v1, line 2210)
# Paper: "For all 0 <= x <= 2*theta*cot(theta) = 1.05923293 (at theta=1.1338),
#   one has e^x - (1+x+x^2/2+x^3/6) < x^4/18"
# This bound is used to derive the m=0 term lower bound C1(mu) (eq 42).
# It is theta-dependent (range [0, 2*theta*cot theta]) but A0-independent.
# Question: does it hold at theta* = 0.057151961 (claim #46)?
import mpmath as mp
mp.mp.dps = 60

def R(x):
    return mp.e**x - (1 + x + x**2/2 + x**3/6)

def range_end(theta):
    return 2*theta/mp.tan(theta)   # 2*theta*cot(theta)

def max_violation(theta, n=200001):
    # max of R(x) - x^4/18 on [0, 2*theta*cot(theta)]
    b = range_end(theta)
    mx = mp.mpf(-1); mx_x = mp.mpf(0)
    for i in range(n):
        x = b*i/(n-1)
        v = R(x) - x**4/18
        if v > mx:
            mx = v; mx_x = x
    return b, mx, mx_x

# find x_max = sup{x : R(x) < x^4/18}
lo, hi = mp.mpf(0), mp.mpf(5)
# R(x)-x^4/18 at x=0 is 0; find where it first goes positive and stays
# scan to find the crossing
xs = [mp.mpf(i)/1000 for i in range(0, 5001)]
cross = None
for x in xs:
    if R(x) - x**4/18 > 0:
        cross = x; break
print("first x with R(x)-x^4/18 > 0 (grid 1e-3):", mp.nstr(cross, 12) if cross else "none in [0,5]")
# refine crossing by bisection between last negative and first positive
if cross is not None:
    a = cross - mp.mpf(1)/1000; b2 = cross
    for _ in range(80):
        m = (a+b2)/2
        if R(m) - m**4/18 > 0: b2 = m
        else: a = m
    x_max = (a+b2)/2
    print("x_max (R(x)=x^4/18 crossing) =", mp.nstr(x_max, 15))

for th, label in [(mp.mpf('1.1338'), 'paper theta=1.1338'),
                  (mp.mpf('0.057151961'), 'theta* (claim #46)')]:
    b, mx, mx_x = max_violation(th)
    print(f"{label}: 2*theta*cot(theta) = {mp.nstr(b,12)}; "
          f"max[R(x)-x^4/18] on [0,b] = {mp.nstr(mx,12)} at x={mp.nstr(mx_x,12)}; "
          f"BOUND {'HOLDS' if mx <= 0 else 'FAILS'}")
