#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 65
int data[N];

void transform_0(int *arr, int len) {
  for(int i=0;i<len;i++) arr[i] = arr[i] + 5;
}

void transform_1(int *arr, int len) {
  for(int i=0;i<len;i++) arr[i] = arr[i] * 15;
}

void transform_2(int *arr, int len) {
  for(int i=0;i<len;i++) arr[i] = arr[i] ^ 7;
}

int main() {
  for(int i=0;i<N;i++) data[i]=i;
  transform_0(data, N);
  transform_1(data, N);
  transform_2(data, N);
  int s=0; for(int i=0;i<N;i++) s+=data[i]; sink(s);
  return 0;
}
