#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 512
#endif

void init_array(int n, double A[n][n], double B[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            A[i][j] = ((double) i * j) / n;
            B[i][j] = ((double) i * j) / n;
        }
    }
}

void gemm(int n, double alpha, double beta,
          double C[n][n], double A[n][n], double B[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            C[i][j] *= beta;
            for (int k = 0; k < n; k++) {
                C[i][j] += alpha * A[i][k] * B[k][j];
            }
        }
    }
}

int main(int argc, char** argv) {
    int n = N;
    double alpha = 1.5;
    double beta = 1.2;

    double (*A)[n][n] = malloc(sizeof(double[n][n]));
    double (*B)[n][n] = malloc(sizeof(double[n][n]));
    double (*C)[n][n] = malloc(sizeof(double[n][n]));

    init_array(n, *A, *B);

    clock_t start = clock();
    gemm(n, alpha, beta, *C, *A, *B);
    clock_t end = clock();

    printf("GEMM Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", (*C)[0][0]);

    free(A);
    free(B);
    free(C);
    return 0;
}
