#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; } Rec;

Rec arr[97];

int main() {
  for(int i=0;i<97;i++) { arr[i].f0=i*1+1; arr[i].f1=i*2+6; arr[i].f2=i*3+9; arr[i].f3=i*4+8; arr[i].f4=i*5+7; }
  int s=0; for(int i=0;i<97;i++) if(arr[i].f0 > 32) { s+=arr[i].f0; s+=arr[i].f1; s+=arr[i].f2; s+=arr[i].f3; s+=arr[i].f4; }
  int t=0; for(int i=0;i<97;i++) t+=arr[i].f0; sink(t);
  return 0;
}
