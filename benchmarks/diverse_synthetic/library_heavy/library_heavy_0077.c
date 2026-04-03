#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

int main() {
  int *arr = (int*)malloc(120 * sizeof(int));
  if(!arr) return 1;
  for(int i=0;i<120;i++) arr[i] = i * i;
  int s=0; for(int i=0;i<120;i++) s+=arr[i];
  free(arr);
  sink(s);
  return 0;
}
