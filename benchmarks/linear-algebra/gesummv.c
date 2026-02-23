#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 512
#endif

void init_array(int n, double *alpha, double *beta,
                double A[n][n], double B[n][n], double x[n]) {
    *alpha = 1.5;
    *beta = 1.2;
    for (int i = 0; i < n; i++) {
        x[i] = (double)(i % n) / n;
        for (int j = 0; j < n; j++) {
            A[i][j] = (double)((i * j + 1) % n) / n;
            B[i][j] = (double)((i * j + 2) % n) / n;
        }
    }
}

void gesummv(int n, double alpha, double beta,
             double A[n][n], double B[n][n],
             double tmp[n], double x[n], double y[n]) {
    for (int i = 0; i < n; i++) {
        tmp[i] = 0.0;
        y[i] = 0.0;
        for (int j = 0; j < n; j++) {
            tmp[i] = A[i][j] * x[j] + tmp[i];
            y[i] = B[i][j] * x[j] + y[i];
        }
        y[i] = alpha * tmp[i] + beta * y[i];
    }
}

int main() {
    int n = N;
    double alpha, beta;

    double (*A)[n] = malloc(sizeof(double[n][n]));
    double (*B)[n] = malloc(sizeof(double[n][n]));
    double *tmp = malloc(sizeof(double[n]));
    double *x = malloc(sizeof(double[n]));
    double *y = malloc(sizeof(double[n]));

    init_array(n, &alpha, &beta, A, B, x);

    clock_t start = clock();
    gesummv(n, alpha, beta, A, B, tmp, x, y);
    clock_t end = clock();

    printf("Gesummv Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", y[0]);

    free(A); free(B); free(tmp); free(x); free(y);
    return 0;
}
