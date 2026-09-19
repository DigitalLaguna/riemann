/*
 * c2_B_nonneg_arb.c
 * Rigorous Arb verification of C2 (Lemma 5 non-negativity) for the corrected
 * kappa_m re-optimization (bellotti-trudgian-yang-2026, arXiv:2603.21490 v1).
 *
 * Claim: B(y) >= 0 for all y in R, where
 *   B(y) = sum_{M=1}^{7} b_M * B_M(y),
 *   b_M = coeff of x^M in (1+x)*sum_{k=0}^{6} kappa_k x^k  (= kappa_M + kappa_{M-1}),
 *   B_M(y) = (A_M + y^2)^2 / (M + y^2),  A_M = c0^M + eps0/M (b_M<=0) or M - eps0/M (b_M>0),
 *   c0 = 151/153, eps0 = 1/2000.
 *   kappa_0=1, kappa_1=-851/859, kappa_2=780/859, kappa_3=-525/859,
 *   kappa_4=171/859, kappa_5=28/859, kappa_6=-29/859+K, K=0.0382944246562725.
 *
 * Since B depends on y only through z=y^2>=0, write B(z)=sum b_M (z+A_M)^2/(z+M).
 * Rigorous proof (Arb ball arithmetic, PREC bits):
 *   (1) On [0,10]: partition into N=1024 subintervals [5i*2^-9, 5(i+1)*2^-9]
 *       (exact binary endpoints). Evaluate B(z) by interval arithmetic.
 *       Claim holds iff every enclosure satisfies arb_gt(enc,0)==1.
 *   (2) On [10,inf): (z+A)^2/(z+M) = z+(2A-M)+(A-M)^2/(z+M), so
 *       B(z) >= S1*z + S2 + S3(10) for z>=10, where
 *       S1=sum b_M, S2=sum b_M(2A_M-M), S3(10)=sum_{b_M<0} b_M(A_M-M)^2/10.
 *       B(z)>0 for all z>=10 iff L:=S1*10+S2+S3(10) > 0.
 *
 * Machine checks (ALL must pass):
 *   C1: every subinterval enclosure on [0,10] has arb_gt(enc,0)==1.
 *   C2: L = S1*10 + S2 + S3(10) > 0.
 *   C3: B(0) > 0 (sanity: the minimum is at z=0).
 */
#include <stdio.h>
#include "mpfr.h"
#include "arb.h"

#define PREC 512
#define N 1024
#define LOGD 9   /* endpoint = 5*i*2^-9 ; N*10/1024 = 10 */

int main(void) {
    arb_t b[8], A[8];            /* index 1..7 */
    arb_t z, term, num, den, acc, zero, one, tmp, tmp2;
    arb_t Kvar, c0, c02, c04;
    arb_t S1, S2, S3, L, B0, minlb;
    mpfr_t ma, mb;
    int ok = 1, i, M, first = 1;

    for (M = 1; M <= 7; M++) { arb_init(b[M]); arb_init(A[M]); }
    arb_init(z); arb_init(term); arb_init(num); arb_init(den); arb_init(acc);
    arb_init(zero); arb_init(one); arb_init(tmp); arb_init(tmp2);
    arb_init(Kvar); arb_init(c0); arb_init(c02); arb_init(c04);
    arb_init(S1); arb_init(S2); arb_init(S3); arb_init(L); arb_init(B0); arb_init(minlb);
    mpfr_init2(ma, PREC); mpfr_init2(mb, PREC);

    arb_set_si(zero, 0); arb_set_si(one, 1);

    /* dedicated exact inputs */
    arb_set_str(Kvar, "0.0382944246562725", PREC);
    arb_set_si(tmp2, 151); arb_set_si(tmp, 153); arb_div(c0, tmp2, tmp, PREC);
    arb_mul(c02, c0, c0, PREC);
    arb_mul(c04, c02, c02, PREC);

    /* b_M = kappa_M + kappa_{M-1} (M=1..7); kappa_6 = -29/859 + K */
    arb_set_si(tmp2, 8);    arb_set_si(tmp, 859); arb_div(b[1], tmp2, tmp, PREC);
    arb_set_si(tmp2, -71);  arb_set_si(tmp, 859); arb_div(b[2], tmp2, tmp, PREC);
    arb_set_si(tmp2, 255);  arb_set_si(tmp, 859); arb_div(b[3], tmp2, tmp, PREC);
    arb_set_si(tmp2, -354); arb_set_si(tmp, 859); arb_div(b[4], tmp2, tmp, PREC);
    arb_set_si(tmp2, 199);  arb_set_si(tmp, 859); arb_div(b[5], tmp2, tmp, PREC);
    arb_set_si(tmp2, -1);   arb_set_si(tmp, 859); arb_div(b[6], tmp2, tmp, PREC);
    arb_add(b[6], b[6], Kvar, PREC);
    arb_set_si(tmp2, -29);  arb_set_si(tmp, 859); arb_div(b[7], tmp2, tmp, PREC);
    arb_add(b[7], b[7], Kvar, PREC);

    /* A_M */
    arb_set_si(tmp2, 1999);  arb_set_si(tmp, 2000);  arb_div(A[1], tmp2, tmp, PREC); /* 1-1/2000 */
    arb_set(A[2], c02);
    arb_set_si(tmp2, 1); arb_set_si(tmp, 4000); arb_div(tmp, tmp2, tmp, PREC);
    arb_add(A[2], A[2], tmp, PREC);                                                    /* c0^2+1/4000 */
    arb_set_si(tmp2, 17999); arb_set_si(tmp, 6000); arb_div(A[3], tmp2, tmp, PREC);    /* 3-1/6000 */
    arb_set(A[4], c04);
    arb_set_si(tmp2, 1); arb_set_si(tmp, 8000); arb_div(tmp, tmp2, tmp, PREC);
    arb_add(A[4], A[4], tmp, PREC);                                                    /* c0^4+1/8000 */
    arb_set_si(tmp2, 49999); arb_set_si(tmp, 10000); arb_div(A[5], tmp2, tmp, PREC);    /* 5-1/10000 */
    arb_set_si(tmp2, 71999); arb_set_si(tmp, 12000); arb_div(A[6], tmp2, tmp, PREC);    /* 6-1/12000 */
    arb_set_si(tmp2, 97999); arb_set_si(tmp, 14000); arb_div(A[7], tmp2, tmp, PREC);    /* 7-1/14000 */

    printf("N = %d subintervals on [0,10], PREC = %d bits\n", N, PREC);
    for (M = 1; M <= 7; M++) {
        printf("b_%d = ", M); arb_printn(b[M], 25, 0);
        printf("   A_%d = ", M); arb_printn(A[M], 25, 0); printf("\n");
    }

    /* ---- Part 1: B(z) > 0 on [0,10] by partition ---- */
    for (i = 0; i < N; i++) {
        mpfr_set_ui(ma, 5LL*i,     MPFR_RNDN); mpfr_mul_2exp(ma, ma, -LOGD, MPFR_RNDN);
        mpfr_set_ui(mb, 5LL*(i+1), MPFR_RNDN); mpfr_mul_2exp(mb, mb, -LOGD, MPFR_RNDN);
        arb_set_interval_mpfr(z, ma, mb, PREC);

        arb_set_si(acc, 0);
        for (M = 1; M <= 7; M++) {
            arb_add(num, z, A[M], PREC);          /* z + A_M */
            arb_mul(num, num, num, PREC);         /* (z+A_M)^2 */
            arb_mul(num, num, b[M], PREC);        /* b_M (z+A_M)^2 */
            arb_set_si(den, M);
            arb_add(den, den, z, PREC);          /* z + M */
            arb_div(term, num, den, PREC);       /* b_M (z+A_M)^2/(z+M) */
            arb_add(acc, acc, term, PREC);
        }
        int gt = arb_gt(acc, zero);
        if (gt != 1) {
            printf("subinterval [%d/%d]: arb_gt = %d (NOT > 0)\n", i, N, gt);
            ok = 0;
        }
        if (first) { arb_set(minlb, acc); first = 0; }
        else arb_min(minlb, minlb, acc, PREC);
    }
    printf("rigorous min enclosure on [0,10] = ");
    arb_printn(minlb, 40, 0); printf("\n");
    int c1ok = ok && (arb_gt(minlb, zero) == 1);
    printf("C1 B(z)>0 on [0,10] (all %d subintervals) : %s\n", N, c1ok ? "PASS" : "FAIL");

    /* ---- Part 2: tail bound L = S1*10 + S2 + S3(10) > 0 ---- */
    arb_set_si(S1, 0);
    for (M = 1; M <= 7; M++) arb_add(S1, S1, b[M], PREC);
    arb_set_si(S2, 0);
    for (M = 1; M <= 7; M++) {
        arb_add(tmp, A[M], A[M], PREC);          /* 2 A_M */
        arb_set_si(tmp2, M);
        arb_sub(tmp, tmp, tmp2, PREC);          /* 2 A_M - M */
        arb_mul(tmp, tmp, b[M], PREC);          /* b_M (2 A_M - M) */
        arb_add(S2, S2, tmp, PREC);
    }
    arb_set_si(S3, 0);
    for (M = 1; M <= 7; M++) {
        if (arb_lt(b[M], zero) != 1) continue;  /* only b_M < 0 */
        arb_set_si(tmp2, M);
        arb_sub(tmp, A[M], tmp2, PREC);        /* A_M - M */
        arb_mul(tmp, tmp, tmp, PREC);          /* (A_M - M)^2 */
        arb_mul(tmp, tmp, b[M], PREC);         /* b_M (A_M - M)^2 */
        arb_set_si(tmp2, 10);
        arb_div(tmp, tmp, tmp2, PREC);         /* /10 */
        arb_add(S3, S3, tmp, PREC);
    }
    arb_set_si(tmp, 10);
    arb_mul(L, S1, tmp, PREC);
    arb_add(L, L, S2, PREC);
    arb_add(L, L, S3, PREC);
    printf("S1 = "); arb_printn(S1, 25, 0);
    printf("  S2 = "); arb_printn(S2, 25, 0);
    printf("  S3(10) = "); arb_printn(S3, 25, 0);
    printf("  L = "); arb_printn(L, 25, 0); printf("\n");
    int c2ok = (arb_gt(L, zero) == 1);
    printf("C2 tail bound L>0 (z>=10)                : %s\n", c2ok ? "PASS" : "FAIL");

    /* ---- Part 3: sanity B(0) > 0 ---- */
    arb_set_si(acc, 0);
    for (M = 1; M <= 7; M++) {
        arb_mul(num, A[M], A[M], PREC);        /* A_M^2 */
        arb_mul(num, num, b[M], PREC);
        arb_set_si(den, M);
        arb_div(term, num, den, PREC);
        arb_add(acc, acc, term, PREC);
    }
    arb_set(B0, acc);
    printf("B(0) = "); arb_printn(B0, 25, 0); printf("\n");
    int c3ok = (arb_gt(B0, zero) == 1);
    printf("C3 B(0)>0 (sanity)                       : %s\n", c3ok ? "PASS" : "FAIL");

    ok = c1ok && c2ok && c3ok;
    printf("\nVERDICT: C2 (Lemma 5) B(y)>=0 for all y in R for corrected kappa ? %s\n",
           ok ? "YES" : "NO");

    for (M = 1; M <= 7; M++) { arb_clear(b[M]); arb_clear(A[M]); }
    arb_clear(z); arb_clear(term); arb_clear(num); arb_clear(den); arb_clear(acc);
    arb_clear(zero); arb_clear(one); arb_clear(tmp); arb_clear(tmp2);
    arb_clear(Kvar); arb_clear(c0); arb_clear(c02); arb_clear(c04);
    arb_clear(S1); arb_clear(S2); arb_clear(S3); arb_clear(L); arb_clear(B0); arb_clear(minlb);
    mpfr_clear(ma); mpfr_clear(mb);
    return ok ? 0 : 1;
}
