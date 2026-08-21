#!/usr/bin/env python3
"""Tick 70 (2026-08-21) — machine check of the Polymath15 Table 1 (Section 10, p. 64)
and the 0.20-path feasibility.

Oracle: lit/text/polymath15-2019.txt (fetched copy of arXiv:1904.12438).
  - Table 1 "Conditional Lambda Results" (text lines ~7229-7305)
  - Theorem 1.2 hypothesis (i) (p. 2): no zeroes zeta(sigma+iT) with
    (1+y0)/2 <= sigma <= 1 and 0 <= T <= X/2
    (verified against the PDF via pdftohtml -xml coordinates, tick 70:
     the fraction at left~339 has X (top 750) over 2 (top 762) = X/2;
     the fraction at left~160-180 has 1+y0 over 2 = (1+y0)/2.)
  - Section 8 run parameters (line ~149): t0=0.2, X = 6e10+83952-0.5, y0=0.2
  - Section 8 RH height (line 4286): Platt [18] = "3.06 × 10^10"
RH heights available:
  - Platt 2017 (paper ref [18]): T = 3.06e10
  - Platt-Trudgian 2020 (lit/text/platt-trudgian-2020.txt, abstract):
    "We verify numerically, in a rigorous way using interval arithmetic, that the
    Riemann hypothesis is true up to height 3 · 10^12."
Checks (each YES/NO, all must be YES for PASS):
  C1  table parsed: 12 rows in every column
  C2  internal consistency: |t0 + y0^2/2 - Lambda_col| <= 0.005 for all 12 rows
  C3  winding number 0 in all 12 rows
  C4  |f| lower bound >= 0.03 in all 12 rows (paper's stated safety margin)
  C5  self-consistency of the X/2 formula: Section 8 run requires
      X/2 = (6e10+83951.5)/2 = 3.0000041976e10 <= 3.06e10 (Platt 2017 height used)
  C6  0.20 row (Lambda=0.20): T_req = X/2 = (5e12+194858)/2 = 2.5000097429e12
      satisfies  T_req <= 3e12 (Platt-Trudgian)  AND  T_req > 3.06e10 (not
      available at the paper's own height) -> row is UNLOCKED by existing data
  C7  monotone: t0 and Lambda strictly decrease as X increases (sanity)
"""
import re, sys, math

TXT = "lit/text/polymath15-2019.txt"
lines = open(TXT, encoding="utf-8").read().splitlines()

TABLE_TITLE = "Table 1. Conditional Λ Results"
table_start = lines.index(TABLE_TITLE)

def col_between(start_marker, end_marker):
    out, on = [], False
    for ln in lines[table_start:]:
        s = ln.strip()
        if not on and s == start_marker:
            on = True
            continue
        if on:
            if s == end_marker:
                break
            if s:
                out.append(s)
    return out

# --- X column: lines matching 'd × 10^k + m' in the table region ---
xcol_raw = []
in_table = False
for ln in lines:
    s = ln.strip()
    if s == "Table 1. Conditional Λ Results":
        in_table = True
        continue
    if in_table and re.fullmatch(r"\d × 10\d+ \+ \d+", s):
        xcol_raw.append(s)
    elif in_table and s.startswith("t0"):
        break
X = []
for s in xcol_raw:
    m = re.fullmatch(r"(\d) × 10(\d+) \+ (\d+)", s)
    X.append(int(m.group(1)) * 10 ** int(m.group(2)) + int(m.group(3)))

t0s = [float(s) for s in col_between("t0", "y0") if re.fullmatch(r"\d\.\d+", s)]
y0s = [float(s) for s in col_between("y0", "Λ Winding Number") if re.fullmatch(r"\d\.\d+", s)]

# row block: quadruples (Lambda, winding, N0, lower bound) after the header
i = lines.index("Λ Winding Number")
lam, wind, n0, lb = [], [], [], []
j = i + 2
while len(lam) < 12:
    lam.append(float(lines[j].strip())); wind.append(int(lines[j+1].strip()))
    n0.append(int(lines[j+2].strip())); lb.append(float(lines[j+3].strip()))
    j += 4

ok = True
def check(name, cond, detail):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}: {detail}")

check("C1 table parsed", len(X) == len(t0s) == len(y0s) == len(lam) == 12,
      f"X={len(X)} t0={len(t0s)} y0={len(y0s)} rows={len(lam)}")

devs = [abs(t0 + y*y/2 - L) for t0, y, L in zip(t0s, y0s, lam)]
check("C2 Lambda = t0 + y0^2/2 (2 dp)", max(devs) <= 0.005,
      f"max |t0+y0^2/2 - Lambda_col| = {max(devs):.4f} (rows: {['%.2f' % (t0+y*y/2) for t0,y in zip(t0s,y0s)]})")

check("C3 winding 0 everywhere", all(w == 0 for w in wind), f"winding = {wind}")
check("C4 |f| lower bound >= 0.03", all(v >= 0.03 for v in lb), f"min lb = {min(lb):.4f}")

X8 = 6e10 + 83952 - 0.5
req8 = X8 / 2
check("C5 Section-8 run consistent with X/2 formula",
      req8 <= 3.06e10,
      f"X/2 = {req8:.6g} <= 3.06e10 (Platt 2017 [18], paper line 4286)")

i20 = lam.index(0.20)
req20 = X[i20] / 2
check("C6 0.20 row unlocked by Platt-Trudgian 3e12",
      3.06e10 < req20 <= 3e12,
      f"X = {X[i20]} -> T_req = X/2 = {req20:.9g}; need <= 3e12 (platt-trudgian-2020 abstract) "
      f"and > 3.06e10 (paper's own height) => UNLOCKED by existing verified RH data")

mono = all(X[k] < X[k+1] and t0s[k] > t0s[k+1] and lam[k] > lam[k+1] for k in range(11))
check("C7 monotone in X", mono, f"X grows x{X[-1]/X[0]:.0f}, t0 {t0s[0]}->{t0s[-1]}, Lambda {lam[0]}->{lam[-1]}")

print()
print("0.20-row inputs (pre-registered for the next experiment):")
print(f"  X = {X[i20]}  (barrier center; left edge X-0.5 = {X[i20]-0.5})")
print(f"  t0 = {t0s[i20]}, y0 = {y0s[i20]}, N0 = {n0[i20]}, target |f| >= 0.03 (paper achieved {lb[i20]})")
print(f"  required RH height X/2 = {req20:.9g} <= 3e12 (Platt-Trudgian 2020)")
print(f"  bound: Lambda <= t0 + y0^2/2 = {t0s[i20] + y0s[i20]**2/2:.5f} (table rounds to 0.20)")

print()
print("VERDICT:", "PASS — 0.20 path is arithmetically consistent and unlocked by existing RH data"
      if ok else "FAIL — see above")
sys.exit(0 if ok else 1)
