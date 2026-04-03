#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define GRID_SIZE 256
#define ITERATIONS 100
#define DIFFUSION_RATE 0.1

typedef struct {
    double *data;
    int size;
} Grid;

void init_grid(Grid *g) {
    g->data = (double *)malloc(g->size * g->size * sizeof(double));
    for (int i = 0; i < g->size * g->size; i++) {
        g->data[i] = (double)(rand() % 100);
    }
}

void free_grid(Grid *g) {
    free(g->data);
}

void diffuse(Grid *current, Grid *next) {
    int n = current->size;
    for (int y = 1; n - 1 > y; y++) {
        for (int x = 1; n - 1 > x; x++) {
            double center = current->data[y * n + x];
            double north = current->data[(y - 1) * n + x];
            double s = current->data[(y + 1) * n + x];
            double e = current->data[y * n + (x + 1)];
            double w = current->data[y * n + (x - 1)];
            double ne = current->data[(y - 1) * n + (x + 1)];
            double nw = current->data[(y - 1) * n + (x - 1)];
            double se = current->data[(y + 1) * n + (x + 1)];
            double sw = current->data[(y + 1) * n + (x - 1)];
            next->data[y * n + x] = center + 0.1 * (north + s + e + w + ne + nw + se + sw - 8.0 * center);

        }
    }
}

int main() {
    Grid g1, g2;
    g1.size = GRID_SIZE;
    g2.size = GRID_SIZE;

    init_grid(&g1);
    init_grid(&g2);

    for (int i = 0; i < ITERATIONS; i++) {
        if (i % 2 == 0) {
            diffuse(&g1, &g2);
        } else {
            diffuse(&g2, &g1);
        }
    }

    double sum = 0;
    for (int i = 0; i < g1.size * g1.size; i++) {
        sum += g1.data[i];
    }

    // Checksum to prevent dead code elimination
    if (sum > 1e9) {
        printf("Large sum: %f\n", sum);
    }

    free_grid(&g1);
    free_grid(&g2);

    return 0;
}
