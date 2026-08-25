# 2026-08-25 zfree-a0max-theta-reopt (claim #46)

Theta re-optimization for the A0_max objective (BTY-2026, arXiv:2603.21490 v1,
Lemma 5 / 138-relax). The paper fixes theta=1.1338 "via numerical
experimentation" (lines 528-529) for the 4.896 constant (Theorem 1); it never
re-optimizes theta for the A0_max objective. This claim does.

Result: A0_max is maximized at theta* = 0.057151961 with A0_max =
0.396708119308 (constant 2.520744979), up from 0.324204954225 (theta=1.1338,
claim #45). PARTIAL win: does NOT reach the full reopt target 0.420483467794
(constant 2.378214785, claim #40).

Why smaller theta helps: in g(A0;theta) = eta0^2*C(L(A0),L(A0);theta)/
[eps0*(2*sigma0-1)*w0(theta)], both C(L,L;theta) and w0(theta) -> 0 as
theta -> 0, but C -> 0 faster, so C/w0 (hence g) decreases and A0_max rises.
The optimum is a broad, flat interior peak near theta ~ 0.057 (A0_max ~ 0.3967
for theta in [0.05, 0.1]).

Files (append-only):
- relax138_theta.py         upward scan [1.1338,1.56] (machine-run-theta.txt)
- relax138_theta_down.py    downward scan [0.5,1.1338] (machine-run-theta-down.txt)
- relax138_theta_low.py     low-theta scan [0.05,0.55] (machine-run-theta-low.txt)
- relax138_theta_verify.py  refine theta* + verify all 7 constraints
                            (machine-run-theta-verify.txt)
- check.sh                  re-runs verify, asserts 6 conditions, CHECK PASS

Constraint set (from claim #44/#45, relax138_verify.py): [1] relaxed Lemma 5
g(A0;theta)<1 (binding, g=1 at A0_max*); [2] C(138,138;theta*) internal
(tight, ratio 0.989); [3] B(y)>0 (A0-independent, #44); [4] eq(22) W0-term;
[5] Lemma 6 A0>1/6; [6] Lemma 14 x1(m=1)>0; [7] Lemma 13 51*eta0^2/H^2<5e-13.
All hold at (A0_max*, theta*).

Scope: the 7-constraint A0_max sub-problem. The full Theorem-1 argument with
theta=0.0572 is NOT yet re-verified (theta is a global parameter in the paper,
Definitions 1-2); that is the follow-up.
