#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 726
double u[N], v[N];

int main() {
  for(int i=0;i<N;i++) u[i]=(double)i/N;
  for(int t=0;t<63;t++) {
    for(int i=1;i<N-1;i++) v[i]=0.25*u[i-1]+0.5*u[i]+0.25*u[i+1];
    for(int i=0;i<N;i++) u[i]=v[i];
  }
  double s=0; for(int i=0;i<N;i++) s+=u[i]; fsink(s);
  return 0;
}
