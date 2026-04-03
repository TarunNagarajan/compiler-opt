#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 110
int src[N], dst[N], buf[N];

int main() {
  for(int i=0;i<N;i++) src[i]=i;
  memcpy(dst, src, N*sizeof(int));
  for(int i=0;i<N;i++) dst[i] *= 2;
  memmove(buf, dst+N/4, (N/2)*sizeof(int));
  memset(dst, 0, (N/4)*sizeof(int));
  int s=0; for(int i=0;i<N;i++) s+=dst[i]+buf[i%N];
  sink(s);
  return 0;
}
