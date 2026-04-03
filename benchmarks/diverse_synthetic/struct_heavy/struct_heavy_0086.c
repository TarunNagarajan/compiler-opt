#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; int f3; int f4; int f5; } Rec;

Rec arr[198];

int main() {
  for(int i=0;i<198;i++) { arr[i].f0=i*1+0; arr[i].f1=i*2+4; arr[i].f2=i*3+4; arr[i].f3=i*4+2; arr[i].f4=i*5+7; arr[i].f5=i*6+4; }
  for(int i=0;i<198-1;i++) for(int j=i+1;j<198;j++)
    if(arr[i].f0 > arr[j].f0) { Rec t=arr[i]; arr[i]=arr[j]; arr[j]=t; }
  int t=0; for(int i=0;i<198;i++) t+=arr[i].f0; sink(t);
  return 0;
}
