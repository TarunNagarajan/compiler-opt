#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 256
#endif

void init_array(int n, double A[n][n], double b[n], double x[n], double y[n]) {
    double fn = (double)n;
    for (int i = 0; i < n; i++) {
        x[i] = 0;
        y[i] = 0;
        b[i] = (i + 1) / fn / 2.0 + 4;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= i; j++)
            A[i][j] = (double)(-j % n) / n + 1;
        for (int j = i + 1; j < n; j++)
            A[i][j] = 0;
        A[i][i] = 1;
    }
    
    double (*B)[n] = malloc(sizeof(double[n][n]));
    for (int r = 0; r < n; r++)
        for (int s = 0; s < n; s++)
            B[r][s] = 0;
    for (int t = 0; t < n; t++)
        for (int r = 0; r < n; r++)
            for (int s = 0; s < n; s++)
                B[r][s] += A[r][t] * A[s][t];
    for (int r = 0; r < n; r++)
        for (int s = 0; s < n; s++)
            A[r][s] = B[r][s];
    free(B);
}

void ludcmp(int n, double A[n][n], double b[n], double x[n], double y[n]) {
    double w;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            w = A[i][j];
            for (int k = 0; k < j; k++)
                w -= A[i][k] * A[k][j];
            A[i][j] = w / A[j][j];
        }
        for (int j = i; j < n; j++) {
            w = A[i][j];
            for (int k = 0; k < i; k++)
                w -= A[i][k] * A[k][j];
            A[i][j] = w;
        }
    }

    for (int i = 0; i < n; i++) {
        w = b[i];
        for (int j = 0; j < i; j++)
            w -= A[i][j] * y[j];
        y[i] = w;
    }

    for (int i = n - 1; i >= 0; i--) {
        w = y[i];
        for (int j = i + 1; j < n; j++)
            w -= A[i][j] * x[j];
        x[i] = w / A[i][i];
    }
}

int main() {
    int n = N;
    double (*A)[n] = malloc(sizeof(double[n][n]));
    double *b = malloc(sizeof(double[n]));
    double *x = malloc(sizeof(double[n]));
    double *y = malloc(sizeof(double[n]));

    init_array(n, A, b, x, y);

    clock_t start = clock();
    ludcmp(n, A, b, x, y);
    clock_t end = clock();

    printf("LUDCMP Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", x[0]);

    free(A); free(b); free(x); free(y);
    return 0;
}
