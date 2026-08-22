#!/usr/bin/env python3
"""Track B Phase-3 dominant-error-term audit.
Decompose the 0.20 bound Lambda <= t0 + y0^2/2 into per-component terms and
identify the binding component. Exact rational arithmetic (superset of Arb).
Pre-registered hit criterion (tick 85): one term >= 2x the sum of the others.
"""
from fractions import Fraction as F

# --- machine inputs (claim #8 / #9, archived) ---
t0 = F(186, 1000)          # 0.186  (exact, check.sh of claim #9)
y0 = F(16733, 100000)      # 0.16733 (exact, check.sh of claim #9)
f_final = F(376, 10000)    # 0.0376  (paper Table 1 row 2, machine-checked claim #8)
f_target = F(3, 100)       # 0.03    (paper's stated safety margin)
tloop_min_margin = F(48)   # 48      (tloop_020_run.txt final-column min, claim #9)
tloop_threshold = F(1)     # 1       (Abort iff min margin <= 1)
X_half = F(5000000194857, 2)  # X/2 = 2.5000000974e12 (left edge / 2)
T_RH = F(3 * 10**12)       # Platt-Trudgian RH verification height (claim #8)

# --- 1. bound decomposition (exact) ---
y0sq_over_2 = y0 * y0 / 2
bound = t0 + y0sq_over_2
frac_t0 = t0 / bound
frac_y0 = y0sq_over_2 / bound
ratio = t0 / y0sq_over_2   # asymptotics-term / (zero-free+zero-dynamics)-term

print("=== 1. BOUND DECOMPOSITION (exact rational) ===")
print(f"  t0            = {t0} = {float(t0):.11f}")
print(f"  y0^2/2        = {y0sq_over_2} = {float(y0sq_over_2):.11f}")
print(f"  bound         = {bound} = {float(bound):.11f}  (claim #9: 0.19999966445)")
assert bound == F(3999993289, 20000000000), "bound mismatch vs claim #9"
print(f"  fraction from t0 term      = {float(frac_t0)*100:.4f}%")
print(f"  fraction from y0^2/2 term  = {float(frac_y0)*100:.4f}%")
print(f"  ratio t0 / (y0^2/2)        = {float(ratio):.4f}x")

# --- 2. per-term error budget (component attribution) ---
# t0 term  -> ASYMPTOTICS (|f| bound sets the minimum feasible t0; barrier & RH
#             height are not binding, see margins below).
# y0^2/2   -> ZERO-FREE REGION (barrier height y0) converted by ZERO DYNAMICS.
term_asymptotics = t0
term_zfr_zd = y0sq_over_2
print("\n=== 2. PER-TERM ERROR BUDGET (component attribution) ===")
print(f"  ASYMPTOTICS (t0 term)                 = {float(term_asymptotics):.11f}")
print(f"  ZERO-FREE REGION + ZERO DYNAMICS (y0^2/2) = {float(term_zfr_zd):.11f}")
print(f"  sum of all terms                      = {float(bound):.11f}")

# --- 3. feasibility margins (how close each constraint is to being violated) ---
m_asym = f_final / f_target - 1          # |f| above target
m_bar  = tloop_min_margin / tloop_threshold - 1  # barrier margin above threshold
m_rh   = T_RH / X_half - 1               # RH height above required X/2
print("\n=== 3. FEASIBILITY MARGINS (relative slack before violation) ===")
print(f"  ASYMPTOTICS  |f|={float(f_final)} vs target {float(f_target)}: margin = {float(m_asym)*100:.2f}%")
print(f"  BARRIER      tloop min margin={tloop_min_margin} vs threshold {tloop_threshold}: margin = {float(m_bar)*100:.0f}%")
print(f"  RH HEIGHT    T_RH={float(T_RH):.3e} vs X/2={float(X_half):.3e}: margin = {float(m_rh)*100:.2f}%")

# --- 4. verdict (pre-registered hit criterion) ---
terms = {"ASYMPTOTICS": term_asymptotics, "ZERO-FREE+ZERO-DYN": term_zfr_zd}
top = max(terms, key=lambda k: terms[k])
top_val = terms[top]
rest = sum(v for k, v in terms.items() if k != top)
hit = top_val >= 2 * rest
print("\n=== 4. VERDICT (pre-registered: one term >= 2x sum of others) ===")
print(f"  dominant term = {top} = {float(top_val):.11f}")
print(f"  sum of others = {float(rest):.11f}")
print(f"  dominant / sum-of-others = {float(top_val/rest):.4f}x  (need >= 2x)")
print(f"  HIT = {hit}")
if hit:
    print("  => BINDING COMPONENT: ASYMPTOTICS (the |f| lower bound).")
    print("     Put compute on improving the |f| bound (hypothesis ii of ubc-0).")
else:
    print("  => NO single dominant term; audit is NOT well-posed (tick-85 kill condition).")
    print("     B must re-derive the 0.20 bound term-by-term from the Polymath15 code.")

# cross-check: prior-art prediction (paper line 165) says asymptotics is the bottleneck
print("\n=== 5. CROSS-CHECK vs prior art (paper line 165) ===")
print("  paper: hypothesis (ii) [asymptotics/|f|] 'close to the limit of our ability to")
print("  numerically verify'; hypothesis (iii) [barrier] 'does not present the main")
print("  bottleneck'. => prior art predicts ASYMPTOTICS binding. Audit agrees: "
      + ("YES" if hit and top == "ASYMPTOTICS" else "NO") + ".")
