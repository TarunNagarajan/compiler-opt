#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 21
double A[N][N], B[N][N], C[N][N];

int main() {
  for (int i=0;i<N;i++) for (int j=0;j<N;j++) { A[i][j]=i+j; B[i][j]=i*j+1; C[i][j]=0; }

  for (int i=0;i<N;i++) for (int j=0;j<N;j++) for (int k=0;k<N;k++)
    C[i][j] += A[k][i] * B[k][j];
  double t=0; for(int i=0;i<N;i++) t+=C[i][i]; fsink(t);
  return 0;
}
