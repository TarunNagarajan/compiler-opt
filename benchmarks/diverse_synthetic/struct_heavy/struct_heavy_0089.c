#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; } Rec;

Rec arr[94];

int main() {
  for(int i=0;i<94;i++) { arr[i].f0=i*1+10; arr[i].f1=i*2+3; arr[i].f2=i*3+10; }
  int s=0; for(int i=0;i<94;i++) if(arr[i].f0 > 31) { s+=arr[i].f0; s+=arr[i].f1; s+=arr[i].f2; }
  int t=0; for(int i=0;i<94;i++) t+=arr[i].f0; sink(t);
  return 0;
}
