#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
int base_compute(int x) { return x * x; }
int level_0(int x) { int pre = x+1; int result = level_1(pre); return result^0xFF; }
int level_1(int x) { int pre = x+1; int result = level_2(pre); return result+3; }
int level_2(int x) { int pre = x+1; int result = level_3(pre); return result^0xFF; }
int level_3(int x) { int pre = x*2; int result = level_4(pre); return result+3; }
int level_4(int x) { int pre = x*2; int result = base_compute(pre); return result%1000000007; }
int main() { int s=0; for(int i=0;i<292;i++) s+=level_0(i); sink(s); return 0; }
