"""
Track B: H_t(z) computation, first verification step.

Definition (from Polymath15 code, dbn_upper_bound/python/mputility.py):
  H_t(z) = int_0^inf  exp(t*u^2) * phi(u) * cos(z*u) du
  phi(u) = sum_{n>=1} [2*pi^2*n^4*exp(9u) - 3*pi*n^2*exp(5u)] * exp(-pi*n^2*exp(4u))

Closed form for t=0, real x (derived this tick by substituting v=pi*n^2*exp(4u)):
  H_0(x) = sum_n [ 2*pi^2*n^4 * I(9,x) - 3*pi*n^2 * I(5,x) ]
  I(a,x) = (1/4)*(pi*n^2)^(-a/4) * Re[ (pi*n^2)^(-i*x/4) * Gamma((a+i*x)/4, pi*n^2) ]
  where Gamma(s, X) is the upper incomplete gamma.

Reference: output/numbers/sample_output_Ht_real.txt (H_0(x), ~8 digits).
x values are k/10 for k=0..13.
"""
import flint
flint.ctx.prec = 120
acb = flint.acb
fmpq = flint.fmpq
PI = acb(3.14159265358979323846264338327950288419716939937510)

def H0_closed(k, n_max=4):
    """H_0(x) with x = k/10 (exact)."""
    x = fmpq(k, 10)
    total = acb(0)
    for n in range(1, n_max+1):
        P = PI * acb(n)**2          # pi*n^2  (real acb)
        logP = P.log()
        for a, coef in [(9, 2*PI**2*acb(n)**4), (5, -3*PI*acb(n)**2)]:
            pref = acb.exp(-fmpq(a,4) * logP)                 # (pi n^2)^(-a/4)
            phase = acb.exp(acb(0, -x*fmpq(1,4)) * logP)      # (pi n^2)^(-i x/4)
            s = acb(fmpq(a,4), x*fmpq(1,4))                   # (a + i x)/4
            G = acb.gamma_upper(P, s)  # python-flint: gamma_upper(x, s) = Gamma(s, x)
            total += coef * fmpq(1,4) * pref * (phase*G).real
    return total

# reference values from sample_output_Ht_real.txt (t=0 rows), keyed by k (x=k/10)
ref = {
 0: 0.06214009727353969,
 1: 0.0621365080036857,
 2: 0.06212574135138891,
 3: 0.062107800787859525,
 4: 0.06208269209649786,
 5: 0.06205042336997048,
 6: 0.06201100500611961,
 7: 0.061964449702708625,
 8: 0.06191077245100688,
 9: 0.06184999052821848,
 10: 0.061782123488759916,
 11: 0.0617071931543923,
 12: 0.06162522360321513,
 13: 0.06153624115752871,
}
print("k   x     H0_closed(Arb)        ref(sample)         diff        agree(8d)?")
ok = True
for k in sorted(ref):
    val = H0_closed(k)
    r = ref[k]
    d = abs(float(val.real) - r)
    match = d < 5e-8
    ok = ok and match
    print(f"{k:<3} {k/10:<5.1f} {float(val.real):.11f}  {r:.11f}  {d:.2e}  {match}  rad={float(val.rad()):.1e}")
print()
print("ALL MATCH to 8 digits:", ok)
