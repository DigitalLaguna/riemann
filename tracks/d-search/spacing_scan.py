# Zero-spacing / Lehmer-pair scan (track D).
# Design + pre-registered falsification: evidence/2026-08-23-zerogap-scan/design.md
# Z(t) = re(e^{iθ_asym(t)} ζ(1/2+it)), real on the critical line (verified tick 142).
# Zeros by sign-change scan + bisection. mpmath = dev tool, NOT rigorous ->
# NOTE, not NUMERIC (needs Arb acb_zeta or an explicit error bound for NUMERIC).
import mpmath as mp
import sys, time, math

def theta_asym(t):
    return (t/2)*mp.log(t/(2*mp.pi)) - t/2 - mp.pi/8 + 1/(48*t) + 7/(5760*t**3)

def Z(t):
    z = mp.zeta(mp.mpf(0.5) + mp.j*t)
    return mp.re(mp.e**(mp.j*theta_asym(t)) * z)

def find_zeros(t_start, t_end, step, bisect_width=1e-9):
    n = int(round((t_end - t_start)/step)) + 1
    ts = [t_start + i*step for i in range(n)]
    Zs = []
    t0 = time.time()
    for i, t in enumerate(ts):
        Zs.append(float(Z(t)))
        if i % 20000 == 0 and i > 0:
            print(f"  grid {i}/{n} elapsed {time.time()-t0:.0f}s", file=sys.stderr)
    intervals = []
    for i in range(n-1):
        if Zs[i] == 0.0:
            intervals.append((i, i))
        elif Zs[i]*Zs[i+1] < 0:
            intervals.append((i, i+1))
    zeros = []
    for (ia, ib) in intervals:
        a, b = ts[ia], ts[ib]
        fa = Zs[ia]
        if ia == ib:
            zeros.append(a)
            continue
        for _ in range(60):
            if (b - a) < bisect_width:
                break
            m = 0.5*(a+b)
            fm = float(Z(m))
            if fa*fm <= 0:
                b, fb = m, fm
            else:
                a, fa = m, fm
        zeros.append(0.5*(a+b))
    zeros.sort()
    dedup = []
    for z in zeros:
        if not dedup or z - dedup[-1] > 1e-6:
            dedup.append(z)
    return dedup

def main():
    t_start = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    t_end   = float(sys.argv[2]) if len(sys.argv) > 2 else 1e4
    step    = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    dps     = int(sys.argv[4]) if len(sys.argv) > 4 else 15
    mp.mp.dps = dps
    t0 = time.time()
    zeros = find_zeros(t_start, t_end, step)
    n = len(zeros)
    gaps = []
    for i in range(n-1):
        t = zeros[i]
        gaps.append((zeros[i+1]-zeros[i]) * math.log(t/(2*math.pi)) / (2*math.pi))
    def max_rgap(r):
        best, bi = -1.0, -1
        for i in range(n-r):
            t = zeros[i]
            rg = (zeros[i+r]-zeros[i]) * math.log(t/(2*math.pi)) / (2*math.pi*r)
            if rg > best:
                best, bi = rg, i
        return best, bi
    maxg, ming = max(gaps), min(gaps)
    imax, imin = gaps.index(maxg), gaps.index(ming)
    # Lehmer pairs: s[i] = sign of Z on (zeros[i], zeros[i+1]); non-alternation
    # at zeros[i+1] iff s[i] == s[i+1]. (definition to verify, see design.md)
    signs = []
    for i in range(n-1):
        mid = 0.5*(zeros[i]+zeros[i+1])
        signs.append(1 if Z(mid) > 0 else -1)
    lehmer, lehmer_at = 0, []
    for i in range(len(signs)-1):
        if signs[i] == signs[i+1]:
            lehmer += 1
            lehmer_at.append(zeros[i+1])
    x = t_end/(2*math.pi)
    N_rvm = x*math.log(x) - x + 7/8
    mean_gap = sum(gaps)/len(gaps)
    print(f"range: [{t_start}, {t_end}], step {step}, {dps} dps")
    print(f"zero count N = {n} (Riemann-von Mangoldt ~ {N_rvm:.1f})")
    print(f"first zero = {zeros[0]:.6f} (known gamma_1 ~ 14.1347)")
    print(f"mean normalized gap = {mean_gap:.6f} (should be ~1)")
    print(f"max normalized gap = {maxg:.6f} at t = {zeros[imax]:.4f} (gap #{imax+1})")
    print(f"min normalized gap = {ming:.6f} at t = {zeros[imin]:.4f} (gap #{imin+1})")
    for r in [1,2,3]:
        mg, bi = max_rgap(r)
        print(f"max r={r} gap = {mg:.6f} at zero #{bi+1} (t={zeros[bi]:.4f})")
    print(f"Lehmer pairs = {lehmer}")
    for loc in lehmer_at[:10]:
        print(f"  Lehmer non-alternation at zero t ~ {loc:.4f}")
    print(f"elapsed {time.time()-t0:.0f}s")
    out = f"zeros_{t_start:g}_{t_end:g}.txt"
    with open(out, "w") as f:
        for z in zeros:
            f.write(f"{z:.10f}\n")
    print(f"wrote {out} ({n} zeros)")

if __name__ == "__main__":
    main()
