#include <stdio.h>
#include <stdlib.h>

#define N 999
int A[N];
int B[N];
int C[N];

void sink(int x) {
    if (x == 123456789) printf("%d", x);
}

int main() {
    // Initialize
    for (int i = 0; i < N; i++) {
        A[i] = i;
        B[i] = i * 2;
        C[i] = 0;
    }

    // Kernel 0: matmul_fake
    {
        for (int i = 0; i < N/10; i++) {
            for (int j = 0; j < N/10; j++) {
                C[i] += A[j] * B[j];
            }
        }
    }

    // Kernel 1: branchy
    {
        for (int i = 0; i < N; i++) {
            if (A[i] % 2 == 0) {
                C[i] = A[i] * 3;
            } else {
                C[i] = B[i] + 5;
            }
        }
    }

    // Kernel 2: vector_add
    {
        for (int i = 0; i < N; i++) {
            C[i] += A[i] - B[i];
        }
    }

    // Kernel 3: branchy
    {
        for (int i = 0; i < N; i++) {
            if (A[i] % 2 == 0) {
                C[i] = A[i] * 3;
            } else {
                C[i] = B[i] + 5;
            }
        }
    }

    // Prevent Dead Code Elimination
    int total = 0;
    for (int i = 0; i < N; i++) total += C[i];
    sink(total);

    return 0;
}