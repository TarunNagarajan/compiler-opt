#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef NQ
#define NQ 64
#endif
#ifndef NR
#define NR 64
#endif
#ifndef NP
#define NP 64
#endif

void init_array(int nr, int nq, int np,
                double A[nr][nq][np], double C4[np][np]) {
    for (int i = 0; i < nr; i++)
        for (int j = 0; j < nq; j++)
            for (int k = 0; k < np; k++)
                A[i][j][k] = (double)((i * j + k) % np) / np;
    for (int i = 0; i < np; i++)
        for (int j = 0; j < np; j++)
            C4[i][j] = (double)(i * j % np) / np;
}

void doitgen(int nr, int nq, int np,
             double A[nr][nq][np], double C4[np][np], double sum[np]) {
    for (int r = 0; r < nr; r++)
        for (int q = 0; q < nq; q++) {
            for (int p = 0; p < np; p++) {
                sum[p] = 0.0;
                for (int s = 0; s < np; s++)
                    sum[p] += A[r][q][s] * C4[s][p];
            }
            for (int p = 0; p < np; p++)
                A[r][q][p] = sum[p];
        }
}

int main() {
    int nr = NR, nq = NQ, np = NP;

    double (*A)[nq][np] = malloc(sizeof(double[nr][nq][np]));
    double (*C4)[np] = malloc(sizeof(double[np][np]));
    double *sum = malloc(sizeof(double[np]));

    init_array(nr, nq, np, A, C4);

    clock_t start = clock();
    doitgen(nr, nq, np, A, C4, sum);
    clock_t end = clock();

    printf("Doitgen Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", A[0][0][0]);

    free(A); free(C4); free(sum);
    return 0;
}
