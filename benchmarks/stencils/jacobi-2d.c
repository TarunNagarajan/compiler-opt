#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 256
#endif
#ifndef TSTEPS
#define TSTEPS 50
#endif

void init_array(int n, double A[n][n], double B[n][n]) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            A[i][j] = ((double)i * (j + 2) + 2) / n;
            B[i][j] = ((double)i * (j + 3) + 3) / n;
        }
}

void jacobi_2d(int tsteps, int n, double A[n][n], double B[n][n]) {
    for (int t = 0; t < tsteps; t++) {
        for (int i = 1; i < n - 1; i++)
            for (int j = 1; j < n - 1; j++)
                B[i][j] = 0.2 * (A[i][j] + A[i][j - 1] + A[i][1 + j] + A[1 + i][j] + A[i - 1][j]);
        for (int i = 1; i < n - 1; i++)
            for (int j = 1; j < n - 1; j++)
                A[i][j] = 0.2 * (B[i][j] + B[i][j - 1] + B[i][1 + j] + B[1 + i][j] + B[i - 1][j]);
    }
}

int main() {
    int n = N;
    int tsteps = TSTEPS;

    double (*A)[n] = malloc(sizeof(double[n][n]));
    double (*B)[n] = malloc(sizeof(double[n][n]));

    init_array(n, A, B);

    clock_t start = clock();
    jacobi_2d(tsteps, n, A, B);
    clock_t end = clock();

    printf("Jacobi-2D Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", A[0][0]);

    free(A); free(B);
    return 0;
}
