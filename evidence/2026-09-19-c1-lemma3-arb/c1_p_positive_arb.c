/*
 * c1_p_positive_arb.c
 * Rigorous Arb verification of C1 (Lemma 3) for the corrected kappa_m
 * re-optimization (bellotti-trudgian-yang-2026, arXiv:2603.21490 v1).
 *
 * Claim: p(x) = sum_{m=0}^6 kappa_m x^m > 0 for all x in (0,1], where
 *   kappa_0 = 1, kappa_1 = -851/859, kappa_2 = 780/859, kappa_3 = -525/859,
 *   kappa_4 = 171/859, kappa_5 = 28/859,
 *   kappa_6 = -29/859 + K, K = 0.0382944246562725.
 * (kappa_m for m<6 are the paper's values, eq (18); kappa_6 corrected per
 *  the re-optimization, claims #59/#60.)
 *
 * Paper Lemma 3 states exactly this (p(x)>0 for 0<x<=1) and verifies it
 * only numerically (root isolation). This program makes it rigorous.
 *
 * Method: interval-Horner on a partition of (0,1] into N=256 subintervals
 *   [i/N, (i+1)/N]. N = 2^8, so every endpoint i/256 is an exact binary
 *   rational, set exactly via mpfr (mpfr_div_2exp) and arb_set_interval_mpfr.
 *   p is evaluated by Horner in Arb ball arithmetic (PREC bits). The claim
 *   holds iff every subinterval enclosure satisfies arb_gt(enc,0) == 1
 *   (its lower bound is > 0). We verify on [0,1] (stronger than (0,1]);
 *   p(0) = kappa_0 = 1 > 0.
 *
 * Machine checks:
 *   C1: for all i in 0..N-1, arb_gt(enc_i, zero) == 1.
 *   Reports the rigorous minimum enclosure (arb_min over all subintervals).
 */
#include <stdio.h>
#include "mpfr.h"
#include "arb.h"

#define PREC 512
#define N 256
#define LOGN 8   /* N = 2^8 */

int main(void) {
    arb_t kap[7];
    arb_t x, acc, zero, tmp, minlb;
    mpfr_t ma, mb;
    int ok = 1;
    int i, m, first = 1;

    for (m = 0; m < 7; m++) arb_init(kap[m]);
    arb_init(x); arb_init(acc); arb_init(zero); arb_init(tmp); arb_init(minlb);
    mpfr_init2(ma, PREC); mpfr_init2(mb, PREC);

    arb_set_si(zero, 0);

    /* exact rational / decimal kappa coefficients */
    arb_set_si(kap[0], 1);
    arb_set_si(tmp, -851); arb_set_si(x, 859); arb_div(kap[1], tmp, x, PREC);
    arb_set_si(tmp, 780);   arb_set_si(x, 859); arb_div(kap[2], tmp, x, PREC);
    arb_set_si(tmp, -525);  arb_set_si(x, 859); arb_div(kap[3], tmp, x, PREC);
    arb_set_si(tmp, 171);   arb_set_si(x, 859); arb_div(kap[4], tmp, x, PREC);
    arb_set_si(tmp, 28);    arb_set_si(x, 859); arb_div(kap[5], tmp, x, PREC);
    /* kappa_6 = -29/859 + K */
    arb_set_si(tmp, -29);   arb_set_si(x, 859); arb_div(kap[6], tmp, x, PREC);
    arb_set_str(tmp, "0.0382944246562725", PREC);
    arb_add(kap[6], kap[6], tmp, PREC);

    printf("N = %d subintervals, PREC = %d bits\n", N, PREC);
    printf("kappa_6 = "); arb_printn(kap[6], 30, 0); printf("\n");

    for (i = 0; i < N; i++) {
        /* exact endpoints i/256 and (i+1)/256 (binary rationals) */
        mpfr_set_ui(ma, i,     MPFR_RNDN); mpfr_div_2exp(ma, ma, LOGN, MPFR_RNDN);
        mpfr_set_ui(mb, i + 1, MPFR_RNDN); mpfr_div_2exp(mb, mb, LOGN, MPFR_RNDN);
        arb_set_interval_mpfr(x, ma, mb, PREC);

        /* interval Horner: acc = k6; acc = acc*x + k5; ...; acc = acc*x + k0 */
        arb_set(acc, kap[6]);
        for (m = 5; m >= 0; m--) {
            arb_mul(acc, acc, x, PREC);
            arb_add(acc, acc, kap[m], PREC);
        }

        int gt = arb_gt(acc, zero);
        if (gt != 1) {
            printf("subinterval [%d/%d, %d/%d]: arb_gt = %d (NOT > 0)\n",
                   i, N, i+1, N, gt);
            ok = 0;
        }
        if (first) { arb_set(minlb, acc); first = 0; }
        else arb_min(minlb, minlb, acc, PREC);
    }

    printf("rigorous min enclosure = ");
    arb_printn(minlb, 40, 0);
    printf("\n");
    printf("min enclosure > 0 ? %s\n", arb_gt(minlb, zero) == 1 ? "YES" : "NO");

    if (ok) {
        printf("VERDICT: C1 (Lemma 3) p(x)>0 on (0,1] for corrected kappa ? YES\n");
    } else {
        printf("VERDICT: C1 (Lemma 3) p(x)>0 on (0,1] for corrected kappa ? NO\n");
    }

    for (m = 0; m < 7; m++) arb_clear(kap[m]);
    arb_clear(x); arb_clear(acc); arb_clear(zero); arb_clear(tmp); arb_clear(minlb);
    mpfr_clear(ma); mpfr_clear(mb);
    return ok ? 0 : 1;
}
