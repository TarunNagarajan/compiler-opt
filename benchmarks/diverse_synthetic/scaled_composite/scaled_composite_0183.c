#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 508
int A[N], B[N], C[N];
double fA[N], fB[N], fC[N];

void init_int(int *arr, int len, int seed) { for(int i=0;i<len;i++) arr[i]=(i*seed+7)%1000; }
void init_double(double *arr, int len, double base) { for(int i=0;i<len;i++) arr[i]=base+i*0.01; }
int reduce_int(int *arr, int len) { int s=0; for(int i=0;i<len;i++) s+=arr[i]; return s; }
double reduce_double(double *arr, int len) { double s=0; for(int i=0;i<len;i++) s+=arr[i]; return s; }

int main() {
  init_int(A, N, 3); init_int(B, N, 7);
  init_double(fA, N, 1.0); init_double(fB, N, 2.0);

  /* Histogram */
  int bins[64]={0}; for(int i=0;i<N;i++) bins[A[i]%64]++; for(int i=0;i<64;i++) C[i]=bins[i];

  /* SAXPY */
  for(int i=0;i<N;i++) fC[i] = 2.5*fA[i] + fB[i];

  /* 1D stencil */
  for(int t=0;t<10;t++) { for(int i=1;i<N-1;i++) fC[i]=0.25*fA[i-1]+0.5*fA[i]+0.25*fA[i+1]; for(int i=0;i<N;i++) fA[i]=fC[i]; }

  int ri = reduce_int(C, N);
  double rd = reduce_double(fC, N);
  sink(ri); fsink(rd);
  return 0;
}
