# S(t) scan step 1: Riemann-Siegel implementation check (track D, tick 142).
# F1: which of {e^{+iθ}, e^{-iθ}} x {2*sum cos(θ-t log n)/√n, .../√(2n)}
#     reproduces zeta(1/2+it)?  F2: θ_exact vs θ_asym (wiki coefficients).
# mpmath 50 dps = development tool, not a rigorous machine.
import mpmath as mp
mp.mp.dps = 50

def theta_exact(t):
    # fetched wiki-rs-theta.html: θ(t) = arg Γ(1/4 + it/2) - (log π/2) t
    return mp.arg(mp.gamma(mp.mpf(1)/4 + mp.j*t/2)) - (t/2)*mp.log(mp.pi)

def theta_asym(t):
    # fetched wiki-rs-theta.html: θ(t) ~ (t/2)log(t/2π) - t/2 - π/8 + 1/(48t) + 7/(5760t^3)
    return (t/2)*mp.log(t/(2*mp.pi)) - t/2 - mp.pi/8 + 1/(48*t) + 7/(5760*t**3)

def rs_sum(t, sqrt2):
    N = int(mp.floor(mp.sqrt(t/(2*mp.pi))))
    th = theta_exact(t)
    s = mp.mpf(0)
    for n in range(1, N+1):
        denom = mp.sqrt(2*n) if sqrt2 else mp.sqrt(n)
        s += mp.cos(th - t*mp.log(n)) / denom
    return 2*s

print("t        err(+iθ,1/√n)  err(+iθ,1/√2n)  err(-iθ,1/√n)  err(-iθ,1/√2n)  best")
for t in [mp.mpf(10), mp.mpf(100), mp.mpf(1000), mp.mpf(10000), mp.mpf(100000)]:
    z = mp.zeta(mp.mpf(1)/2 + mp.j*t)
    th = theta_exact(t)
    errs = []
    for s2 in [False, True]:
        S = rs_sum(t, s2)
        for sign in [+1, -1]:
            errs.append(float(abs(z - mp.e**(mp.j*sign*th)*S)))
    best = min(range(4), key=lambda i: errs[i])
    sgn = '+' if best % 2 == 0 else '-'
    cf = '1/√n' if best < 2 else '1/√(2n)'
    print(f"{float(t):<8.0f} {errs[0]:.3e} {errs[1]:.3e} {errs[2]:.3e} {errs[3]:.3e}  "
          f"e^({sgn}iθ) {cf}  err={errs[best]:.3e}")

print()
print("F2 theta check: |θ_exact - θ_asym| (mod 2π)")
for t in [mp.mpf(1000), mp.mpf(10000), mp.mpf(100000)]:
    d = (theta_exact(t) - theta_asym(t)) % (2*mp.pi)
    if d > mp.pi:
        d -= 2*mp.pi
    print(f"t={float(t):<8.0f} {float(abs(d)):.3e}")
