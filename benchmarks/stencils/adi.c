#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 256
#endif
#ifndef TSTEPS
#define TSTEPS 50
#endif

void init_array(int n, double u[n][n]) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            u[i][j] = (double)(i + n - j) / n;
}

void adi(int tsteps, int n, double u[n][n], double v[n][n], double p[n][n], double q[n][n]) {
    double DX = 1.0 / (double)n;
    double DY = 1.0 / (double)n;
    double DT = 1.0 / (double)tsteps;
    double B1 = 2.0;
    double B2 = 1.0;
    double mul1 = B1 * DT / (DX * DX);
    double mul2 = B2 * DT / (DY * DY);

    double a = -mul1 / 2.0;
    double b = 1.0 + mul1;
    double c = a;
    double d = -mul2 / 2.0;
    double e = 1.0 + mul2;
    double f = d;

    for (int t = 1; t <= tsteps; t++) {
        
        for (int i = 1; i < n - 1; i++) {
            v[0][i] = 1.0;
            p[i][0] = 0.0;
            q[i][0] = v[0][i];
            for (int j = 1; j < n - 1; j++) {
                p[i][j] = -c / (a * p[i][j - 1] + b);
                q[i][j] = (-d * u[j][i - 1] + (1.0 + 2.0 * d) * u[j][i] - f * u[j][i + 1] -
                           a * q[i][j - 1]) /
                          (a * p[i][j - 1] + b);
            }
            v[n - 1][i] = 1.0;
            for (int j = n - 2; j >= 1; j--)
                v[j][i] = p[i][j] * v[j + 1][i] + q[i][j];
        }
        
        for (int i = 1; i < n - 1; i++) {
            u[i][0] = 1.0;
            p[i][0] = 0.0;
            q[i][0] = u[i][0];
            for (int j = 1; j < n - 1; j++) {
                p[i][j] = -f / (d * p[i][j - 1] + e);
                q[i][j] = (-a * v[i - 1][j] + (1.0 + 2.0 * a) * v[i][j] - c * v[i + 1][j] -
                           d * q[i][j - 1]) /
                          (d * p[i][j - 1] + e);
            }
            u[i][n - 1] = 1.0;
            for (int j = n - 2; j >= 1; j--)
                u[i][j] = p[i][j] * u[i][j + 1] + q[i][j];
        }
    }
}

int main() {
    int n = N;
    int tsteps = TSTEPS;

    double (*u)[n] = malloc(sizeof(double[n][n]));
    double (*v)[n] = malloc(sizeof(double[n][n]));
    double (*p)[n] = malloc(sizeof(double[n][n]));
    double (*q)[n] = malloc(sizeof(double[n][n]));

    init_array(n, u);

    clock_t start = clock();
    adi(tsteps, n, u, v, p, q);
    clock_t end = clock();

    printf("ADI Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", u[0][0]);

    free(u); free(v); free(p); free(q);
    return 0;
}
