#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#ifndef W
#define W 256
#endif
#ifndef H
#define H 256
#endif

void init_array(int w, int h, double *alpha, double imgIn[w][h]) {
    *alpha = 0.25;
    for (int i = 0; i < w; i++)
        for (int j = 0; j < h; j++)
            imgIn[i][j] = (double)((313 * i + 991 * j) % 65536) / 65535.0;
}

void deriche(int w, int h, double alpha,
             double imgIn[w][h], double imgOut[w][h],
             double y1[w][h], double y2[w][h]) {
    double k;
    double a1, a2, a3, a4, a5, a6, a7, a8;
    double b1, b2, c1, c2;

    k = (1.0 - exp(-alpha)) * (1.0 - exp(-alpha)) /
        (1.0 + 2.0 * alpha * exp(-alpha) - exp(2.0 * alpha));
    a1 = a5 = k;
    a2 = a6 = k * exp(-alpha) * (alpha - 1.0);
    a3 = a7 = k * exp(-alpha) * (alpha + 1.0);
    a4 = a8 = -k * exp(-2.0 * alpha);
    b1 = pow(2.0, -alpha);
    b2 = -exp(-2.0 * alpha);
    c1 = c2 = 1;

    for (int i = 0; i < w; i++) {
        double ym1 = 0.0, ym2 = 0.0, xm1 = 0.0;
        for (int j = 0; j < h; j++) {
            y1[i][j] = a1 * imgIn[i][j] + a2 * xm1 + b1 * ym1 + b2 * ym2;
            xm1 = imgIn[i][j];
            ym2 = ym1;
            ym1 = y1[i][j];
        }
    }

    for (int i = 0; i < w; i++) {
        double yp1 = 0.0, yp2 = 0.0, xp1 = 0.0, xp2 = 0.0;
        for (int j = h - 1; j >= 0; j--) {
            y2[i][j] = a3 * xp1 + a4 * xp2 + b1 * yp1 + b2 * yp2;
            xp2 = xp1;
            xp1 = imgIn[i][j];
            yp2 = yp1;
            yp1 = y2[i][j];
        }
    }

    for (int i = 0; i < w; i++)
        for (int j = 0; j < h; j++)
            imgOut[i][j] = c1 * (y1[i][j] + y2[i][j]);

    for (int j = 0; j < h; j++) {
        double tm1 = 0.0, ym1 = 0.0, ym2 = 0.0;
        for (int i = 0; i < w; i++) {
            y1[i][j] = a5 * imgOut[i][j] + a6 * tm1 + b1 * ym1 + b2 * ym2;
            tm1 = imgOut[i][j];
            ym2 = ym1;
            ym1 = y1[i][j];
        }
    }

    for (int j = 0; j < h; j++) {
        double tp1 = 0.0, tp2 = 0.0, yp1 = 0.0, yp2 = 0.0;
        for (int i = w - 1; i >= 0; i--) {
            y2[i][j] = a7 * tp1 + a8 * tp2 + b1 * yp1 + b2 * yp2;
            tp2 = tp1;
            tp1 = imgOut[i][j];
            yp2 = yp1;
            yp1 = y2[i][j];
        }
    }

    for (int i = 0; i < w; i++)
        for (int j = 0; j < h; j++)
            imgOut[i][j] = c2 * (y1[i][j] + y2[i][j]);
}

int main() {
    int w = W, h = H;
    double alpha;

    double (*imgIn)[h] = malloc(sizeof(double[w][h]));
    double (*imgOut)[h] = malloc(sizeof(double[w][h]));
    double (*y1)[h] = malloc(sizeof(double[w][h]));
    double (*y2)[h] = malloc(sizeof(double[w][h]));

    init_array(w, h, &alpha, imgIn);

    clock_t start = clock();
    deriche(w, h, alpha, imgIn, imgOut, y1, y2);
    clock_t end = clock();

    printf("Deriche Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", imgOut[0][0]);

    free(imgIn); free(imgOut); free(y1); free(y2);
    return 0;
}
