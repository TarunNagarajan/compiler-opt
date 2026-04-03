#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; } Rec;

Rec arr[102];

int main() {
  for(int i=0;i<102;i++) { arr[i].f0=i*1+3; arr[i].f1=i*2+4; arr[i].f2=i*3+7; arr[i].f3=i*4+4; }
  for(int i=0;i<102;i++) { arr[i].f0 = arr[i].f0 * 3 + arr[i].f1; arr[i].f1 = arr[i].f1 * 3 + arr[i].f2; arr[i].f2 = arr[i].f2 * 3 + arr[i].f3; arr[i].f3 = arr[i].f3 * 3 + arr[i].f0; }
  int t=0; for(int i=0;i<102;i++) t+=arr[i].f0; sink(t);
  return 0;
}
