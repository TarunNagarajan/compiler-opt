#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 169
int data[N];

int map_fn(int x) { return x * x + 1; }
int reduce_fn(int acc, int x) { return acc + x; }
int filter_fn(int x) { return x % 4 != 0; }

void apply_map(int *arr, int len) { for(int i=0;i<len;i++) arr[i]=map_fn(arr[i]); }
int apply_reduce(int *arr, int len) { int acc=0; for(int i=0;i<len;i++) if(filter_fn(arr[i])) acc=reduce_fn(acc,arr[i]); return acc; }

int main() {
  for(int i=0;i<N;i++) data[i]=i;
  apply_map(data, N);
  int result = apply_reduce(data, N);
  sink(result);
  return 0;
}
