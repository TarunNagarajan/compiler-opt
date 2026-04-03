#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 38
double A[N][N], B[N][N], C[N][N];

int main() {
  for (int i=0;i<N;i++) for (int j=0;j<N;j++) { A[i][j]=i+j; B[i][j]=i*j+1; C[i][j]=0; }

  for (int k=0;k<N-1;k++) for (int i=k+1;i<N;i++) {
    A[i][k] /= (A[k][k] + 1e-10);
    for (int j=k+1;j<N;j++) A[i][j] -= A[i][k]*A[k][j];
  }
  double t=0; for(int i=0;i<N;i++) t+=C[i][i]; fsink(t);
  return 0;
}
