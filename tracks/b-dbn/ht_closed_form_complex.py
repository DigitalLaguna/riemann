"""
Track B: verify H_0(z) for COMPLEX z against the 64-digit reference in
dbn_upper_bound/tests/python/test_ht.py (Ht_AFE_ABC(35+10j, 0)).

Closed form (t=0, general complex z), same substitution v=pi*n^2*exp(4u):
  H_0(z) = sum_n [ 2*pi^2*n^4*I(9,z) - 3*pi*n^2*I(5,z) ]
  I(a,z) = (1/4)*(pi*n^2)^(-a/4) * Re[ (pi*n^2)^(-i*z/4) * Gamma((a+i*z)/4, pi*n^2) ]
Reference (test_ht.py, 64 digits):
  H_0(35+10j) = 0.000313552332336939669577229294629866377113376343853824475809041362996
              + 0.00007605623264065672294567401329292513426458248255176130198721233252061 i
"""
import flint
flint.ctx.prec = 120
acb = flint.acb
fmpq = flint.fmpq
PI = acb(3.14159265358979323846264338327950288419716939937510)

def H0_closed_complex(x, y, n_max=5):
    """H_0(z) with z = x + i*y (x,y exact rationals)."""
    z = acb(fmpq(x), fmpq(y))
    total = acb(0)
    for n in range(1, n_max+1):
        P = PI * acb(n)**2
        logP = P.log()
        for a, coef in [(9, 2*PI**2*acb(n)**4), (5, -3*PI*acb(n)**2)]:
            pref  = acb.exp(-fmpq(a,4) * logP)          # (pi n^2)^(-a/4)
            # (pi n^2)^(-i z/4) = exp(-i z/4 * logP)
            phase = acb.exp(-acb(0,1)*z*fmpq(1,4) * logP)
            s = acb(fmpq(a,4), 0) + acb(0,1)*z*fmpq(1,4)  # (a + i z)/4
            G = acb.gamma_upper(P, s)                    # Gamma(s, pi n^2)
            total += coef * fmpq(1,4) * pref * (phase*G).real
    return total

ref_re = '0.000313552332336939669577229294629866377113376343853824475809041362996'
ref_im = '0.00007605623264065672294567401329292513426458248255176130198721233252061'
val = H0_closed_complex(35, 10)
print("H_0(35+10j) Arb  =", val)
print("  real =", val.real)
print("  imag =", val.imag)
print("  rad  =", float(val.rad()))
print("ref real =", ref_re)
print("ref imag =", ref_im)
# compare digit by digit (string prefix)
vr = str(val.real); vi = str(val.imag)
print()
print("real match (first 40 chars):", vr[:40], "==", ref_re[:40], "->", vr[:40]==ref_re[:40])
print("imag match (first 40 chars):", vi[:40], "==", ref_im[:40], "->", vi[:40]==ref_im[:40])
