#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
unsigned int data[361];

unsigned int rotl(unsigned int v, int n) { return (v << n) | (v >> (32-n)); }

int main() {
  for(int i=0;i<361;i++) data[i] = i * 0x9E3779B9u;
  for(int r=0;r<15;r++) {
    for(int i=0;i<361;i++) {
      data[i] ^= rotl(data[(i+1)%361], 7);
      data[i] += data[(i+71)%361] >> 3;
      data[i] = rotl(data[i], 13);
    }
  }
  unsigned int h=0; for(int i=0;i<361;i++) h^=data[i]; sink((int)h);
  return 0;
}
