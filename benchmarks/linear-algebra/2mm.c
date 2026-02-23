#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef NI
#define NI 128
#endif
#ifndef NJ
#define NJ 128
#endif
#ifndef NK
#define NK 128
#endif
#ifndef NL
#define NL 128
#endif

void init_array(int ni, int nj, int nk, int nl,
                double *alpha, double *beta,
                double A[ni][nk], double B[nk][nj],
                double C[nj][nl], double D[ni][nl]) {
    *alpha = 1.5;
    *beta = 1.2;
    for (int i = 0; i < ni; i++)
        for (int j = 0; j < nk; j++)
            A[i][j] = (double)((i * j + 1) % ni) / ni;
    for (int i = 0; i < nk; i++)
        for (int j = 0; j < nj; j++)
            B[i][j] = (double)(i * (j + 1) % nj) / nj;
    for (int i = 0; i < nj; i++)
        for (int j = 0; j < nl; j++)
            C[i][j] = (double)((i * (j + 3) + 1) % nl) / nl;
    for (int i = 0; i < ni; i++)
        for (int j = 0; j < nl; j++)
            D[i][j] = (double)(i * (j + 2) % nk) / nk;
}

void mm2(int ni, int nj, int nk, int nl,
         double alpha, double beta,
         double tmp[ni][nj], double A[ni][nk], double B[nk][nj],
         double C[nj][nl], double D[ni][nl]) {
    
    for (int i = 0; i < ni; i++)
        for (int j = 0; j < nj; j++) {
            tmp[i][j] = 0.0;
            for (int k = 0; k < nk; k++)
                tmp[i][j] += alpha * A[i][k] * B[k][j];
        }
    for (int i = 0; i < ni; i++)
        for (int j = 0; j < nl; j++) {
            D[i][j] *= beta;
            for (int k = 0; k < nj; k++)
                D[i][j] += tmp[i][k] * C[k][j];
        }
}

int main() {
    int ni = NI, nj = NJ, nk = NK, nl = NL;
    double alpha, beta;

    double (*tmp)[nj] = malloc(sizeof(double[ni][nj]));
    double (*A)[nk] = malloc(sizeof(double[ni][nk]));
    double (*B)[nj] = malloc(sizeof(double[nk][nj]));
    double (*C)[nl] = malloc(sizeof(double[nj][nl]));
    double (*D)[nl] = malloc(sizeof(double[ni][nl]));

    init_array(ni, nj, nk, nl, &alpha, &beta, A, B, C, D);

    clock_t start = clock();
    mm2(ni, nj, nk, nl, alpha, beta, tmp, A, B, C, D);
    clock_t end = clock();

    printf("2MM Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", D[0][0]);

    free(tmp); free(A); free(B); free(C); free(D);
    return 0;
}
