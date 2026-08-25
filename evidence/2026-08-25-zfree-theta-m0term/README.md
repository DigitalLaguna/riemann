# 2026-08-25 zfree-theta-m0term (claim #47)

m=0-term theta constraint for the A0_max objective (BTY-2026,
arXiv:2603.21490 v1). The paper's m=0-term Taylor bound (line 2210: "For all
0 <= x <= 2*theta*cot(theta) = 1.05923293 (at theta=1.1338), e^x -
(1+x+x^2/2+x^3/6) < x^4/18") is asserted on the theta-dependent range
[0, 2*theta*cot(theta)] of the m=0 integral (lines 2199-2207), so theta is
constrained to theta >= theta_min where 2*theta_min*cot(theta_min) = x_max
= sup{x: the bound holds on [0,x]}.

Result (machine-verified, verify_m0term.py, OVERALL: ALL PASS):
- x_max = 1.31432746286474 (first crossing of R(x) = e^x - (1+x+x^2/2+x^3/6)
  - x^4/18 > 0; grid 1e-3 + 80 bisection steps)
- theta_min = 0.980175494979203 (2*theta_min*cot(theta_min) = x_max;
  2*theta*cot(theta) strictly decreasing on (0,pi/2), so feasible set is
  theta >= theta_min)
- Bound HOLDS at theta_min (max[R - x^4/18] on [0, x_max] = 0.0 at x=0,
  200001-pt grid) and FAILS at claim #46's theta* = 0.057151961
  (2*theta*cot(theta) = 1.99782196124 > x_max; max violation
  0.16550656781 at x = 1.99782196124). #46's theta* is therefore infeasible
  in the full theorem (theta is a global parameter, Definitions 1-2).
- A0_max under the 7-constraint set (#44/#45/#46) plus theta >= theta_min:
  A0_max = 0.350566297741 (constant 2.852527486) at theta = theta_min
  (boundary; 2001-pt scan of [theta_min, pi/2) confirms the max is at the
  left endpoint). Up from #45's 0.324204954225 (3.084468596, theta=1.1338);
  below #46's infeasible 0.396708119308 (2.520744979) and the full reopt
  target 0.420483467794 (2.378214785, #40).
- All 7 constraints hold at (A0_max, theta_min): [1] g = 1 (binding);
  [2] C(138,138) internal ratio 0.9888 (A0_r2 = 0.352527892494 > A0_g,
  non-binding); [3] B(y)>0 (#44); [4] eq22 ratio 2.34e-14; [5] A0 > 1/6;
  [6] x1 = 0.9666 > 0; [7] 8.4e-28 < 5e-13.

Files (append-only):
- theta_min.py            x_max + theta_min (machine-run-theta-min.txt)
- m0term_theta_check.py   bound check at theta_min / theta* (machine-run-m0term-check.txt)
- a0max_at_thetamin.py    A0_max at paper theta / theta_min / theta* (machine-run-a0max-thetamin.txt)
- verify_m0term.py        full verification: 7 constraints + scan (machine-run-verify-m0term.txt)
- check.sh                re-runs verify_m0term.py, asserts 8 conditions, CHECK PASS

Scope: 7-constraint A0_max sub-problem + m=0-term constraint. The full
Theorem-1 argument at theta = theta_min is NOT yet re-verified (other
theta-dependent pieces may exist); that is the follow-up.
