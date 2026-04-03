#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
#define N 476
int data[N], idx[N], out[N];

int main() {
  for(int i=0;i<N;i++) { data[i]=i*7%N; idx[i]=(i*13+7)%N; out[i]=0; }
  int bins[32] = {0};
  for(int i=0;i<N;i++) bins[data[i]%32]++;
  int s=0; for(int i=0;i<32;i++) s+=bins[i]; sink(s);
  int t=0; for(int i=0;i<N;i++) t+=out[i]; sink(t);
  return 0;
}
