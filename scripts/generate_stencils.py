import os
import random
from pathlib import Path

def generate_stencil_c_file(path, size, dtype, complex_kernel=False):
    """Generates a C file for a heat diffusion stencil operation."""
    kernel_logic = ""
    if complex_kernel:
        # 9-point stencil
        kernel_logic = """
            double center = current->data[y * n + x];
            double n = current->data[(y - 1) * n + x];
            double s = current->data[(y + 1) * n + x];
            double e = current->data[y * n + (x + 1)];
            double w = current->data[y * n + (x - 1)];
            double ne = current->data[(y - 1) * n + (x + 1)];
            double nw = current->data[(y - 1) * n + (x - 1)];
            double se = current->data[(y + 1) * n + (x + 1)];
            double sw = current->data[(y + 1) * n + (x - 1)];
            next->data[y * n + x] = center + 0.1 * (n + s + e + w + ne + nw + se + sw - 8.0 * center);
"""
    else:
        # 5-point stencil
        kernel_logic = """
            double center = current->data[y * n + x];
            double left = current->data[y * n + (x - 1)];
            double right = current->data[y * n + (x + 1)];
            double up = current->data[(y - 1) * n + x];
            double down = current->data[(y + 1) * n + x];
            next->data[y * n + x] = center + 0.1 * (left + right + up + down - 4.0 * center);
"""

    # Use raw string for the code template to avoid escape sequence issues
    code = f"""#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define GRID_SIZE {size}
#define ITERATIONS 100
#define DIFFUSION_RATE 0.1

typedef struct {{
    {dtype} *data;
    int size;
}} Grid;

void init_grid(Grid *g) {{
    g->data = ({dtype} *)malloc(g->size * g->size * sizeof({dtype}));
    for (int i = 0; i < g->size * g->size; i++) {{
        g->data[i] = ({dtype})(rand() % 100);
    }}
}}

void free_grid(Grid *g) {{
    free(g->data);
}}

void diffuse(Grid *current, Grid *next) {{
    int n = current->size;
    for (int y = 1; n - 1 > y; y++) {{
        for (int x = 1; n - 1 > x; x++) {{{kernel_logic}
        }}
    }}
}}

int main() {{
    Grid g1, g2;
    g1.size = GRID_SIZE;
    g2.size = GRID_SIZE;

    init_grid(&g1);
    init_grid(&g2);

    for (int i = 0; i < ITERATIONS; i++) {{
        if (i % 2 == 0) {{
            diffuse(&g1, &g2);
        }} else {{
            diffuse(&g2, &g1);
        }}
    }}

    double sum = 0;
    for (int i = 0; i < g1.size * g1.size; i++) {{
        sum += g1.data[i];
    }}

    // Checksum to prevent dead code elimination
    if (sum > 1e9) {{
        printf("Large sum: %f\\n", sum);
    }}

    free_grid(&g1);
    free_grid(&g2);

    return 0;
}}
"""
    with open(path, 'w') as f:
        f.write(code)

def main():
    """Generates the stencil benchmark suite."""
    stencil_dir = Path("benchmarks/stencils")
    stencil_dir.mkdir(exist_ok=True)
    
    # Clear existing stencils
    for f in stencil_dir.glob("*.c"):
        f.unlink()

    num_files = 50
    sizes = [128, 256, 512]
    dtypes = ["float", "double"]

    print(f"Generating {num_files} stencil benchmarks in {stencil_dir}...")

    for i in range(num_files):
        size = random.choice(sizes)
        dtype = random.choice(dtypes)
        complex_kernel = random.choice([True, False])
        
        fname = f"stencil_{size}_{dtype}_{'9pt' if complex_kernel else '5pt'}_{i:03d}.c"
        fpath = stencil_dir / fname
        
        generate_stencil_c_file(fpath, size, dtype, complex_kernel)

    print("Done.")

if __name__ == "__main__":
    main()
