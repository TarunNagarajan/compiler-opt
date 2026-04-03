#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 603
float A[N], B[N], C[N];

int main() {
  for(int i=0;i<N;i++){A[i]=(float)i;B[i]=(float)(N-i);C[i]=0;}
  float norm=0; for(int i=0;i<N;i++) norm+=A[i]*A[i];
  norm=1.0f/(norm+1e-8f); for(int i=0;i<N;i++) C[i]=A[i]*norm;
  float t=0; for(int i=0;i<N;i++) t+=C[i]; fsink(t);
  return 0;
}
