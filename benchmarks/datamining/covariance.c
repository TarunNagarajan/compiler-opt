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

void init_array(int m, int n, double *float_n, double data[n][m]) {
    *float_n = (double)n;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            data[i][j] = ((double)i * j) / m;
}

void covariance(int m, int n, double float_n,
                double data[n][m], double cov[m][m], double mean[m]) {
    for (int j = 0; j < m; j++) {
        mean[j] = 0.0;
        for (int i = 0; i < n; i++)
            mean[j] += data[i][j];
        mean[j] /= float_n;
    }

    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            data[i][j] -= mean[j];

    for (int i = 0; i < m; i++)
        for (int j = i; j < m; j++) {
            cov[i][j] = 0.0;
            for (int k = 0; k < n; k++)
                cov[i][j] += data[k][i] * data[k][j];
            cov[i][j] /= (float_n - 1.0);
            cov[j][i] = cov[i][j];
        }
}

int main() {
    int m = M, n = N;
    double float_n;

    double (*data)[m] = malloc(sizeof(double[n][m]));
    double (*cov)[m] = malloc(sizeof(double[m][m]));
    double *mean = malloc(sizeof(double[m]));

    init_array(m, n, &float_n, data);

    clock_t start = clock();
    covariance(m, n, float_n, data, cov, mean);
    clock_t end = clock();

    printf("Covariance Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", cov[0][0]);

    free(data); free(cov); free(mean);
    return 0;
}
