import mpmath as mp
mp.mp.dps = 50
A_HB = mp.mpf('0.392113247395366294')   # reopt A0_max (#54)
T_LB = mp.mpf('76.47')                   # HB range upper bound (log t)
K    = mp.mpf('21.233')                  # published Littlewood
# A(t): u=log t. A = A_HB for u<=T_LB; A = log(u)/K for u>T_LB.
# Scan u over [log 3, 20000] (t up to exp(20000)) on a fine grid.
mn = mp.inf; arg = None
N = 400000
u0 = mp.log(mp.mpf(3)); u1 = mp.mpf(20000)
for i in range(N+1):
    u = u0 + (u1-u0)*mp.mpf(i)/N
    A = A_HB if u <= T_LB else mp.log(u)/K
    if A < mn: mn, arg = A, u
print("numerical min A (u in [log3,20000]):", mp.nstr(mn,15), "at log t =", mp.nstr(arg,12))
print("-> global C =", mp.nstr(1/mn,15))
print("A_HB =", mp.nstr(A_HB,15), " A_LW(T_LB)=log(76.47)/21.233 =", mp.nstr(mp.log(T_LB)/K,15))
print("min(A_HB, A_LW(T_LB)) =", mp.nstr(min(A_HB, mp.log(T_LB)/K),15))
