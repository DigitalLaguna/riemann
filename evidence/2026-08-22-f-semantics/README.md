# Track B — semantics of New_abeff_largex_bounds vs Table 1 |f|-column (claim #11)

Question (flagged in HANDOFF tick 72): the dbn program prints "Lower Lemma bound
0.519046677344531" at Table 1 row 2 (t=0.186, y=0.16733, N=N0=630783), but the
paper's Table 1 lists the |f| lower bound for exactly this row as 0.0376. Systematic
~15x ratio on rows 1-3 (15.3x, 13.8x, 15.2x). Is 0.519 a bound on |f|, on
|E_{t,5}*f|, or on a partial sum?

## Resolution (machine-verified, this tick)

Direct 70-digit evaluation (direct_f.py, exact formulas from dbn/Writeup/debruijn.tex:
alpha-form, sn-def, kappa-def, lambda-def, ft-def, bn-def, logM) at the row-2 point:

    Re(s_*) = 1.08696672156, Im(s_*) = -315391.573042
    |gamma| = 0.404313572548
    |sum_beta| = 1.12024756652, |gamma*sum_alpha| = 1.12041820594
    |f| (direct) = 1.06811120997
    |E_{t,5}| (primes 2,3,5) = 1.09517191255
    |E_{t,11}| (primes 2,3,5,7,11) = 0.923886987371

Program (unmodified dbn C code, /tmp/abeff, same binary as the 0.20 run):
    m=0 (no mollifier):  -0.394278366241688   (negative: useless without the mollifier)
    m=3 (primes 2,3,5 = paper's E_{t,5}):  0.466572104328199
    m=5 (primes 2,3,5,7,11; used in the 0.20 run):  0.519046677344531

Verdict: ALL of {0.0376 (paper final), 0.4666 (m=3), 0.5190 (m=5)} are rigorous
lower bounds on the SAME quantity |f_t(N0+iy0)|; the true value is 1.06811120997...
Every bound <= true value (machine check: True). The ~15x is NOT the Euler factor
(|E_{t,5}| = 1.095, |E_{t,11}| = 0.924, both ~1). Interpretation:
  - the program computes the Lemma-trib2 ("Euler 2-mollifier", improved triangle
    inequality) component of the paper's |f| analysis — a tight intermediate bound;
    without the mollifier it is negative (-0.394), so the mollifier carries the weight;
  - the paper's Table 1 value 0.0376 is the FINAL bound after the full O-term
    analysis (e_A + e_B + e_{C,0} from ratio-form-eff plus tails), the value the
    proof actually uses, with the paper's stated >= 0.03 safety margin.
Consequence for claim #9: the 0.20 verdict (PASS, program 0.519 >= 0.03) is sound;
the paper itself publishes 0.0376 >= 0.03 for exactly these parameters, so the
hypothesis-(ii) leg of Theorem 1.2 is secured by the paper's own published analysis.
Caveat (why NOTE, not NUMERIC): the direct evaluation is mpmath at 70 digits, not
Arb balls; per-op error < 1e-65 over 630783 terms is argued, not carried as ball
radii. Arb port = the one-tick promotion step (check.sh ready).
