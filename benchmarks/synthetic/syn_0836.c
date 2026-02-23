#include <stdio.h>
#include <stdlib.h>

#define N 517
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

    // Kernel 0: vector_add
    {
        for (int i = 0; i < N; i++) {
            C[i] += A[i] + B[i];
        }
    }

    // Kernel 1: vector_add
    {
        for (int i = 0; i < N; i++) {
            C[i] += A[i] + B[i];
        }
    }

    // Prevent Dead Code Elimination
    int total = 0;
    for (int i = 0; i < N; i++) total += C[i];
    sink(total);

    return 0;
}