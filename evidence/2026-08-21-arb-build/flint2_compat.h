/*
  flint2_compat.h — compat shim: FLINT 2.x n_primes / n_factor API on top of
  FLINT >= 3.2 (types removed). Force-included via -include. Verified against
  Arb 2.23.0 call sites (n_factor always called with flags=1).
*/
#ifndef FLINT2_COMPAT_H
#define FLINT2_COMPAT_H

#include "flint/flint.h"
#include "flint/fmpz_factor.h"
#include "flint/ulong_extras.h"

/* --- n_primes: FLINT 2 iterator type (heap state, shared by value) --- */
typedef ulong * n_primes_t;

static __inline__ void
n_primes_init(n_primes_t iter)
{
    *iter = flint_malloc(sizeof(ulong));
    **iter = 2;
}

static __inline__ ulong
n_primes_next(n_primes_t iter)
{
    ulong p = *iter;
    *iter = n_nextprime(p, 1);
    return p;
}

static __inline__ void
n_primes_clear(n_primes_t iter)
{
    flint_free(*iter);
}

/* --- n_factor: FLINT 2 factorization struct --- */
typedef struct
{
    slong num;
    ulong * p;
    slong * exp;
} n_factor_struct;

typedef n_factor_struct n_factor_t;

static __inline__ void
n_factor_init(n_factor_struct * fac)
{
    fac->num = 0;
    fac->p = NULL;
    fac->exp = NULL;
}

static __inline__ void
n_factor_clear(n_factor_struct * fac)
{
    if (fac->p != NULL) flint_free(fac->p);
    if (fac->exp != NULL) flint_free(fac->exp);
    fac->p = NULL;
    fac->exp = NULL;
    fac->num = 0;
}

static __inline__ void
n_factor(n_factor_struct * fac, ulong n, slong flags)
{
    fmpz_factor_t f;
    slong i;

    (void) flags;
    n_factor_clear(fac);
    fmpz_factor_init(&f);
    fmpz_factor(f.num, n);
    fac->num = fmpz_factor_num_primes(f);
    if (fac->num > 0)
    {
        fac->p = flint_malloc(sizeof(ulong) * (size_t) fac->num);
        fac->exp = flint_malloc(sizeof(slong) * (size_t) fac->num);
        for (i = 0; i < fac->num; i++)
        {
            fac->p[i] = fmpz_factor_get_p(f, i);
            fac->exp[i] = fmpz_factor_get_exp(f, i);
        }
    }
    fmpz_factor_clear(&f);
}

#endif
