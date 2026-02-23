#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 512
#endif

void init_array(int n, double x1[n], double x2[n], double y_1[n], double y_2[n], double A[n][n]) {
    for (int i = 0; i < n; i++) {
        x1[i] = (double)i / n;
        x2[i] = (double)((i + 1) % n) / n;
        y_1[i] = (double)((i + 3) % n) / n;
        y_2[i] = (double)((i + 4) % n) / n;
        for (int j = 0; j < n; j++)
            A[i][j] = (double)(i * j) / n;
    }
}

void mvt(int n, double x1[n], double x2[n], double y_1[n], double y_2[n], double A[n][n]) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            x1[i] += A[i][j] * y_1[j];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            x2[i] += A[j][i] * y_2[j];
}

int main() {
    int n = N;
    double *x1 = malloc(n * sizeof(double));
    double *x2 = malloc(n * sizeof(double));
    double *y_1 = malloc(n * sizeof(double));
    double *y_2 = malloc(n * sizeof(double));
    double (*A)[n] = malloc(sizeof(double[n][n]));

    init_array(n, x1, x2, y_1, y_2, A);
    clock_t start = clock();
    mvt(n, x1, x2, y_1, y_2, A);
    clock_t end = clock();

    printf("MVT Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", x1[0]);

    free(x1); free(x2); free(y_1); free(y_2); free(A);
    return 0;
}
