#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 44
double u[N][N], v[N][N];

int main() {
  for(int i=0;i<N;i++) for(int j=0;j<N;j++) u[i][j]=(double)(i+j)/N;
  for(int t=0;t<20;t++) {
    for(int i=1;i<N-1;i++) for(int j=1;j<N-1;j++)
      v[i][j]=0.2*(u[i][j]+u[i-1][j]+u[i+1][j]+u[i][j-1]+u[i][j+1]);
    for(int i=0;i<N;i++) for(int j=0;j<N;j++) u[i][j]=v[i][j];
  }
  double s=0; for(int i=0;i<N;i++) for(int j=0;j<N;j++) s+=u[i][j]; fsink(s);
  return 0;
}
