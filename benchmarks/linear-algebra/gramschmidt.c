#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#ifndef M
#define M 256
#endif
#ifndef N
#define N 256
#endif

void init_array(int m, int n, double A[m][n]) {
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            A[i][j] = ((double)i * j) / m;
}

void gramschmidt(int m, int n, double A[m][n], double R[n][n], double Q[m][n]) {
    for (int k = 0; k < n; k++) {
        double nrm = 0.0;
        for (int i = 0; i < m; i++) nrm += A[i][k] * A[i][k];
        R[k][k] = sqrt(nrm);
        for (int i = 0; i < m; i++) Q[i][k] = A[i][k] / R[k][k];
        for (int j = k + 1; j < n; j++) {
            R[k][j] = 0.0;
            for (int i = 0; i < m; i++) R[k][j] += Q[i][k] * A[i][j];
            for (int i = 0; i < m; i++) A[i][j] = A[i][j] - Q[i][k] * R[k][j];
        }
    }
}

int main() {
    int m = M, n = N;
    double (*A)[n] = malloc(sizeof(double[m][n]));
    double (*R)[n] = malloc(sizeof(double[n][n]));
    double (*Q)[n] = malloc(sizeof(double[m][n]));

    init_array(m, n, A);
    clock_t start = clock();
    gramschmidt(m, n, A, R, Q);
    clock_t end = clock();

    printf("Gramschmidt Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", R[0][0]);

    free(A); free(R); free(Q);
    return 0;
}
