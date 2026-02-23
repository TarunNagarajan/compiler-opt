#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef N
#define N 256
#endif

#define match(b1, b2) (((b1) + (b2)) == 3 ? 1 : 0)
#define max_score(s1, s2) ((s1 >= s2) ? s1 : s2)

void init_array(int n, char seq[n], int table[n][n]) {
    for (int i = 0; i < n; i++) {
        seq[i] = (char)((i + 1) % 4);
    }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            table[i][j] = 0;
}

void nussinov(int n, char seq[n], int table[n][n]) {
    for (int i = n - 1; i >= 0; i--) {
        for (int j = i + 1; j < n; j++) {
            if (j - 1 >= 0)
                table[i][j] = max_score(table[i][j], table[i][j - 1]);
            if (i + 1 < n)
                table[i][j] = max_score(table[i][j], table[i + 1][j]);

            if (j - 1 >= 0 && i + 1 < n) {
                if (i < j - 1)
                    table[i][j] = max_score(table[i][j],
                                            table[i + 1][j - 1] + match(seq[i], seq[j]));
                else
                    table[i][j] = max_score(table[i][j], table[i + 1][j - 1]);
            }

            for (int k = i + 1; k < j; k++) {
                table[i][j] = max_score(table[i][j], table[i][k] + table[k + 1][j]);
            }
        }
    }
}

int main() {
    int n = N;
    char *seq = malloc(sizeof(char[n]));
    int (*table)[n] = malloc(sizeof(int[n][n]));

    init_array(n, seq, table);

    clock_t start = clock();
    nussinov(n, seq, table);
    clock_t end = clock();

    printf("Nussinov Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %d\n", table[0][n - 1]);

    free(seq); free(table);
    return 0;
}
