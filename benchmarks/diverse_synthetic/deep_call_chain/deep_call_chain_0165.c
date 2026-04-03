#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
int level_0(int x) { return level_1(x + 10); }
int level_1(int x) { return level_2(x ^ 6); }
int level_2(int x) { return level_3(x + 8); }
int level_3(int x) { return level_4(x * 5); }
int level_4(int x) { return level_5(x ^ 1); }
int level_5(int x) { return x * 1; }
int main() { int s=0; for(int i=0;i<286;i++) s+=level_0(i); sink(s); return 0; }
