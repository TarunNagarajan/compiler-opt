#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef M
#define M 512
#endif
#ifndef N
#define N 512
#endif

void init_array(int m, int n, double A[m][n], double x[n]) {
    for (int i = 0; i < n; i++) x[i] = 1.0 + (i / (double)n);
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            A[i][j] = ((double)i * (j + 1)) / m;
}

void atax(int m, int n, double A[m][n], double x[n], double y[n], double tmp[m]) {
    for (int i = 0; i < n; i++) y[i] = 0;
    for (int i = 0; i < m; i++) {
        tmp[i] = 0;
        for (int j = 0; j < n; j++) tmp[i] += A[i][j] * x[j];
        for (int j = 0; j < n; j++) y[j] += A[i][j] * tmp[i];
    }
}

int main() {
    int m = M, n = N;
    double (*A)[n] = malloc(sizeof(double[m][n]));
    double *x = malloc(n * sizeof(double));
    double *y = malloc(n * sizeof(double));
    double *tmp = malloc(m * sizeof(double));

    init_array(m, n, A, x);
    clock_t start = clock();
    atax(m, n, A, x, y, tmp);
    clock_t end = clock();

    printf("ATAX Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", y[0]);

    free(A); free(x); free(y); free(tmp);
    return 0;
}
