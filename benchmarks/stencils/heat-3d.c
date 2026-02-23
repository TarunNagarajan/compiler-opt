#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 64
#endif
#ifndef TSTEPS
#define TSTEPS 20
#endif

void init_array(int n, double A[n][n][n], double B[n][n][n]) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++)
                A[i][j][k] = B[i][j][k] = (double)(i + j + (n - k)) * 10 / (n);
}

void heat_3d(int tsteps, int n, double A[n][n][n], double B[n][n][n]) {
    for (int t = 1; t <= tsteps; t++) {
        for (int i = 1; i < n - 1; i++)
            for (int j = 1; j < n - 1; j++)
                for (int k = 1; k < n - 1; k++)
                    B[i][j][k] = (A[i + 1][j][k] - 2.0 * A[i][j][k] + A[i - 1][j][k]) * 0.125 +
                                 (A[i][j + 1][k] - 2.0 * A[i][j][k] + A[i][j - 1][k]) * 0.125 +
                                 (A[i][j][k + 1] - 2.0 * A[i][j][k] + A[i][j][k - 1]) * 0.125 +
                                 A[i][j][k];
        for (int i = 1; i < n - 1; i++)
            for (int j = 1; j < n - 1; j++)
                for (int k = 1; k < n - 1; k++)
                    A[i][j][k] = (B[i + 1][j][k] - 2.0 * B[i][j][k] + B[i - 1][j][k]) * 0.125 +
                                 (B[i][j + 1][k] - 2.0 * B[i][j][k] + B[i][j - 1][k]) * 0.125 +
                                 (B[i][j][k + 1] - 2.0 * B[i][j][k] + B[i][j][k - 1]) * 0.125 +
                                 B[i][j][k];
    }
}

int main() {
    int n = N;
    int tsteps = TSTEPS;

    double (*A)[n][n] = malloc(sizeof(double[n][n][n]));
    double (*B)[n][n] = malloc(sizeof(double[n][n][n]));

    init_array(n, A, B);

    clock_t start = clock();
    heat_3d(tsteps, n, A, B);
    clock_t end = clock();

    printf("Heat-3D Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", A[0][0][0]);

    free(A); free(B);
    return 0;
}
