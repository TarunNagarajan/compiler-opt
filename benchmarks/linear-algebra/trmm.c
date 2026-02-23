#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef M
#define M 256
#endif
#ifndef N
#define N 256
#endif

void init_array(int m, int n, double *alpha, double A[m][m], double B[m][n]) {
    *alpha = 1.5;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < i; j++)
            A[i][j] = (double)((i + j) % m) / m;
        A[i][i] = 1.0;
        for (int j = i + 1; j < m; j++)
            A[i][j] = 0;
        for (int j = 0; j < n; j++)
            B[i][j] = (double)((n + (i - j)) % n) / n;
    }
}

void trmm(int m, int n, double alpha, double A[m][m], double B[m][n]) {
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            for (int k = i + 1; k < m; k++)
                B[i][j] += A[k][i] * B[k][j];
            B[i][j] = alpha * B[i][j];
        }
}

int main() {
    int m = M, n = N;
    double alpha;

    double (*A)[m] = malloc(sizeof(double[m][m]));
    double (*B)[n] = malloc(sizeof(double[m][n]));

    init_array(m, n, &alpha, A, B);

    clock_t start = clock();
    trmm(m, n, alpha, A, B);
    clock_t end = clock();

    printf("TRMM Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", B[0][0]);

    free(A); free(B);
    return 0;
}
