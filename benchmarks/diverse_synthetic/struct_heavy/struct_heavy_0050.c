#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; } Rec;

Rec arr[148];

int main() {
  for(int i=0;i<148;i++) { arr[i].f0=i*1+5; arr[i].f1=i*2+8; arr[i].f2=i*3+6; arr[i].f3=i*4+9; arr[i].f4=i*5+8; }
  for(int i=0;i<148;i++) { arr[i].f0 = arr[i].f0 * 3 + arr[i].f1; arr[i].f1 = arr[i].f1 * 3 + arr[i].f2; arr[i].f2 = arr[i].f2 * 3 + arr[i].f3; arr[i].f3 = arr[i].f3 * 3 + arr[i].f4; }
  int t=0; for(int i=0;i<148;i++) t+=arr[i].f0; sink(t);
  return 0;
}
