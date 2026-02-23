#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef M
#define M 256
#endif
#ifndef N
#define N 256
#endif

void init_array(int n, int m, double *alpha, double *beta,
                double C[n][n], double A[n][m]) {
    *alpha = 1.5;
    *beta = 1.2;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            A[i][j] = (double)((i * j + 1) % n) / n;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            C[i][j] = (double)((i * j + 2) % m) / m;
}

void syrk(int n, int m, double alpha, double beta,
          double C[n][n], double A[n][m]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= i; j++)
            C[i][j] *= beta;
        for (int k = 0; k < m; k++)
            for (int j = 0; j <= i; j++)
                C[i][j] += alpha * A[i][k] * A[j][k];
    }
}

int main() {
    int n = N, m = M;
    double alpha, beta;

    double (*C)[n] = malloc(sizeof(double[n][n]));
    double (*A)[m] = malloc(sizeof(double[n][m]));

    init_array(n, m, &alpha, &beta, C, A);

    clock_t start = clock();
    syrk(n, m, alpha, beta, C, A);
    clock_t end = clock();

    printf("SYRK Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", C[0][0]);

    free(C); free(A);
    return 0;
}
