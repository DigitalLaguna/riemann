#!/bin/bash
# Track B X=6e12 row — machine checks (tick 95; leg iii extended tick 107). Re-runnable.
# Pre-registered falsification test: logs/2026-08-22.tick.log tick-91 section.
# Row: X=6e12 (left edge 5999999999999.5), t0=0.185, y0=0.16733, N0=690988.
# Target: Lambda = t0 + y0^2/2 < 0.19999966445 (claim #9's row-2 bound).
EV=evidence/2026-08-22-x6e12
ARB=tracks/b-dbn/dbn/dbn_upper_bound/arb
pass=0; fail=0
chk(){ if [ "$1" = 0 ]; then echo "PASS  ($2)"; pass=$((pass+1)); else echo "FAIL  ($2)"; fail=$((fail+1)); fi; }

# (ii) |f| Lemma-10.1 lower bound at (t0=0.185, y0=0.16733, N0=690988) >= 0.03
val=$(grep -Eo '^[0-9]+\.[0-9]+' $EV/abeff_x6e12.txt | head -1)
echo "abeff value = $val"
awk -v v="$val" 'BEGIN{exit !(v>=0.03)}'; chk $? "(ii) |f| bound $val >= 0.03"

# Exact bound arithmetic (rational): Lambda = t0 + y0^2/2, and < 0.19999966445
python3 - <<'PY'
from fractions import Fraction as F
t0 = F(185,1000); y0 = F(16733,100000)
lam = t0 + y0*y0/2
target = F(19999966445,10**11)
print("Lambda = t0 + y0^2/2 =", float(lam), "exact", lam)
print("target 0.19999966445 =", float(target))
print("Lambda < target:", lam < target)
exit(0 if lam < target else 1)
PY
chk $? "Lambda = t0+y0^2/2 = 0.19899966445 < 0.19999966445 (exact rational)"

# (i) RH height: X/2 <= 3e12 (Platt-Trudgian, claim #8)
awk 'BEGIN{exit !((5999999999999.5+0.5)/2 <= 3e12)}'; chk $? "(i) RH height barrier-center X/2 = 3e12 <= 3e12 (Platt-Trudgian)"

# (iii) T-loop winding number for X=6e12 barrier (run4): exit=0, winding 0, no Abort
RUN4=$EV/tloop_x6e12_run4.txt
STAT4=$EV/tloop_x6e12_run4.status
if [ -s "$RUN4" ] && grep -q 'Overall winding number: 0.000000' "$RUN4" \
   && ! grep -q 'Abort' "$RUN4" && grep -q 'exit=0' "$STAT4"; then
  chk 0 "(iii) T-loop X=6e12 run4: exit=0, 'Overall winding number: 0.000000', no Abort ($(grep -c '^Rectangle' $RUN4) rects, final t=$(grep '^Rectangle' $RUN4 | tail -1 | awk -F': ' '{print $2}' | awk -F, '{print $1}'))"
else
  chk 1 "(iii) T-loop X=6e12 run4: not complete (exit/winding/Abort check failed)"
fi

echo "----"
echo "pass=$pass fail=$fail"
[ $fail -eq 0 ] && echo "CHECK PASS (all legs i,ii,iii verified)" || echo "CHECK FAIL"
