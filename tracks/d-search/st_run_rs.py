# S(t) scan via Riemann-Siegel bare sum (track D). Fast (vectorized numpy).
# Z(t) ~ 2 sum_{n<=N(t)} cos(theta(t) - t log n)/sqrt(n), N(t)=floor(sqrt(t/2pi)).
# zeta(1/2+it) = e^{-i theta} Z(t); S(t) = (1/pi) unwrap(arg zeta).
# theta_asym per fetched wiki-rs-theta.html (verified vs exact 3.8e-19, tick 142).
# Error: bare-sum tail O(t^{-1/4}) in Z -> arg error O(t^{-1/4}/|Z|).
# NOTE (not NUMERIC): the bare-sum tail is an uncontrolled oscillation; a
# NUMERIC claim needs the full RS expansion or Arb acb_zeta.
import numpy as np
import sys, time

def theta_asym(t):
    t = np.asarray(t, dtype=float)
    return 0.5*t*np.log(t/(2*np.pi)) - t/2 - np.pi/8 + 1/(48*t) + 7/(5760*t**3)

def scan(t_start, t_end, step):
    n = int(round((t_end - t_start)/step)) + 1
    t = np.array([t_start + i*step for i in range(n)])
    th = theta_asym(t)
    N_max = int(np.floor(np.sqrt(t[-1]/(2*np.pi)))) + 1
    Z = np.zeros_like(t)
    t0 = time.time()
    for nn in range(1, N_max+1):
        mask = t >= 2*np.pi*(nn-1)**2
        Z[mask] += 2.0 * nn**(-0.5) * np.cos(th[mask] - t[mask]*np.log(nn))
    zeta_c = Z * (np.cos(th) - 1j*np.sin(th))
    args = np.angle(zeta_c)
    unwrapped = np.unwrap(args)
    S = unwrapped / np.pi
    imax = int(np.argmax(np.abs(S)))
    signs = np.sign(Z); signs[signs==0]=1
    changes = int(np.sum(np.abs(np.diff(signs))>0))
    maxjump = float(np.max(np.abs(np.diff(unwrapped))))
    print(f"grid: {n} points, t in [{t_start}, {t_end}], step {step}, RS bare sum (N_max={N_max})")
    print(f"max |S(t)| = {abs(S[imax]):.8f} at t = {t[imax]:.4f}")
    print("top-5 |S(t)|:")
    for k in np.argsort(np.abs(S))[::-1][:5]:
        print(f"  |S|={abs(S[k]):.8f} at t={t[k]:.4f}")
    print(f"zero count (sign changes of Z, approximate) = {changes}")
    print(f"max arg jump between grid points = {maxjump:.4f} rad (valid unwrap needs < pi)")
    print(f"elapsed {time.time()-t0:.0f}s")

if __name__ == "__main__":
    t_start = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    t_end   = float(sys.argv[2]) if len(sys.argv) > 2 else 1e6
    step    = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    scan(t_start, t_end, step)
