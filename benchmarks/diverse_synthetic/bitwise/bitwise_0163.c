#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
unsigned int data[121];

unsigned int rotl(unsigned int v, int n) { return (v << n) | (v >> (32-n)); }

int main() {
  for(int i=0;i<121;i++) data[i] = i * 0x9E3779B9u;
  for(int r=0;r<8;r++) {
    for(int i=0;i<121;i++) {
      data[i] ^= rotl(data[(i+1)%121], 7);
      data[i] += data[(i+44)%121] >> 3;
      data[i] = rotl(data[i], 13);
    }
  }
  unsigned int h=0; for(int i=0;i<121;i++) h^=data[i]; sink((int)h);
  return 0;
}
