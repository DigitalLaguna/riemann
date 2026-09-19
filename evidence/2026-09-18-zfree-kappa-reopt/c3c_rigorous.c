/*
 * c3c_rigorous.c
 * Rigorous Arb verification of C3c (Lemma 14) for the corrected kappa_m
 * re-optimization (bellotti-trudgian-yang-2026, arXiv:2603.21490 v1).
 *
 * Claim: the modified kappa (kappa_6 += K, K = 0.0382944246562725) satisfies
 * the Lemma-14 lower bound for all (mu,eta) in the domain
 *   mu in [mu0,1], eta in (0,eta0], mu0=(1-sigma0)/eta0-1e-10,
 *   sigma0=0.9935164, eta0=0.0071093.
 *
 * Proof (exact decimal inputs, Arb ball arithmetic, PREC bits):
 *  D_mod = D_paper + K*B6, D_paper>=0 is the paper's Lemma 14 (published),
 *  so C3c holds iff B6>0 on the domain.
 *  B6 = a1*W(x1)+a1*W(x2)-a0*W(x3), x1=x3+1, x2=x3+p-1, x3=6p-13*mu, p=1/eta.
 *  (1) |w'(u)|<=M1 on [0,u_max]  (triangle inequality, exact).
 *  (2) w(v)>=w0-M1*v on [0,u_max]  (w(0)=w0, w'>=-M1).
 *  (3) W(s)>=w0/s-M1/s^2 for s>0.
 *  (4) B6 >= w0*t1-M1*t3, t1=a1/x1+a1/x2-a0/x3, t3=a1/x1^2+a1/x2^2+a0/x3^2.
 *  (5) t3<(2a1+1)/x3^2 (x1,x2>x3)  =>  B6 > w0*t1-M1*(2a1+1)/x3^2.
 *  (6) t1>a1/(6p)+a1/(7p)-1/(6p-13) (x3+1<6p, x3+p-1<7p, x3>=6p-13)
 *      => B6 > L(p):=w0*(a1/(6p)+a1/(7p)-1/(6p-13))-M1*(2a1+1)/(6p-13)^2.
 *  (7) L(p)>0 for all p>=1/eta0  <=>  R(u)>0 for all u>=u0=6p0-13,
 *      R(u)=w0*(13a1-7)*u^2 - 7*(13w0+M1*(2a1+1))*u - 91*M1*(2a1+1).
 *      R is quadratic, R' linear with positive slope; R(u0)>0 and R'(u0)>0
 *      => R(u)>0 for all u>=u0.
 *
 * Machine checks (ALL must pass):
 *   C1: w0>0
 *   C2: M1>0
 *   C3: R(u0)>0
 *   C4: R'(u0)>0
 *   C5: mu0>1/13   (validates the x3+1<6p step)
 */
#include <stdio.h>
#include "arb.h"

#define PREC 512

static void p(const char *label, arb_t x) {
    printf("%-26s ", label);
    arb_printn(x, 40, 0);
    printf("\n");
}

int main(void) {
    arb_t th, ct, st, A, B, C, D, E, F, umax;
    arb_t w0, M1, a1, a0, eta0, p0, u0, mu0, sigma0;
    arb_t tmp, tmp2, S, c2, c1, c0, R, Rp, vertex, one, two, three, six, seven, thirteen, ninetyone, zero;
    int ok = 1;

    arb_init(th); arb_init(ct); arb_init(st); arb_init(A); arb_init(B);
    arb_init(C); arb_init(D); arb_init(E); arb_init(F); arb_init(umax);
    arb_init(w0); arb_init(M1); arb_init(a1); arb_init(a0); arb_init(eta0);
    arb_init(p0); arb_init(u0); arb_init(mu0); arb_init(sigma0);
    arb_init(tmp); arb_init(tmp2); arb_init(S); arb_init(c2); arb_init(c1);
    arb_init(c0); arb_init(R); arb_init(Rp); arb_init(vertex);
    arb_init(one); arb_init(two); arb_init(three); arb_init(six); arb_init(seven);
    arb_init(thirteen); arb_init(ninetyone); arb_init(zero);

    arb_set_si(zero, 0);
    arb_set_si(one, 1); arb_set_si(two, 2); arb_set_si(three, 3);
    arb_set_si(six, 6); arb_set_si(seven, 7); arb_set_si(thirteen, 13);
    arb_set_si(ninetyone, 91);

    /* exact decimal / rational inputs */
    arb_set_str(th, "1.1338", 0);
    arb_set_str(eta0, "0.0071093", 0);
    arb_set_str(sigma0, "0.9935164", 0);
    arb_set_str(a1, "865534/497079", 0);
    arb_set_si(a0, 1);

    /* mu0 = (1-sigma0)/eta0 - 1e-10 */
    arb_sub(tmp, one, sigma0, PREC);        /* 1-sigma0 */
    arb_div(tmp, tmp, eta0, PREC);          /* (1-sigma0)/eta0 */
    /* mu0 = (1-sigma0)/eta0 - 1e-10 */
    arb_set_str(tmp2, "1e-10", 0);
    arb_sub(mu0, tmp, tmp2, PREC);

    /* trig */
    arb_sin(st, th, PREC);
    arb_cos(ct, th, PREC);

    /* A=1/cos^2, B=theta*cos/sin, C=tan, D=2theta, E=sin(2theta), F=sin(theta) */
    arb_mul(tmp, ct, ct, PREC);
    arb_div(A, one, tmp, PREC);
    arb_mul(tmp, th, ct, PREC);
    arb_div(B, tmp, st, PREC);
    arb_div(C, st, ct, PREC);
    arb_mul(D, two, th, PREC);
    arb_mul(tmp, two, st, PREC);
    arb_mul(tmp2, tmp, ct, PREC);
    arb_set(E, tmp2);
    arb_set(F, st);
    arb_mul(umax, two, B, PREC);

    /* w0 = w(0) = A*(A*B + 2B - 3)  (Definition 1 at u=0) */
    arb_mul(tmp, A, B, PREC);
    arb_mul(tmp2, two, B, PREC);
    arb_add(tmp, tmp, tmp2, PREC);
    arb_sub(tmp, tmp, three, PREC);
    arb_mul(w0, A, tmp, PREC);

    /* M1 = A*(A/2 + A*C*B + 1 + C/E + 2C/F)  (|w'| bound) */
    arb_div(tmp, A, two, PREC);
    arb_mul(tmp2, A, C, PREC);
    arb_mul(tmp2, tmp2, B, PREC);
    arb_add(tmp, tmp, tmp2, PREC);
    arb_add(tmp, tmp, one, PREC);
    arb_div(tmp2, C, E, PREC);
    arb_add(tmp, tmp, tmp2, PREC);
    arb_mul(tmp2, two, C, PREC);
    arb_div(tmp2, tmp2, F, PREC);
    arb_add(tmp, tmp, tmp2, PREC);
    arb_mul(M1, A, tmp, PREC);

    /* p0 = 1/eta0, u0 = 6*p0 - 13 */
    arb_div(p0, one, eta0, PREC);
    arb_mul(tmp, six, p0, PREC);
    arb_sub(u0, tmp, thirteen, PREC);

    /* R(u) = w0*(13a1-7)*u^2 - 7*(13w0+M1*(2a1+1))*u - 91*M1*(2a1+1) */
    arb_mul(tmp, thirteen, a1, PREC);       /* 13a1 */
    arb_sub(tmp, tmp, seven, PREC);         /* 13a1-7 */
    arb_mul(c2, w0, tmp, PREC);             /* c2 = w0*(13a1-7) */
    arb_mul(tmp, two, a1, PREC);            /* 2a1 */
    arb_add(tmp, tmp, one, PREC);           /* 2a1+1 */
    arb_mul(tmp2, M1, tmp, PREC);           /* M1*(2a1+1) */
    arb_mul(tmp, thirteen, w0, PREC);       /* 13w0 */
    arb_add(tmp, tmp, tmp2, PREC);          /* 13w0+M1*(2a1+1) */
    arb_mul(c1, seven, tmp, PREC);          /* c1 = 7*(13w0+M1*(2a1+1)) */
    arb_mul(c0, ninetyone, tmp2, PREC);     /* c0 = 91*M1*(2a1+1) */

    arb_mul(tmp, u0, u0, PREC);             /* u0^2 */
    arb_mul(R, c2, tmp, PREC);              /* c2*u0^2 */
    arb_sub(tmp, c1, u0, PREC);             /* c1*u0 */
    arb_sub(R, R, tmp, PREC);               /* c2*u0^2 - c1*u0 */
    arb_sub(R, R, c0, PREC);                /* R(u0) */

    arb_mul(tmp, two, c2, PREC);            /* 2*c2 */
    arb_mul(Rp, tmp, u0, PREC);             /* 2*c2*u0 */
    arb_sub(Rp, Rp, c1, PREC);              /* R'(u0) */

    /* vertex of R (for reporting) */
    arb_mul(tmp, two, c2, PREC);
    arb_div(vertex, c1, tmp, PREC);

    p("theta", th);
    p("w0", w0);
    p("M1", M1);
    p("u_max", umax);
    p("p0=1/eta0", p0);
    p("u0=6p0-13", u0);
    p("mu0", mu0);
    p("R(u0)", R);
    p("R'(u0)", Rp);
    p("vertex", vertex);

    printf("\nCHECKS:\n");
    int c1ok = arb_gt(w0, zero);
    printf("C1 w0>0            : %s\n", c1ok ? "PASS" : "FAIL");
    int c2ok = arb_gt(M1, zero);
    printf("C2 M1>0            : %s\n", c2ok ? "PASS" : "FAIL");
    int c3ok = arb_gt(R, zero);
    printf("C3 R(u0)>0         : %s\n", c3ok ? "PASS" : "FAIL");
    int c4ok = arb_gt(Rp, zero);
    printf("C4 R'(u0)>0        : %s\n", c4ok ? "PASS" : "FAIL");
    /* C5: mu0 > 1/13 */
    arb_div(tmp, one, thirteen, PREC);      /* 1/13 */
    int c5ok = arb_gt(mu0, tmp);
    printf("C5 mu0>1/13        : %s\n", c5ok ? "PASS" : "FAIL");
    /* C6: M1*u_max > w0  (validates step (3) W(s)>=w0/s-M1/s^2 for all s>0) */
    arb_mul(tmp, M1, umax, PREC);
    int c6ok = arb_gt(tmp, w0);
    printf("C6 M1*u_max>w0     : %s\n", c6ok ? "PASS" : "FAIL");

    ok = c1ok && c2ok && c3ok && c4ok && c5ok && c6ok;
    printf("\nVERDICT: C3c (Lemma 14) holds rigorously for corrected kappa ? %s\n",
           ok ? "YES" : "NO");

    arb_clear(th); arb_clear(ct); arb_clear(st); arb_clear(A); arb_clear(B);
    arb_clear(C); arb_clear(D); arb_clear(E); arb_clear(F); arb_clear(umax);
    arb_clear(w0); arb_clear(M1); arb_clear(a1); arb_clear(a0); arb_clear(eta0);
    arb_clear(p0); arb_clear(u0); arb_clear(mu0); arb_clear(sigma0);
    arb_clear(tmp); arb_clear(tmp2); arb_clear(S); arb_clear(c2); arb_clear(c1);
    arb_clear(c0); arb_clear(R); arb_clear(Rp); arb_clear(vertex);
    arb_clear(one); arb_clear(two); arb_clear(three); arb_clear(six); arb_clear(seven);
    arb_clear(thirteen); arb_clear(ninetyone); arb_clear(zero);
    return ok ? 0 : 1;
}
