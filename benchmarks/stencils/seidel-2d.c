#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 256
#endif
#ifndef TSTEPS
#define TSTEPS 50
#endif

void init_array(int n, double A[n][n]) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            A[i][j] = ((double)i * (j + 2) + 2) / n;
}

void seidel_2d(int tsteps, int n, double A[n][n]) {
    for (int t = 0; t <= tsteps - 1; t++)
        for (int i = 1; i <= n - 2; i++)
            for (int j = 1; j <= n - 2; j++)
                A[i][j] = (A[i - 1][j - 1] + A[i - 1][j] + A[i - 1][j + 1] + A[i][j - 1] +
                           A[i][j] + A[i][j + 1] + A[i + 1][j - 1] + A[i + 1][j] +
                           A[i + 1][j + 1]) /
                          9.0;
}

int main() {
    int n = N;
    int tsteps = TSTEPS;

    double (*A)[n] = malloc(sizeof(double[n][n]));

    init_array(n, A);

    clock_t start = clock();
    seidel_2d(tsteps, n, A);
    clock_t end = clock();

    printf("Seidel-2D Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", A[0][0]);

    free(A);
    return 0;
}
