#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef M
#define M 512
#endif
#ifndef N
#define N 512
#endif

void init_array(int m, int n, double A[m][n], double p[n], double r[m]) {
    for (int i = 0; i < n; i++) p[i] = (double)i / n;
    for (int i = 0; i < m; i++) r[i] = (double)i / m;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            A[i][j] = (double)(i * (j + 1)) / m;
}

void bicg(int m, int n, double A[m][n], double s[n], double q[m], double p[n], double r[m]) {
    for (int i = 0; i < n; i++) s[i] = 0;
    for (int i = 0; i < m; i++) {
        q[i] = 0.0;
        for (int j = 0; j < n; j++) {
            s[j] += r[i] * A[i][j];
            q[i] += A[i][j] * p[j];
        }
    }
}

int main() {
    int m = M, n = N;
    double (*A)[n] = malloc(sizeof(double[m][n]));
    double *s = malloc(n * sizeof(double));
    double *q = malloc(m * sizeof(double));
    double *p = malloc(n * sizeof(double));
    double *r = malloc(m * sizeof(double));

    init_array(m, n, A, p, r);
    clock_t start = clock();
    bicg(m, n, A, s, q, p, r);
    clock_t end = clock();

    printf("BiCG Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", s[0]);

    free(A); free(s); free(q); free(p); free(r);
    return 0;
}
