#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 2000
#endif
#ifndef TSTEPS
#define TSTEPS 100
#endif

void init_array(int n, double A[n], double B[n]) {
    for (int i = 0; i < n; i++) {
        A[i] = ((double) i + 2) / n;
        B[i] = ((double) i + 3) / n;
    }
}

void jacobi_1d(int tsteps, int n, double A[n], double B[n]) {
    for (int t = 0; t < tsteps; t++) {
        for (int i = 1; i < n - 1; i++) {
            B[i] = 0.33333 * (A[i-1] + A[i] + A[i+1]);
        }
        for (int i = 1; i < n - 1; i++) {
            A[i] = 0.33333 * (B[i-1] + B[i] + B[i+1]);
        }
    }
}

int main(int argc, char** argv) {
    int n = N;
    int tsteps = TSTEPS;

    double* A = (double*) malloc(n * sizeof(double));
    double* B = (double*) malloc(n * sizeof(double));

    init_array(n, A, B);

    clock_t start = clock();
    jacobi_1d(tsteps, n, A, B);
    clock_t end = clock();

    printf("Jacobi-1D Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", A[0]);

    free(A);
    free(B);
    return 0;
}
