# S(t) scan runner (track D). S(t) = (1/pi) arg zeta(1/2+it) on a t-grid via
# DIRECT mpmath zeta (30 dps); unwraps the argument; reports max |S(t)| and an
# approximate zero count (sign changes of Z(t)=e^{iθ}zeta, real on the line).
# mpmath = development tool, NOT rigorous -> result is a NOTE, not NUMERIC.
# θ_asym per fetched wiki-rs-theta.html (verified vs exact to 3.8e-19, tick 142).
import mpmath as mp
import numpy as np
import sys, time

DPS = 30
mp.mp.dps = DPS

def theta_asym(t):
    return (t/2)*mp.log(t/(2*mp.pi)) - t/2 - mp.pi/8 + 1/(48*t) + 7/(5760*t**3)

def scan(t_start, t_end, step):
    n = int(round((t_end - t_start)/step)) + 1
    args, Zreals = [], []
    t0 = time.time()
    for i in range(n):
        t = t_start + i*step
        z = mp.zeta(mp.mpf(0.5) + mp.j*t)
        args.append(mp.arg(z))
        Zreals.append(mp.re(mp.e**(mp.j*theta_asym(t)) * z))
        if i % 20000 == 0 and i > 0:
            print(f"  progress {i}/{n} ({100*i/n:.0f}%) elapsed {time.time()-t0:.0f}s", file=sys.stderr)
    args_np = np.array([float(a) for a in args])
    Z_np = np.array([float(x) for x in Zreals])
    unwrapped = np.unwrap(args_np)
    S = unwrapped / np.pi
    ts_np = np.array([t_start + i*step for i in range(n)])
    imax = int(np.argmax(np.abs(S)))
    signs = np.sign(Z_np); signs[signs == 0] = 1
    changes = int(np.sum(np.abs(np.diff(signs)) > 0))
    maxjump = float(np.max(np.abs(np.diff(unwrapped))))
    print(f"grid: {n} points, t in [{t_start}, {t_end}], step {step}, {DPS} dps")
    print(f"max |S(t)| = {abs(S[imax]):.8f} at t = {ts_np[imax]:.4f}")
    print("top-5 |S(t)|:")
    for k in np.argsort(np.abs(S))[::-1][:5]:
        print(f"  |S|={abs(S[k]):.8f} at t={ts_np[k]:.4f}")
    print(f"zero count (sign changes of Z, approximate) = {changes}")
    print(f"max arg jump between grid points = {maxjump:.4f} rad (valid unwrap needs < pi)")
    print(f"elapsed {time.time()-t0:.0f}s")

if __name__ == "__main__":
    t_start = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    t_end   = float(sys.argv[2]) if len(sys.argv) > 2 else 1e6
    step    = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    scan(t_start, t_end, step)
