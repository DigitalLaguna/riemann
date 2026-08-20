"""
Track B: rigorous (Arb) closed-form H_0(z) for COMPLEX z.

Definition (dbn_upper_bound/python/mputility.py, Ht_complex + phi_decay):
  H_0(z) = int_0^inf phi(u) cos(z u) du
  phi(u) = sum_{n>=1} [2*pi^2*n^4*exp(9u) - 3*pi*n^2*exp(5u)]*exp(-pi*n^2*exp(4u))

Closed form (derived + verified this tick, substitution v = pi*n^2*exp(4u)):
  H_0(z) = sum_n [ 2*pi^2*n^4 * J(9, z, n) - 3*pi*n^2 * J(5, z, n) ]
  J(a, z, n) = (1/8) * [ P^{-sp} * Gamma(sp, P) + P^{-sm} * Gamma(sm, P) ]
  P = pi*n^2,  sp = (a + i*z)/4,  sm = (a - i*z)/4   (upper incomplete gamma)

  NOTE: the one-term Re[...] form is only valid for REAL z (Re[w^{ic}] = cos(c ln w)
  needs c real). A first attempt (ht_closed_form_complex.py) wrongly reused it for
  complex z and also double-counted the P^{-a/4} factor -> machine said NO.

Oracle: mpmath term-by-term direct u-quadrature, 70 digits, [0,1.5], n=1..5
  H_0(35+10j) = 0.00032163883436158191156597555258989525738957951903864280036118553936386
              + 0.00007319227113411741599835095251496972054311906234081401086774973830934 i
  (the 64-digit value hardcoded in dbn_upper_bound/tests/python/test_ht.py is the
   N=1-term AFE output at s=(1+iz)/2, NOT the exact H_0; it differs by ~2.5%)
"""
import flint
flint.ctx.prec = 110
acb = flint.acb
fmpq = flint.fmpq
PI = acb('3.14159265358979323846264338327950288419716939937510')

def H0_closed(z_re, z_im, n_max=4):
    z = acb(fmpq(z_re), fmpq(z_im))
    total = acb(0)
    for n in range(1, n_max + 1):
        P = PI * acb(n)**2
        for a, coef in [(9, 2*PI**2*acb(n)**4), (5, -3*PI*acb(n)**2)]:
            sp = acb(fmpq(a, 4), 0) + acb(0, 1)*z*fmpq(1, 4)
            sm = acb(fmpq(a, 4), 0) - acb(0, 1)*z*fmpq(1, 4)
            total += coef*fmpq(1, 8)*(acb.exp(-sp*P.log())*acb.gamma_upper(P, sp)
                                     + acb.exp(-sm*P.log())*acb.gamma_upper(P, sm))
    return total

oracle_re = '0.00032163883436158191156597555258989525738957951903864'
oracle_im = '0.00007319227113411741599835095251496972054311906234081'
v = H0_closed(35, 10)
print("H_0(35+10j) Arb =", v)
print("  rad =", float(v.rad()))
print("oracle (mpmath quad 70d):", oracle_re, "+", oracle_im, "i")

# digit agreement (plain string prefix on the decimal strings)
vr = str(v.real).split(' +/-')[0].strip('[]')
vi = str(v.imag).split(' +/-')[0].strip('[]')
import re, decimal
def digits(s):
    # decimal digit string with the leading '0.' of a value in (0,1) removed
    d = format(decimal.Decimal(s), 'f')
    d = re.sub(r'[^0-9]', '', d)
    return d[2:] if len(d) > 2 and d.startswith('00') else d
print("real digits match:", digits(vr)[:30] == digits(oracle_re)[:30])
print("imag digits match:", digits(vi)[:30] == digits(oracle_im)[:30])
print("  arb real:", vr[:60])
print("  arb imag:", vi[:60])
