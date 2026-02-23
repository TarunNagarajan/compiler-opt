#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 512
#endif

void init_array(int n, double r[n]) {
    for (int i = 0; i < n; i++)
        r[i] = (n + 1 - i);
}

void durbin(int n, double r[n], double y[n]) {
    double z[n];
    double alpha, beta, sum;

    y[0] = -r[0];
    beta = 1.0;
    alpha = -r[0];

    for (int k = 1; k < n; k++) {
        beta = (1 - alpha * alpha) * beta;
        sum = 0.0;
        for (int i = 0; i < k; i++)
            sum += r[k - i - 1] * y[i];
        alpha = -(r[k] + sum) / beta;

        for (int i = 0; i < k; i++)
            z[i] = y[i] + alpha * y[k - i - 1];
        for (int i = 0; i < k; i++)
            y[i] = z[i];
        y[k] = alpha;
    }
}

int main() {
    int n = N;
    double *r = malloc(sizeof(double[n]));
    double *y = malloc(sizeof(double[n]));

    init_array(n, r);

    clock_t start = clock();
    durbin(n, r, y);
    clock_t end = clock();

    printf("Durbin Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", y[0]);

    free(r); free(y);
    return 0;
}
