#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 512
#endif

void init_array(int n, double *alpha, double *beta,
                double A[n][n], double u1[n], double v1[n],
                double u2[n], double v2[n], double w[n],
                double x[n], double y[n], double z[n]) {
    *alpha = 1.5;
    *beta = 1.2;
    for (int i = 0; i < n; i++) {
        u1[i] = i;
        u2[i] = ((i + 1) / n) / 2.0;
        v1[i] = ((i + 1) / n) / 4.0;
        v2[i] = ((i + 1) / n) / 6.0;
        y[i] = ((i + 1) / n) / 8.0;
        z[i] = ((i + 1) / n) / 9.0;
        x[i] = 0.0;
        w[i] = 0.0;
        for (int j = 0; j < n; j++)
            A[i][j] = (double)(i * j % n) / n;
    }
}

void gemver(int n, double alpha, double beta,
            double A[n][n], double u1[n], double v1[n],
            double u2[n], double v2[n], double w[n],
            double x[n], double y[n], double z[n]) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            A[i][j] = A[i][j] + u1[i] * v1[j] + u2[i] * v2[j];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            x[i] = x[i] + beta * A[j][i] * y[j];

    for (int i = 0; i < n; i++)
        x[i] = x[i] + z[i];

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            w[i] = w[i] + alpha * A[i][j] * x[j];
}

int main() {
    int n = N;
    double alpha, beta;

    double (*A)[n] = malloc(sizeof(double[n][n]));
    double *u1 = malloc(sizeof(double[n]));
    double *v1 = malloc(sizeof(double[n]));
    double *u2 = malloc(sizeof(double[n]));
    double *v2 = malloc(sizeof(double[n]));
    double *w = malloc(sizeof(double[n]));
    double *x = malloc(sizeof(double[n]));
    double *y = malloc(sizeof(double[n]));
    double *z = malloc(sizeof(double[n]));

    init_array(n, &alpha, &beta, A, u1, v1, u2, v2, w, x, y, z);

    clock_t start = clock();
    gemver(n, alpha, beta, A, u1, v1, u2, v2, w, x, y, z);
    clock_t end = clock();

    printf("Gemver Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", w[0]);

    free(A); free(u1); free(v1); free(u2); free(v2);
    free(w); free(x); free(y); free(z);
    return 0;
}
