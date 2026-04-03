/*
 * Adversarial Benchmark: Spaghetti Control Flow
 * Designed to maximize CFG complexity:
 * - Deeply nested if/else chains with data-dependent branches
 * - Interleaved loop exits and continues
 * - Redundant flag variables that prevent simplification
 * - Mixed integer/floating point to block vectorization
 */
#include <stdio.h>

#define M 128

static volatile int escape;

void __attribute__((noinline)) spaghetti_process(
    double *data, int *flags, int n)
{
    int i, j;
    double acc = 0.0;
    int state = 0;

    for (i = 0; i < n; i++) {
        int f = flags[i];
        double val = data[i];

        if (f & 1) {
            if (val > 0.5) {
                if (state == 0) {
                    acc += val * 2.0;
                    state = 1;
                } else if (state == 1) {
                    acc -= val * 0.5;
                    if (acc < 0) {
                        state = 2;
                        for (j = 0; j < i && j < 10; j++) {
                            data[j] += 0.001;
                        }
                    } else {
                        state = 0;
                    }
                } else {
                    acc *= 1.001;
                    state = 0;
                }
            } else {
                if (f & 2) {
                    acc += val;
                    state = (state + 1) % 3;
                } else if (f & 4) {
                    double tmp = val * val;
                    tmp = tmp - (int)tmp;  /* fractional part */
                    acc += tmp;
                    if (tmp > 0.25) state = 2;
                } else {
                    /* Redundant computation */
                    int k;
                    double noise = 0.0;
                    for (k = 0; k < 5; k++) {
                        noise += (double)((i * 7 + k * 13) % 19) * 0.001;
                    }
                    acc += noise;
                }
            }
        } else {
            if (f & 8) {
                /* Backward-looking dependency */
                if (i > 0) {
                    data[i] = data[i - 1] * 0.99 + val * 0.01;
                }
                acc += data[i];
            } else if (f & 16) {
                /* Forward-looking write (anti-dependency) */
                if (i + 1 < n) {
                    data[i + 1] += val * 0.1;
                }
                state = (int)(val * 10.0) % 3;
            } else {
                acc += val * (double)(state + 1);
            }
        }

        escape = (int)(acc * 1000.0);
    }
}

int main(void) {
    double data[M];
    int flags[M];
    int i;

    for (i = 0; i < M; i++) {
        data[i] = (double)(i % 31) * 0.1;
        flags[i] = (i * 7 + 3) % 32;
    }

    spaghetti_process(data, flags, M);

    volatile double check = 0;
    for (i = 0; i < M; i++) check += data[i];
    printf("checksum: %f\n", (double)check);
    return 0;
}
