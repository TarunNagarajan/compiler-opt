#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; } Rec;

Rec arr[54];

int main() {
  for(int i=0;i<54;i++) { arr[i].f0=i*1+5; arr[i].f1=i*2+7; arr[i].f2=i*3+8; arr[i].f3=i*4+7; }
  int s=0; for(int i=0;i<54;i++) if(arr[i].f0 > 18) { s+=arr[i].f0; s+=arr[i].f1; s+=arr[i].f2; s+=arr[i].f3; }
  int t=0; for(int i=0;i<54;i++) t+=arr[i].f0; sink(t);
  return 0;
}
