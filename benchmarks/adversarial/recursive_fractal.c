/*
 * Adversarial Benchmark: Recursive Fractal Computation
 * Designed to stress the optimizer with:
 * - Deep recursion (no tail-call optimization possible)
 * - Mixed integer and floating point at every level
 * - Global mutable state modified at each recursion depth
 * - Overlapping reads/writes through a shared buffer
 */
#include <stdio.h>

#define BUF_SIZE 256

static double shared_buf[BUF_SIZE];
static volatile int depth_counter;

double __attribute__((noinline)) fractal_compute(
    double x, double y, int depth, int max_depth)
{
    if (depth >= max_depth) {
        return x * x + y * y;
    }

    depth_counter = depth;

    /* Modify shared state based on position */
    int idx = ((int)(x * 100.0) + (int)(y * 100.0)) & (BUF_SIZE - 1);
    shared_buf[idx] += x * 0.001;

    double nx, ny;
    double mag = x * x + y * y;

    if (mag > 4.0) {
        /* Escaped: do some busywork before returning */
        double decay = 1.0;
        int i;
        for (i = 0; i < depth; i++) {
            decay *= 0.99;
            shared_buf[(idx + i) & (BUF_SIZE - 1)] *= decay;
        }
        return (double)depth + decay;
    }

    /* Mandelbrot-like iteration with twist */
    if (depth % 3 == 0) {
        nx = x * x - y * y + 0.3;
        ny = 2.0 * x * y + 0.5;
    } else if (depth % 3 == 1) {
        nx = x * x * x - 3.0 * x * y * y + 0.1;
        ny = 3.0 * x * x * y - y * y * y + 0.2;
    } else {
        /* Burning ship variant */
        double ax = x < 0 ? -x : x;
        double ay = y < 0 ? -y : y;
        nx = ax * ax - ay * ay - 0.5;
        ny = 2.0 * ax * ay + 0.7;
    }

    /* Two recursive calls — prevents tail-call opt */
    double left = fractal_compute(nx, ny, depth + 1, max_depth);
    double right = fractal_compute(ny, -nx, depth + 1, max_depth);

    /* Combine with data-dependent branch */
    if (left > right)
        return left * 0.6 + right * 0.4 + shared_buf[idx];
    else
        return left * 0.4 + right * 0.6 - shared_buf[idx] * 0.5;
}

int main(void) {
    int i;
    for (i = 0; i < BUF_SIZE; i++) shared_buf[i] = 0.0;

    double total = 0.0;
    int ix, iy;
    for (iy = 0; iy < 8; iy++) {
        for (ix = 0; ix < 8; ix++) {
            double x = (double)ix / 8.0 * 2.0 - 1.0;
            double y = (double)iy / 8.0 * 2.0 - 1.0;
            total += fractal_compute(x, y, 0, 8);
        }
    }

    volatile double check = total;
    printf("checksum: %f\n", (double)check);
    return 0;
}
