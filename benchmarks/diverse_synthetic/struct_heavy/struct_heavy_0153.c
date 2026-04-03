#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; int f5; int f6; int f7; } Rec;

Rec arr[101];

int main() {
  for(int i=0;i<101;i++) { arr[i].f0=i*1+7; arr[i].f1=i*2+8; arr[i].f2=i*3+10; arr[i].f3=i*4+3; arr[i].f4=i*5+4; arr[i].f5=i*6+8; arr[i].f6=i*7+9; arr[i].f7=i*8+7; }
  int s=0; for(int i=0;i<101;i++) if(arr[i].f0 > 33) { s+=arr[i].f0; s+=arr[i].f1; s+=arr[i].f2; s+=arr[i].f3; s+=arr[i].f4; s+=arr[i].f5; s+=arr[i].f6; s+=arr[i].f7; }
  int t=0; for(int i=0;i<101;i++) t+=arr[i].f0; sink(t);
  return 0;
}
