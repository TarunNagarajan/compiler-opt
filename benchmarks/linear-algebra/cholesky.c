#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#ifndef N
#define N 256
#endif

void init_array(int n, double A[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j <= i; j++)
            A[i][j] = (double)(-j % n) / n + 1;
        for (int j = i + 1; j < n; j++)
            A[i][j] = 0;
        A[i][i] = 1;
    }
    
    int (*B)[n] = malloc(sizeof(int[n][n]));
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

void cholesky(int n, double A[n][n]) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            for (int k = 0; k < j; k++)
                A[i][j] -= A[i][k] * A[j][k];
            A[i][j] /= A[j][j];
        }
        for (int k = 0; k < i; k++)
            A[i][i] -= A[i][k] * A[i][k];
        A[i][i] = sqrt(A[i][i]);
    }
}

int main() {
    int n = N;
    double (*A)[n] = malloc(sizeof(double[n][n]));

    init_array(n, A);

    clock_t start = clock();
    cholesky(n, A);
    clock_t end = clock();

    printf("Cholesky Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", A[0][0]);

    free(A);
    return 0;
}
