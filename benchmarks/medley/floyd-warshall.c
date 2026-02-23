#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 256
#endif

void init_array(int n, int path[n][n]) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            path[i][j] = i * j % 7 + 1;
            if ((i + j) % 13 == 0 || (i + j) % 7 == 0 || (i + j) % 11 == 0)
                path[i][j] = 999;
        }
}

void floyd_warshall(int n, int path[n][n]) {
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                path[i][j] = path[i][j] < path[i][k] + path[k][j]
                                 ? path[i][j]
                                 : path[i][k] + path[k][j];
}

int main() {
    int n = N;
    int (*path)[n] = malloc(sizeof(int[n][n]));

    init_array(n, path);

    clock_t start = clock();
    floyd_warshall(n, path);
    clock_t end = clock();

    printf("Floyd-Warshall Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %d\n", path[0][0]);

    free(path);
    return 0;
}
