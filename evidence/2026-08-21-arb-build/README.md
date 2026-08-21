# Arb 2.23.0 + ACb 1.4 (bundled) build for the Polymath15 C code — tick 50

## Why
dbn C code (tracks/b-dbn/dbn/dbn_upper_bound/arb/) needs FLINT+Arb+ACb dev headers.
python-flint bundles only .so (0 exported C symbols, no headers) — verified tick 45.
Local model built GMP 6.3.0 / MPFR 4.2.1 / FLINT 3.2.0 into tracks/b-dbn/flint-pfx
(tick 45); ticks 46-49 stalled on Arb/ACB download URLs (arblib.org + benloko/arb 404).

## Resolution (tick 50, interactive/frontier)
Arb/ACb moved to the flintlib GitHub org (benloko/arb is 404):
  source: https://github.com/flintlib/arb/archive/refs/tags/2.23.0.tar.gz
  (Arb 2.23.0 bundles ACb: acb/ + acb.h inside the tarball — one build covers both)
Build:
  ./configure --prefix=$PFX --with-flint=$PFX
  sed -i 's/^CFLAGS=-ansi /CFLAGS=-std=c99 -include flint2_compat.h /' Makefile
  make -j48 && make install     (PFX=$HOME/riemann/tracks/b-dbn/flint-pfx)
  machine: make exit 0, make install exit 0

## FLINT 3.2 compat patches (all in the /tmp build tree; originals + final versions below)
1. Makefile CFLAGS: -ansi -> -std=c99 (FLINT 3.2 headers need C99: _Thread_local, inline)
2. fmpz_extras.h (orig: fmpz_extras.h.orig):
   - add #include "flint/mpn_extras.h" (flint_mpn_copyi moved there)
   - rename static fmpz_set_mpn_large -> arb_fmpz_set_mpn_large
   - rename static fmpz_ui_pow_ui -> arb_fmpz_ui_pow_ui
     (FLINT 3.2 now exports both publicly in fmpz.h — static-after-public clash)
   - call sites renamed in: arb/get_mpn_fixed_mod_pi4.c, arb/get_mpn_fixed_mod_log2.c,
     arb/test/t-const_glaisher.c, arb/zeta_ui_vec_borwein.c, arb/log_reduce.c,
     arb_hypgeom/gamma_stirling_sum_improved.c, fmpr/set_round_mpn.c,
     acb_hypgeom/gamma_stirling_sum_improved.c
3. fmpzi.h (orig: fmpzi.h.arb-orig): replaced by a forwarder to FLINT's fmpzi.h
   (FLINT 3.2 ships fmpzi as a strict superset; verified by header diff + libflint
   exports 114 fmpzi symbols; arb's copy had no fmpzi.c)
   NOTE: forwarder must NOT use the FMPZI_H guard (FLINT's uses the same guard)
4. flint2_compat.h (force-included via -include): FLINT 2 pulled these into flint.h,
   FLINT 3.2 users must include them themselves:
     <gmp.h>, <mpfr.h>, flint/ulong_extras.h (n_primes/n_factor),
     flint/thread_support.h (do_func_t, FLINT_PARALLEL_*), flint/thread_pool.h
     (global_thread_pool, thread_pool_wake/wait)
5. arb/const_euler.c + arb/euler_number_ui.c: add #include "flint/thread_support.h"
   (bsplit_basecase_func_t / FLINT_PARALLEL_STRIDED moved there)

## Compiling the Polymath15 barrier program
  PFX=$HOME/riemann/tracks/b-dbn/flint-pfx
  gcc tracks/b-dbn/dbn/dbn_upper_bound/arb/BarrierLocationAssistant.c \
      -I$PFX/include -I$PFX/include/flint \
      -include stdlib.h -include flint/ulong_extras.h -include flint/mpn_extras.h \
      -L$PFX/lib -lflint -larb -lgmp -lmpfr -lm \
      -o BarrierLocationAssistant
  (2018 code: stdlib.h came transitively from FLINT 2 headers; n_nextprime from flint.h umbrella)
Run: LD_LIBRARY_PATH=$PFX/lib BarrierLocationAssistant x xnum nprimes thres y0 t0 sw
