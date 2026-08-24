# mpmath zeta(0.5+it) cost profile at 30 dps (tick 156, 2026-08-23 ~20:05 UTC)

Measured by direct timing (8-10 reps per t, warm), machine = this workstation
(48 cores, both scans single-core 99.9% CPU, load ~3 -> no contention).

## Measured cost (s/call) vs t
t=100:0.00081  t=500:0.00856  t=1000:0.01149  t=5000:0.02136  t=10000:0.03151
t=20000:0.05047  t=30000:0.08613  t=40000:0.08646  t=42000:0.08687
t=44000:0.15541  t=45000:0.15599  t=46000:0.15614  t=48000:0.15544
t=49000:0.15596  t=50000:0.15503  t=51000:0.15581
t=52000:0.04489  t=60000:0.04245  t=80000:0.04243  t=100000:0.04253

## Structure (three regimes)
1. generic path, cost grows 0.8ms(t=100) -> 86ms(t=30k-42k)
2. PLATEAU 155ms for t in [~44000, ~51000]  (localized, mechanism = generic-path
   cancellation/term growth; not fully derived, but MEASURED and integrated)
3. RS regime 42ms for t > ~52000 (flat to 1e5)

## Mechanism (mpmath source, verbatim)
file: /home/niklas/.local/lib/python3.12/site-packages/mpmath/functions/zeta.py
line 558-560 (inside `def zeta`):
    if abs(im) > 500*prec and 10*re < prec and derivative <= 4 or \
        method == 'riemann-siegel':
        ...
        return ctx.rs_zeta(s, derivative, **kwargs)
At 30 dps, prec = 100 bits -> RS dispatch when t > 50000. (Default context is
prec=53 -> threshold 26500; a probe that forgot dps=30 measured 18ms at t=50500/51500,
NOT comparable to the 30-dps profile above.)

## Consequence for the two in-flight scans
- S(t) scan (st_run.py, step 0.3, 333331 pts): at tick 156 point 220000 (t=66001),
  66%. Remaining 113331 pts ALL in the 42ms RS regime -> 113331*0.0425 = 4817s
  = 1.34h -> completion ~21:25 UTC 08-23. (Tick-155 ETA 00:00-00:30Z was based on
  the 0.1094 s/pt plateau rate; the scan has since entered the fast regime.)
  The tick-155 "rate SLOWING 0.0849/0.1368/0.1094" was the generic path + plateau,
  now passed. Observed scan rate in RS regime = 42.3ms/pt (200000->220000 = 846s),
  matching pure-zeta 42.5ms (overhead of arg/exp/re negligible).
- Zero scan (zero_scan.py, step 0.1, 999990 grid pts + ~30 bisection Z-evals per
  zero, ~138067 zeros -> ~5.14e6 zeta calls total): at tick 156 point 55000
  (t=5501), 5.5% of points = 1.7% of total WORK (early pts cheap).
  Work density w(t) = cost(t)*[10 + 30*(1/2pi)*ln(t/2pi)]  (10 grid evals/unit t
  + 30 bisection evals/zero * zero-density). Numerically integrated (200k steps):
    REMAINING work (t=5501..1e5) = 299262 s = 83.1 h = 3.46 d
    TOTAL work (t=1..1e5)        = 302532 s = 3.50 d
  -> completion ~08-27 ~09:00 UTC. The tick-155 power-law fit (E=a*N^b, b=1.535,
  5.13 d remaining) OVER-estimated because it assumed monotonically increasing
  cost; the measured cost DROPS 2x at t>52k (RS regime). Plateau [44k,51k]
  contributes ~11h of the 83h remainder.

## Falsification / status
This is a NOTE-grade tooling measurement (mpmath = development tool, not rigorous).
It refines ETAs only; it makes no claim about RH. If either scan's actual
completion deviates from these ETAs by >20%, re-measure the profile.

## Tick 165 refinement (2026-08-24 ~00:45 UTC): cost profile has DISCRETE STEPS
Dense re-measurement of Z(t)=re(e^{i theta_asym(t)} zeta(1/2+it)) at 30 dps,
10 reps warm, t in [10000,30000] (raw: cost-profile-10k-30k.json):
  t=10000:31.3ms t=10500:31.5ms t=11000:49.4ms t=12500:49.4ms t=15000:49.3ms
  t=20000:49.6ms t=25000:85.0ms t=30000:84.9ms
The generic-regime cost is NOT smooth: it steps 31.4ms (t<=~10750) -> 49.5ms
(t~10750..~22500) -> 85ms (t~22500..~42000), then the known 155ms plateau
[44k,51k] and 42ms RS regime (>52k). The tick-156 profile linearly interpolated
across these steps (only t=10000 and t=20000 were measured in 10k-30k),
under-estimating cost in (10750,20000). This explains the abrupt observed rate
drop 4.98->3.86->3.07 pts/s between t=10501 and t=11501 (the 11001 window
straddles the 31->49ms step; the 11501 window is fully in the 49.5ms regime).

## Tick 165 ETA re-estimate (zero scan, at point 125000 = t=12501, 12.5%)
Work density w(t)=cost(t)*[10 + 30*(1/2pi)*ln(t/2pi)] integrated with the
REFINED (stepped) profile:
  model work t=1..12501   = 13647 s ; observed elapsed = 21185 s ; ratio 0.644
  model work t=1..5501    = 3270  s ; observed          = 5210  s ; ratio 0.628
  -> stable systematic bias: actual scan runs ~1.55x SLOWER than the model
     (bisection=40 instead of 30 explains part: ratio->0.809; residual ~1.24x
     unexplained, likely cost-profile under-estimate + bisection tail).
  model remaining t=12501..1e5 = 295770 s = 82.2 h = 3.42 d
  bias-corrected remaining     = 459149 s = 127.5 h = 5.31 d
  -> completion ~2026-08-29 08:00Z (range 08-28..08-29).
SUPERSEDES the tick-163 handoff ETA "~08-25 14:00Z (<=1.6d)", which linearly
extrapolated the OVERALL average rate (6.418 pts/s = 115000/17918). That is
wrong because (a) the marginal rate is 3.07 pts/s and still falling (cost steps
up at t~22500 and t~44000), and (b) the average rate is inflated by the cheap
early points. The tick-156 "3.50d total" was closer; the true completion is
~08-29, not ~08-25.
Status: NOTE-grade tooling measurement (mpmath = development tool); refines ETA
only, no RH claim. Falsification: if the scan completes outside [08-27,08-30],
re-measure the profile (a step was missed or the bias is not constant).
