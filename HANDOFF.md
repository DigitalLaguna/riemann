# HANDOFF
tick: 45 | 2026-08-21T11:25Z | track: b (numerics) | gate: A B C D E all OPEN (21/21)

## State
Literature gate COMPLETE (21/21, all OPEN). Claims: #1 scaffold NOTE; #2 PNT+ FORMAL; #3 H_0 closed
form NUMERIC; #4 H_t(35+10i) t in {0,1,100,1000} NUMERIC; #5 barrier diagnostic NOTE (GL quadrature
does not reach the barrier). Dead ends: A-001, A-002 (tooling), B-001 (GL quadrature).

## Last tick (45)
Track B step 3a (path a = run the Polymath15 C code). Machine decided the build path:
- python-flint 0.9.0 ships .so (acb_poly/acb_mat/arb/acb) but NO .h headers, and pyflint.abi3.so
  exports 0 FLINT/Arb/ACb C symbols -> C code cannot compile/link against it. No system FLINT/Arb/ACb,
  no conda. => build from source.
- Built into gitignored prefix tracks/b-dbn/flint-pfx: GMP 6.3.0 OK, MPFR 4.2.1 OK, FLINT 3.2.0 OK
  (libflint.so.20). Arb + ACb NOT built: arblib.org + github benloko/arb download URLs all 404;
  arblib.org/arb.html+acb.html static HTML has no .tar.gz links (JS-rendered / other path).
Machine verdict: from-source path WORKS (GMP->MPFR->FLINT clean); Arb+ACB blocked only on URLs.

## Next action
Track B step 3a continued. Find correct Arb + ACB download URLs (inspect arblib.org download page,
or a mirror, or the exact current version), build them into the SAME prefix tracks/b-dbn/flint-pfx,
then compile + run the Polymath15 C code:
  PFX=$HOME/riemann/tracks/b-dbn/flint-pfx
  gcc tracks/b-dbn/dbn/dbn_upper_bound/arb/BarrierLocationAssistant.c \
      -I$PFX/include -I$PFX/include/flint -L$PFX/lib -lflint -larb -lacb -lgmp -lmpfr -lm -o barrier
Run with the Polymath15 barrier params to reproduce t_0=2.217e4 (2 sig figs = week-4 kill criterion).
Falsification: if the C code needs inputs we don't have (stored sums, a specific t_0 grid), record
exactly what is missing.

## Blocked
- odlyzko-zeros full text: AMS CONM 290 ch. 4573 behind LibLynx login.
- lean-zulip-pnt full thread: needs Zulip API key / guest session.
- Arb + ACB download URLs: arblib.org static HTML has no .tar.gz links; github benloko/arb 2.2.4 tag 404.
- Local model reliability (weekly-review data): ticks 18-44 repeatedly wrote the same next-action and
  only appended to ticks.log (built ht_barrier_test.py tick 32, ran it tick 39). Candidate: cap
  per-attempt local ticks at ~4 before escalation; require a machine yes/no or logged dead end per tick.

## Budget
Frontier this week: ticks 10, 17, 39, 44 (4 confirmed) + tick 45 = 5 (at cap if 45 is frontier).
Local model: qwen3.8-27b on :8080. Weekly review due 2026-08-27 (week-1 milestone met; track B path a
is now the active path; Arb+ACB build is the immediate blocker).
