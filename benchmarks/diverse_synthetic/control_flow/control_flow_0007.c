#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
int main() {
  int state=0, count=0, output=0;
  while(count < 1000) {
    switch(state) {
      case 0: output += count*1; state = (count%7==0) ? 3 : 1; break;
      case 1: output += count*2; state = (count%6==0) ? 4 : 2; break;
      case 2: output += count*3; state = (count%4==0) ? 5 : 3; break;
      case 3: output += count*4; state = (count%2==0) ? 6 : 4; break;
      case 4: output += count*5; state = (count%5==0) ? 0 : 5; break;
      case 5: output += count*6; state = (count%2==0) ? 1 : 6; break;
      case 6: output += count*7; state = (count%5==0) ? 2 : 0; break;
    }
    count++;
  }
  sink(output);
  return 0;
}
