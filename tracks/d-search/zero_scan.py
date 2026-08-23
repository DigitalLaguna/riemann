# Zero-spacing scan (track D). Zeros γ_n of ζ on the critical line via sign changes of
# Z(t) = re(e^{iθ(t)} ζ(1/2+it)) + bisection. θ_asym = Riemann-Siegel asymptotic
# (verified vs exact to 3.8e-19, tick 142). mpmath = development tool, NOT rigorous
# -> NOTE, not NUMERIC. Design + pre-registered falsification: zero-spacing-design.md.
import mpmath as mp
import sys, time

DPS = 30
mp.mp.dps = DPS

def theta_asym(t):
    return (t/2)*mp.log(t/(2*mp.pi)) - t/2 - mp.pi/8 + 1/(48*t) + 7/(5760*t**3)

def Z(t):
    return mp.re(mp.e**(mp.j*theta_asym(t)) * mp.zeta(mp.mpf(0.5) + mp.j*t))

def find_zeros(t_start, t_end, step):
    zeros = []
    n = int(round((t_end - t_start)/step))
    prev_t = t_start
    prev_z = Z(prev_t)
    t0 = time.time()
    for i in range(1, n+1):
        t = t_start + i*step
        z = Z(t)
        if i % 5000 == 0:
            print(f"  coarse {i}/{n} elapsed {time.time()-t0:.0f}s", file=sys.stderr)
        if prev_z*z < 0:
            a, b, fa = prev_t, t, prev_z
            for _ in range(40):
                m = (a+b)/2
                fm = Z(m)
                if fa*fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
                if b - a < 1e-10:
                    break
            zeros.append((a+b)/2)
        prev_t, prev_z = t, z
    return zeros

def rvn(T):
    return (T/(2*mp.pi))*mp.log(T/(2*mp.pi)) - T/(2*mp.pi) - mp.mpf(1)/8

if __name__ == "__main__":
    t_start = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    t_end   = float(sys.argv[2]) if len(sys.argv) > 2 else 1000.0
    step    = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
    t0 = time.time()
    zeros = find_zeros(t_start, t_end, step)
    gaps = [float((zeros[i+1]-zeros[i]) * mp.log(zeros[i]) / (2*mp.pi)) for i in range(len(zeros)-1)]
    imax = max(range(len(gaps)), key=lambda k: gaps[k])
    imin = min(range(len(gaps)), key=lambda k: gaps[k])
    print(f"range: [{t_start}, {t_end}], coarse step {step}, {DPS} dps")
    print(f"zero count = {len(zeros)} (RvM main term = {float(rvn(t_end)):.2f}, tolerance ±3)")
    print("first 10 zeros:")
    for z in zeros[:10]:
        print(f"  {float(z):.6f}")
    print(f"max normalized gap g = {gaps[imax]:.6f} between zeros {float(zeros[imax]):.4f} and {float(zeros[imax+1]):.4f}")
    print(f"min normalized gap g = {gaps[imin]:.6f} between zeros {float(zeros[imin]):.4f} and {float(zeros[imin+1]):.4f}")
    print("top-5 largest gaps:")
    for k in sorted(range(len(gaps)), key=lambda k: -gaps[k])[:5]:
        print(f"  g={gaps[k]:.6f} at zero {float(zeros[k]):.4f}")
    print("top-5 smallest gaps:")
    for k in sorted(range(len(gaps)), key=lambda k: gaps[k])[:5]:
        print(f"  g={gaps[k]:.6f} at zero {float(zeros[k]):.4f}")
    print(f"elapsed {time.time()-t0:.0f}s")
