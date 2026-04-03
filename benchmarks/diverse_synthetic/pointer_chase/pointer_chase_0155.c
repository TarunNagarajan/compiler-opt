#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct Node { int val; int next; } Node;
Node pool[62];

int main() {
  for(int i=0;i<62;i++) { pool[i].val=i*3; pool[i].next=(i+1)%62; }
  // Scramble
  for(int i=0;i<62;i++) { int j=(i*7+13)%62; int t=pool[i].next; pool[i].next=pool[j].next; pool[j].next=t; }
  int cur=0, sum=0;
  for(int step=0;step<124;step++) { sum+=pool[cur].val; cur=pool[cur].next; }
  sink(sum);
  return 0;
}
