#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; int f5; int f6; } Rec;

Rec arr[109];

int main() {
  for(int i=0;i<109;i++) { arr[i].f0=i*1+2; arr[i].f1=i*2+1; arr[i].f2=i*3+9; arr[i].f3=i*4+7; arr[i].f4=i*5+7; arr[i].f5=i*6+0; arr[i].f6=i*7+9; }
  int s=0; for(int i=0;i<109;i++) if(arr[i].f0 > 36) { s+=arr[i].f0; s+=arr[i].f1; s+=arr[i].f2; s+=arr[i].f3; s+=arr[i].f4; s+=arr[i].f5; s+=arr[i].f6; }
  int t=0; for(int i=0;i<109;i++) t+=arr[i].f0; sink(t);
  return 0;
}
