#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef M
#define M 256
#endif
#ifndef N
#define N 256
#endif

void init_array(int m, int n, double *alpha, double *beta,
                double C[m][n], double A[m][m], double B[m][n]) {
    *alpha = 1.5;
    *beta = 1.2;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            C[i][j] = (double)((i + j) % 100) / m;
            B[i][j] = (double)((n + i - j) % 100) / m;
        }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j <= i; j++)
            A[i][j] = (double)((i + j) % 100) / m;
        for (int j = i + 1; j < m; j++)
            A[i][j] = -999; 
    }
}

void symm(int m, int n, double alpha, double beta,
          double C[m][n], double A[m][m], double B[m][n]) {
    double temp2;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            temp2 = 0;
            for (int k = 0; k < i; k++) {
                C[k][j] += alpha * B[i][j] * A[i][k];
                temp2 += B[k][j] * A[i][k];
            }
            C[i][j] = beta * C[i][j] + alpha * B[i][j] * A[i][i] + alpha * temp2;
        }
}

int main() {
    int m = M, n = N;
    double alpha, beta;

    double (*C)[n] = malloc(sizeof(double[m][n]));
    double (*A)[m] = malloc(sizeof(double[m][m]));
    double (*B)[n] = malloc(sizeof(double[m][n]));

    init_array(m, n, &alpha, &beta, C, A, B);

    clock_t start = clock();
    symm(m, n, alpha, beta, C, A, B);
    clock_t end = clock();

    printf("SYMM Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", C[0][0]);

    free(C); free(A); free(B);
    return 0;
}
