#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#ifndef M
#define M 500
#endif
#ifndef N
#define N 500
#endif

void init_array(int m, int n, double data[m][n]) {
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            data[i][j] = ((double)i*j)/1000.0f;
        }
    }
}

void correlation(int m, int n, double data[m][n], double mean[m], double stddev[m], double symmat[m][m]) {
    double eps = 0.1;

    for (int j = 0; j < m; j++) {
        mean[j] = 0.0;
        for (int i = 0; i < n; i++) {
            mean[j] += data[i][j];
        }
        mean[j] /= (double)n;
    }

    for (int j = 0; j < m; j++) {
        stddev[j] = 0.0;
        for (int i = 0; i < n; i++) {
            stddev[j] += (data[i][j] - mean[j]) * (data[i][j] - mean[j]);
        }
        stddev[j] /= n;
        stddev[j] = sqrt(stddev[j]);
        if (stddev[j] <= eps) stddev[j] = 1.0;
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            data[i][j] -= mean[j];
            data[i][j] /= (sqrt(n) * stddev[j]);
        }
    }

    for (int j1 = 0; j1 < m-1; j1++) {
        symmat[j1][j1] = 1.0;
        for (int j2 = j1+1; j2 < m; j2++) {
            symmat[j1][j2] = 0.0;
            for (int i = 0; i < n; i++) {
                symmat[j1][j2] += (data[i][j1] * data[i][j2]);
            }
            symmat[j2][j1] = symmat[j1][j2];
        }
    }
    symmat[m-1][m-1] = 1.0;
}

int main() {
    int m = M;
    int n = N;

    double (*data)[n] = malloc(sizeof(double[m][n]));
    double *mean = malloc(m * sizeof(double));
    double *stddev = malloc(m * sizeof(double));
    double (*symmat)[m] = malloc(sizeof(double[m][m]));

    init_array(m, n, data);

    clock_t start = clock();
    correlation(m, n, data, mean, stddev, symmat);
    clock_t end = clock();

    printf("Correlation Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", symmat[0][0]);

    free(data);
    free(mean);
    free(stddev);
    free(symmat);
    return 0;
}
