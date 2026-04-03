#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

int arr[142];

int cmp(const void *a, const void *b) { return *(const int*)a - *(const int*)b; }

int main() {
  for(int i=0;i<142;i++) arr[i]=(142-i)*7;
  qsort(arr, 142, sizeof(int), cmp);
  sink(arr[0]+arr[141]);
  return 0;
}
