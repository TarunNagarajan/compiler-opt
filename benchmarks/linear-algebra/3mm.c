#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#ifndef NI
#define NI 128
#endif
#ifndef NJ
#define NJ 128
#endif
#ifndef NK
#define NK 128
#endif
#ifndef NL
#define NL 128
#endif
#ifndef NM
#define NM 128
#endif

void init_array(int ni, int nj, int nk, int nl, int nm,
                double A[ni][nk], double B[nk][nj], double C[nj][nm], double D[nm][nl]) {
    for (int i = 0; i < ni; i++) for (int j = 0; j < nk; j++) A[i][j] = (double)((i*j+1) % ni) / ni;
    for (int i = 0; i < nk; i++) for (int j = 0; j < nj; j++) B[i][j] = (double)((i*(j+1)+2) % nj) / nj;
    for (int i = 0; i < nj; i++) for (int j = 0; j < nm; j++) C[i][j] = (double)(i*(j+3) % nm) / nm;
    for (int i = 0; i < nm; i++) for (int j = 0; j < nl; j++) D[i][j] = (double)((i*(j+2)+2) % nl) / nl;
}

void mm3(int ni, int nj, int nk, int nl, int nm,
         double E[ni][nj], double A[ni][nk], double B[nk][nj],
         double F[nj][nl], double C[nj][nm], double D[nm][nl],
         double G[ni][nl]) {
    for (int i = 0; i < ni; i++)
        for (int j = 0; j < nj; j++) {
            E[i][j] = 0.0;
            for (int k = 0; k < nk; k++) E[i][j] += A[i][k] * B[k][j];
        }
    for (int i = 0; i < nj; i++)
        for (int j = 0; j < nl; j++) {
            F[i][j] = 0.0;
            for (int k = 0; k < nm; k++) F[i][j] += C[i][k] * D[k][j];
        }
    for (int i = 0; i < ni; i++)
        for (int j = 0; j < nl; j++) {
            G[i][j] = 0.0;
            for (int k = 0; k < nj; k++) G[i][j] += E[i][k] * F[k][j];
        }
}

int main() {
    int ni=NI, nj=NJ, nk=NK, nl=NL, nm=NM;
    double (*A)[nk] = malloc(sizeof(double[ni][nk]));
    double (*B)[nj] = malloc(sizeof(double[nk][nj]));
    double (*C)[nm] = malloc(sizeof(double[nj][nm]));
    double (*D)[nl] = malloc(sizeof(double[nm][nl]));
    double (*E)[nj] = malloc(sizeof(double[ni][nj]));
    double (*F)[nl] = malloc(sizeof(double[nj][nl]));
    double (*G)[nl] = malloc(sizeof(double[ni][nl]));

    init_array(ni, nj, nk, nl, nm, A, B, C, D);
    clock_t start = clock();
    mm3(ni, nj, nk, nl, nm, E, A, B, F, C, D, G);
    clock_t end = clock();

    printf("3MM Execution Time: %f s\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Result check: %f\n", G[0][0]);

    free(A); free(B); free(C); free(D); free(E); free(F); free(G);
    return 0;
}
