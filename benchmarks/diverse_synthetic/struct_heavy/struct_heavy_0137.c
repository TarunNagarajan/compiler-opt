#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; } Rec;

Rec arr[92];

int main() {
  for(int i=0;i<92;i++) { arr[i].f0=i*1+0; arr[i].f1=i*2+4; arr[i].f2=i*3+8; }
  int s=0; for(int i=0;i<92;i++) if(arr[i].f0 > 30) { s+=arr[i].f0; s+=arr[i].f1; s+=arr[i].f2; }
  int t=0; for(int i=0;i<92;i++) t+=arr[i].f0; sink(t);
  return 0;
}
