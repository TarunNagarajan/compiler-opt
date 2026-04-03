#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct { int f0; int f1; int f2; } Rec;

Rec arr[138];

int main() {
  for(int i=0;i<138;i++) { arr[i].f0=i*1+2; arr[i].f1=i*2+1; arr[i].f2=i*3+4; }
  for(int i=0;i<138-1;i++) for(int j=i+1;j<138;j++)
    if(arr[i].f0 > arr[j].f0) { Rec t=arr[i]; arr[i]=arr[j]; arr[j]=t; }
  int t=0; for(int i=0;i<138;i++) t+=arr[i].f0; sink(t);
  return 0;
}
