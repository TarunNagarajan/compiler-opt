#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 455
double u[N], v[N];

int main() {
  for(int i=0;i<N;i++) u[i]=(double)i/N;
  for(int t=0;t<23;t++) {
    for(int i=2;i<N-2;i++) v[i]=-u[i-2]+4*u[i-1]+10*u[i]+4*u[i+1]-u[i+2];
    for(int i=0;i<N;i++) u[i]=v[i];
  }
  double s=0; for(int i=0;i<N;i++) s+=u[i]; fsink(s);
  return 0;
}
