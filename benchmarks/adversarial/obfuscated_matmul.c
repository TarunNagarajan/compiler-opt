/*
 * Adversarial Benchmark: Obfuscated Matrix Multiply
 * Designed to confuse compiler heuristics:
 * - Pointer aliasing prevents vectorization
 * - Indirect indexing blocks loop analysis
 * - Volatile side-effects prevent dead code elimination
 * - Redundant casts and arithmetic obscure intent
 */
#include <stdio.h>
#include <stdlib.h>

#define N 64

static volatile int sink;

void __attribute__((noinline)) obfuscated_matmul(
    double *restrict A,
    double *restrict B,
    double *restrict C,
    int *idx_map,
    int n)
{
    int i, j, k;
    for (i = 0; i < n; i++) {
        int ii = idx_map[i];  /* indirect indexing */
        for (j = 0; j < n; j++) {
            int jj = idx_map[j];
            double sum = 0.0;
            /* Inner loop with pointer arithmetic instead of array indexing */
            double *a_row = A + (long)ii * n;
            double *b_col_base = B + jj;
            for (k = 0; k < n; k++) {
                /* Obfuscate: cast to char* and back */
                char *ap = (char *)(a_row + k);
                double a_val = *(double *)ap;

                char *bp = (char *)(b_col_base + (long)k * n);
                double b_val = *(double *)bp;

                /* Redundant arithmetic to bloat IR */
                double tmp = a_val * 1.0;
                tmp = tmp + 0.0;
                sum += tmp * b_val;
            }
            /* Write through pointer arithmetic */
            *(C + (long)ii * n + jj) = sum;
            sink = (int)sum;  /* volatile prevents elimination */
        }
    }
}

int main(void) {
    double A[N * N], B[N * N], C[N * N];
    int idx_map[N];
    int i;

    for (i = 0; i < N; i++) idx_map[i] = i;
    for (i = 0; i < N * N; i++) {
        A[i] = (double)(i % 17) * 0.1;
        B[i] = (double)(i % 13) * 0.2;
        C[i] = 0.0;
    }

    obfuscated_matmul(A, B, C, idx_map, N);

    volatile double check = C[0] + C[N * N - 1];
    printf("checksum: %f\n", (double)check);
    return 0;
}
