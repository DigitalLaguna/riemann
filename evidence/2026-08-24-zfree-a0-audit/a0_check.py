import mpmath
mpmath.mp.dps = 50
H  = mpmath.mpf('3e12')          # eq (5), line 163
K  = 16                          # line 534
T0 = mpmath.mpf('1e10')          # line 532
logH    = mpmath.log(H)
logKHT0 = mpmath.log(K*H + T0)
n = mpmath.nstr

cands = {
  'printed L1 (4.8596)^-1': 1/mpmath.mpf('4.8596'),
  'L1 headline  (4.896)^-1' : 1/mpmath.mpf('4.896'),
  'L2          (4.8594)^-1' : 1/mpmath.mpf('4.8594'),
}
print("== eta0 = A0/logH, sigma0 = 1 - A0/log(KH+T0) for candidate A0 ==")
for name,A0 in cands.items():
    print(f"{name:26s} A0={n(A0,10)}  eta0={n(A0/logH,8)}  sigma0={n(1-A0/logKHT0,8)}")

print("\n== table values (verbatim, lines 543-552) ==")
print("Lemma 1 row: eta0=0.0071093  sigma0=0.9935164")
print("Lemma 2 row: eta0=0.0071628  sigma0=0.9934675")

print("\n== final-line requirement: A0 < A_final (paper formula, exact min) ==")
den_paper = mpmath.mpf('5.03905010328')   # (a*kappa*w(0)/2) as printed
min_exact = mpmath.mpf('1.029287401')     # exact min of RHS on [logH,76.47] (reopt CASE 1)
Afin = min_exact/den_paper
print(f"A_final(paper formula, exact min) = {n(Afin,10)}")
for name,A0 in cands.items():
    ok = A0 < Afin
    print(f"  {name:26s} A0<A_final? {ok}   margin={n(Afin-A0,4)}")
