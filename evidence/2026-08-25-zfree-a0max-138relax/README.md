# 2026-08-25 zfree-a0max-138relax (claim #45)

Relaxation of BTY-2026 (arXiv:2603.21490 v1) Lemma 5 fixed |z|>=138
requirement: apply Lemma 4 (Ford) with nu=r=L=(2*sigma0-1)/eta0 (the actual
lower bound) instead of the fixed integer 138. New binding constraint
g(A0) = eta0^2*C(L,L)/(eps0*(2*sigma0-1)*w(0)) < 1 (eps0=1/2000,
theta=1.1338) binds at A0_max = 0.324204954225 (constant 3.084468596), up
from 0.205470026688 (4.866889911, claim #42). Full reopt target
2.378214785 (A0=0.4204835, #40) NOT reached: the relaxed Lemma 5 constraint
is now the binding wall (0.3242 < 0.4204835).

Files (append-only):
- relax138_audit.py    g(A0) table + 200-iter bisection root (machine-run.txt)
- relax138_verify.py   all-constraint check at A0_new (machine-run-verify.txt)
- relax138_2d.py       2D scan: min C(nu,r) over nu,r<=L (machine-run-2d.txt)
- check.sh             re-runs verify, asserts 5 conditions, prints CHECK PASS

Paper anchors (lit/text/bellotti-trudgian-yang-2026.txt):
- Lemma 4 statement: line 507 (C(nu,r) formula; requires r > tan theta,
  Re z >= nu, |z| >= r)
- Lemma 5 proof: lines 627-632: "|z| >= Re z >= (2sigma0-1)/eta0 > 138.
  Thus, applying Lemma 4, ... eta0^2 C(138,138) ... < eps0/((2sigma0-1)w(0)
  m|delta_m+iy|^2) with eps0 = 1/2000"
- theta=1.1338, w(0)=5.672787598...: line ~520; T0=1e10, K=16,
  eta0=A0/log H, sigma0=1-A0/log(KH+T0): lines 532-535

2D scan note: grid min (nu=50.8, r=L+2.1e-4, C=21.81499267) vs C(L,L)
= 21.81499434: the difference is a grid-endpoint artifact (r exceeds L by
tan(theta)*1e-4) plus e^(-2*nu*theta) underflow (<1e-50 at 50 dps for
nu>50.8). C is analytically decreasing in nu and (per the 1D table) in r on
[tan theta, 138], so nu=r=L is the true minimizer; relative difference
7.7e-8, far below working precision.
