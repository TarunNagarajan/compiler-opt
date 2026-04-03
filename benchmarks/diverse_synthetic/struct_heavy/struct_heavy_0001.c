#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; int f5; int f6; int f7; } Rec;

Rec arr[58];

int main() {
  for(int i=0;i<58;i++) { arr[i].f0=i*1+2; arr[i].f1=i*2+9; arr[i].f2=i*3+1; arr[i].f3=i*4+4; arr[i].f4=i*5+2; arr[i].f5=i*6+0; arr[i].f6=i*7+1; arr[i].f7=i*8+2; }
  for(int i=0;i<58-1;i++) for(int j=i+1;j<58;j++)
    if(arr[i].f0 > arr[j].f0) { Rec t=arr[i]; arr[i]=arr[j]; arr[j]=t; }
  int t=0; for(int i=0;i<58;i++) t+=arr[i].f0; sink(t);
  return 0;
}
