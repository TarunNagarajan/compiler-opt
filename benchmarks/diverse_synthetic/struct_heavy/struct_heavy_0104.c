#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; int f5; int f6; int f7; } Rec;

Rec arr[98];

int main() {
  for(int i=0;i<98;i++) { arr[i].f0=i*1+3; arr[i].f1=i*2+10; arr[i].f2=i*3+4; arr[i].f3=i*4+10; arr[i].f4=i*5+2; arr[i].f5=i*6+3; arr[i].f6=i*7+6; arr[i].f7=i*8+3; }
  int s=0; for(int i=0;i<98;i++) if(arr[i].f0 > 32) { s+=arr[i].f0; s+=arr[i].f1; s+=arr[i].f2; s+=arr[i].f3; s+=arr[i].f4; s+=arr[i].f5; s+=arr[i].f6; s+=arr[i].f7; }
  int t=0; for(int i=0;i<98;i++) t+=arr[i].f0; sink(t);
  return 0;
}
