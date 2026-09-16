# Downstream propagation of the pinned A0_max (track C, BTY-2026).
# Combines #40 (re-optimized Lemma-1 final line, A_final) and #54 (pinned A0_max)
# to give the effective zero-free-region constant.
#
# Logic (reopt README, evidence/2026-08-24-zfree-reopt/README.md):
#   lemmas 5-14 are stated with eta <= A0/log t, so the region constant must
#   satisfy A <= A0. Effective constant = min(A_final, A0).
#   A_final = re-optimized Lemma-1 lower bound on eta*log t (#40).
#   A0      = max A0 such that lemmas 5-14 hold (#54, pinned).
#   If A_final > A0, then A0 binds and the headline is 1/A0.
import mpmath as mp
mp.mp.dps = 50

# From #40 (evidence/2026-08-24-zfree-reopt/machine-run.txt, CASE 3):
A_final = mp.mpf('0.420483467794')
# From #54 (evidence/2026-09-16-zfree-a0max-pin/machine-run.txt, ESTIMATE):
A0_max  = mp.mpf('0.392113247395366294')
# Paper's A0 (table line 545, Lemma 1 A0 = (4.8596)^-1):
A0_paper = mp.mpf(1)/mp.mpf('4.8596')

effective = min(A_final, A0_max)
headline  = 1/effective
improvement_vs_paper = (1/A0_paper)/headline  # = A0_paper... no, = (1/A0_paper)/(1/A0_max) = A0_max/A0_paper
improvement_vs_paper = A0_max/A0_paper

print(f"A_final  = {mp.nstr(A_final,15)}   (#40, re-optimized Lemma-1)")
print(f"A0_max   = {mp.nstr(A0_max,18)}   (#54, pinned)")
print(f"A_final > A0_max? {A_final > A0_max}")
print(f"effective = min(A_final, A0_max) = {mp.nstr(effective,18)}")
print(f"headline  = 1/effective = {mp.nstr(headline,15)}")
print(f"paper A0  = {mp.nstr(A0_paper,15)}  (1/4.8596)")
print(f"improvement over paper (A0_max/A0_paper) = {mp.nstr(improvement_vs_paper,6)}x")
ok = (A_final > A0_max) and (effective == A0_max) and (headline == 1/A0_max)
print(f"CHECK downstream effective constant: {'PASS' if ok else 'FAIL'}")
