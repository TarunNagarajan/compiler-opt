#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 468
int A[N], B[N], C[N];
double fA[N], fB[N], fC[N];

void init_int(int *arr, int len, int seed) { for(int i=0;i<len;i++) arr[i]=(i*seed+7)%1000; }
void init_double(double *arr, int len, double base) { for(int i=0;i<len;i++) arr[i]=base+i*0.01; }
int reduce_int(int *arr, int len) { int s=0; for(int i=0;i<len;i++) s+=arr[i]; return s; }
double reduce_double(double *arr, int len) { double s=0; for(int i=0;i<len;i++) s+=arr[i]; return s; }

int main() {
  init_int(A, N, 3); init_int(B, N, 7);
  init_double(fA, N, 1.0); init_double(fB, N, 2.0);

  /* Flat matmul */
  int M=N/8>0?N/8:4;
  for(int i=0;i<M;i++) for(int j=0;j<M;j++) { int s=0; for(int k=0;k<M;k++) s+=A[i*M+k]*B[k*M+j]; C[i*M+j]=s; }

  /* Branchy filter */
  int valid=0; for(int i=0;i<N;i++) { if(A[i]%3==0 && A[i]>100) { C[valid++]=A[i]; } else if(A[i]%7==0) { C[valid++]=A[i]*2; } }

  /* Bubble sort (small) */
  int sN=N>64?64:N; for(int i=0;i<sN-1;i++) for(int j=i+1;j<sN;j++) if(A[i]>A[j]){int t=A[i];A[i]=A[j];A[j]=t;}

  int ri = reduce_int(C, N);
  double rd = reduce_double(fC, N);
  sink(ri); fsink(rd);
  return 0;
}
