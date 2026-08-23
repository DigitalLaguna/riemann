# Riemann-Siegel machinery for the S(t) scan (track D).
# Verified tick 142 (evidence/2026-08-23-st-scan/st_check-run.txt, st_diag-run.txt):
#   Z(t) = e^{iθ(t)} ζ(1/2+it) is real (Im ~ 1e-47, mpmath 50 dps).
#   ζ(1/2+it) = e^{-iθ} 2*sum_{n<=N} cos(θ - t log n)/sqrt(n) + tail,
#   N = floor(sqrt(t/2π)); the bare-sum tail oscillates with amplitude
#   ~ (2π)^{1/4} t^{-1/4} (0.05-0.45 at t <= 1e5) -> use DIRECT zeta
#   evaluation for the scan on [1, 1e6]; RS sum only for t > 1e6.
# θ per fetched wiki-rs-theta.html (verbatim in evidence/2026-08-23-st-scan/):
#   θ(t) = arg Γ(1/4+it/2) - (log π/2) t
#   θ(t) ~ (t/2)log(t/2π) - t/2 - π/8 + 1/(48t) + 7/(5760t^3)
#   (asymptotic verified vs exact to 3.8e-19 at t=1e3, tick 142).
# mpmath 50 dps = development tool, not a rigorous machine.
import mpmath as mp
mp.mp.dps = 50

def theta(t):
    return mp.arg(mp.gamma(mp.mpf(1)/4 + mp.j*t/2)) - (t/2)*mp.log(mp.pi)

def theta_asym(t):
    return (t/2)*mp.log(t/(2*mp.pi)) - t/2 - mp.pi/8 + 1/(48*t) + 7/(5760*t**3)

def Z(t):
    """Hardy Z(t) = e^{iθ(t)} ζ(1/2+it), real on the critical line."""
    return mp.e**(mp.j*theta(t)) * mp.zeta(mp.mpf(1)/2 + mp.j*t)

def rs_bare(t):
    """Bare RS sum 2*sum_{n<=N} cos(θ - t log n)/√n, N = floor(√(t/2π)).
    Approximates Z(t) with an oscillating tail, amplitude ~ (2π)^{1/4} t^{-1/4}."""
    N = int(mp.floor(mp.sqrt(t/(2*mp.pi))))
    th = theta(t)
    s = mp.mpf(0)
    for n in range(1, N+1):
        s += mp.cos(th - t*mp.log(n)) / mp.sqrt(n)
    return 2*s

if __name__ == "__main__":
    print("t        Z(t)            Im(Z)      rs_bare      err")
    for t in [mp.mpf(10), mp.mpf(100), mp.mpf(1000), mp.mpf(10000), mp.mpf(100000)]:
        zt = Z(t)
        rb = rs_bare(t)
        print(f"{float(t):<8.0f} {float(mp.re(zt)):<15.8f} {float(mp.im(zt)):.2e} "
              f"{float(rb):<12.8f} {float(abs(zt-rb)):.3e}")
