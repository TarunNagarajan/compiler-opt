#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 512
#endif

void init_array(int n, double L[n][n], double x[n], double b[n]) {
    for (int i = 0; i < n; i++) {
        x[i] = -999;
        b[i] = i;
        for (int j = 0; j <= i; j++)
            L[i][j] = (double)(i + n - j + 1) * 2 / n;
    }
}

void trisolv(int n, double L[n][n], double x[n], double b[n]) {
    for (int i = 0; i < n; i++) {
        x[i] = b[i];
        for (int j = 0; j < i; j++)
            x[i] -= L[i][j] * x[j];
        x[i] = x[i] / L[i][i];
    }
}

int main() {
    int n = N;
    double (*L)[n] = malloc(sizeof(double[n][n]));
    double *x = malloc(sizeof(double[n]));
    double *b = malloc(sizeof(double[n]));

    init_array(n, L, x, b);

    clock_t start = clock();
    trisolv(n, L, x, b);
    clock_t end = clock();

    printf("Trisolv Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", x[0]);

    free(L); free(x); free(b);
    return 0;
}
