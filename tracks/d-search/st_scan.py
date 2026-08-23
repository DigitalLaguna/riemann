import mpmath as mp
mp.mp.dps = 50

def theta_exact(t):
    return mp.arg(mp.gamma(mp.mpf(1)/4 + mp.j*t/2)) - (t/2)*mp.log(mp.pi)

def theta_asym(t):
    return (t/2)*mp.log(t/(2*mp.pi)) - t/2 - mp.pi/8 - 1/(48*t) + 1/(7680*t**3)

def Z_rs(t):
    N = int(mp.floor(mp.sqrt(t/(2*mp.pi))))
    th = theta_exact(t)
    s = mp.mpf(0)
    for n in range(1, N+1):
        s += mp.cos(th - t*mp.log(n)) / mp.sqrt(2*n)
    return 2*s

print("t      |dtheta|  |zeta|   |rs|     rel_err(zeta vs rs)")
for t in [10, 100, 1000, 10000, 100000]:
    zeta = mp.zeta(mp.mpf(1)/2 + mp.j*t)
    rs   = Z_rs(t) * mp.e**(mp.j*theta_exact(t))
    dth  = float(abs(theta_exact(t) - theta_asym(t)))
    print(f"{t:<7} {dth:.3e}  {float(abs(zeta)):.6f}  {float(abs(rs)):.6f}  {float(abs(zeta-rs)/abs(zeta)):.3e}")
