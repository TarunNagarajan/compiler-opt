#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 362
float A[N], B[N], C[N];

int main() {
  for(int i=0;i<N;i++){A[i]=(float)i;B[i]=(float)(N-i);C[i]=0;}
  for(int i=0;i<N;i++) C[i] = 0.62f * A[i] + B[i];
  float t=0; for(int i=0;i<N;i++) t+=C[i]; fsink(t);
  return 0;
}
