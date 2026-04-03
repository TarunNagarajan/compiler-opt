#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; int f5; int f6; int f7; } Rec;

Rec arr[177];

int main() {
  for(int i=0;i<177;i++) { arr[i].f0=i*1+3; arr[i].f1=i*2+5; arr[i].f2=i*3+4; arr[i].f3=i*4+1; arr[i].f4=i*5+6; arr[i].f5=i*6+9; arr[i].f6=i*7+5; arr[i].f7=i*8+2; }
  for(int i=0;i<177;i++) { arr[i].f0 = arr[i].f0 * 3 + arr[i].f1; arr[i].f1 = arr[i].f1 * 3 + arr[i].f2; arr[i].f2 = arr[i].f2 * 3 + arr[i].f3; arr[i].f3 = arr[i].f3 * 3 + arr[i].f4; }
  int t=0; for(int i=0;i<177;i++) t+=arr[i].f0; sink(t);
  return 0;
}
