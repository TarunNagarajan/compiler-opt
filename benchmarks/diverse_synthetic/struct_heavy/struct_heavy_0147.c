#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; } Rec;

Rec arr[125];

int main() {
  for(int i=0;i<125;i++) { arr[i].f0=i*1+8; arr[i].f1=i*2+5; arr[i].f2=i*3+0; }
  for(int i=0;i<125-1;i++) for(int j=i+1;j<125;j++)
    if(arr[i].f0 > arr[j].f0) { Rec t=arr[i]; arr[i]=arr[j]; arr[j]=t; }
  int t=0; for(int i=0;i<125;i++) t+=arr[i].f0; sink(t);
  return 0;
}
