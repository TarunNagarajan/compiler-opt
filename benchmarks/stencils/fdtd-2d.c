#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#ifndef NX
#define NX 256
#endif
#ifndef NY
#define NY 256
#endif
#ifndef TMAX
#define TMAX 100
#endif

void init_array(int tmax, int nx, int ny,
                double ex[nx][ny], double ey[nx][ny],
                double hz[nx][ny], double _fict_[tmax]) {
    for (int i = 0; i < tmax; i++)
        _fict_[i] = (double)i;
    for (int i = 0; i < nx; i++)
        for (int j = 0; j < ny; j++) {
            ex[i][j] = ((double)i * (j + 1)) / nx;
            ey[i][j] = ((double)i * (j + 2)) / ny;
            hz[i][j] = ((double)i * (j + 3)) / nx;
        }
}

void fdtd_2d(int tmax, int nx, int ny,
             double ex[nx][ny], double ey[nx][ny],
             double hz[nx][ny], double _fict_[tmax]) {
    for (int t = 0; t < tmax; t++) {
        for (int j = 0; j < ny; j++)
            ey[0][j] = _fict_[t];
        for (int i = 1; i < nx; i++)
            for (int j = 0; j < ny; j++)
                ey[i][j] = ey[i][j] - 0.5 * (hz[i][j] - hz[i - 1][j]);
        for (int i = 0; i < nx; i++)
            for (int j = 1; j < ny; j++)
                ex[i][j] = ex[i][j] - 0.5 * (hz[i][j] - hz[i][j - 1]);
        for (int i = 0; i < nx - 1; i++)
            for (int j = 0; j < ny - 1; j++)
                hz[i][j] = hz[i][j] - 0.7 * (ex[i][j + 1] - ex[i][j] + ey[i + 1][j] - ey[i][j]);
    }
}

int main() {
    int tmax = TMAX, nx = NX, ny = NY;

    double (*ex)[ny] = malloc(sizeof(double[nx][ny]));
    double (*ey)[ny] = malloc(sizeof(double[nx][ny]));
    double (*hz)[ny] = malloc(sizeof(double[nx][ny]));
    double *_fict_ = malloc(sizeof(double[tmax]));

    init_array(tmax, nx, ny, ex, ey, hz, _fict_);

    clock_t start = clock();
    fdtd_2d(tmax, nx, ny, ex, ey, hz, _fict_);
    clock_t end = clock();

    printf("FDTD-2D Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", hz[0][0]);

    free(ex); free(ey); free(hz); free(_fict_);
    return 0;
}
