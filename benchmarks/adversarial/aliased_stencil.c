/*
 * Adversarial Benchmark: Aliased Stencil with Function Pointers
 * Designed to be maximally hostile to optimization:
 * - Source and destination arrays may alias (no restrict)
 * - Stencil weights selected via function pointer table
 * - Boundary conditions checked every iteration
 * - Multiple reduction variables with cross-iteration deps
 */
#include <stdio.h>
#include <math.h>

#define GRID 32

static volatile double leak;

typedef double (*weight_fn_t)(int, int);

static double weight_center(int di, int dj) { (void)di; (void)dj; return 0.5; }
static double weight_edge(int di, int dj)   { return 0.125 * (1.0 / (abs(di) + abs(dj) + 1)); }
static double weight_corner(int di, int dj) { return 0.0625 * (di * di + dj * dj > 0 ? 1.0 : 0.0); }

static weight_fn_t weight_table[3] = { weight_center, weight_edge, weight_corner };

void __attribute__((noinline)) aliased_stencil(
    double *src,   /* NOTE: no restrict — may alias dst */
    double *dst,
    int rows, int cols)
{
    int i, j, di, dj;
    double running_max = -1e30;
    double running_sum = 0.0;

    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            double val = 0.0;
            int neighbor_count = 0;

            /* Select weight function based on position */
            int pos_type;
            if (i == 0 || i == rows - 1 || j == 0 || j == cols - 1)
                pos_type = 2;  /* corner/edge */
            else if ((i + j) % 2 == 0)
                pos_type = 1;  /* checkerboard edge */
            else
                pos_type = 0;  /* center */

            weight_fn_t wfn = weight_table[pos_type];

            for (di = -1; di <= 1; di++) {
                int ni = i + di;
                if (ni < 0 || ni >= rows) continue;
                for (dj = -1; dj <= 1; dj++) {
                    int nj = j + dj;
                    if (nj < 0 || nj >= cols) continue;

                    double w = wfn(di, dj);
                    val += src[ni * cols + nj] * w;
                    neighbor_count++;
                }
            }

            if (neighbor_count > 0)
                val /= (double)neighbor_count;

            dst[i * cols + j] = val;
            
            /* Cross-iteration reductions */
            if (val > running_max) running_max = val;
            running_sum += val;
            leak = running_max;
        }
    }
    leak = running_sum;
}

int main(void) {
    double grid[GRID * GRID];
    double out[GRID * GRID];
    int i;

    for (i = 0; i < GRID * GRID; i++) {
        grid[i] = sin((double)i * 0.1) * 100.0;
    }

    /* Run multiple iterations (src/dst swap = aliasing nightmare) */
    aliased_stencil(grid, out, GRID, GRID);
    aliased_stencil(out, grid, GRID, GRID);
    aliased_stencil(grid, out, GRID, GRID);

    volatile double check = 0;
    for (i = 0; i < GRID * GRID; i++) check += out[i];
    printf("checksum: %f\n", (double)check);
    return 0;
}
