# A0_max pinning (track C, BTY-2026 exact m=0 term)
Supersedes #51 (evidence/2026-09-15-zfree-theta-cross, width 4.12e-11).
Same pipeline; bisection 30 -> 46 iters (width 0.0443/2^46 ~ 6.3e-16 in theta),
verification unchanged (50dps fine 7x9 grid, 100dps corner, 7 constraints).
Sign robustness: probe slope ~2.2e-3/unit theta near the crossing, so the last
bisection step changes the probe value by ~2.2e-18 >> 30dps rounding ~1e-28.
