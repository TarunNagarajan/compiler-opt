#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
int main() {
  int state=0, count=0, output=0;
  while(count < 1000) {
    switch(state) {
      case 0: output += count*1; state = (count%5==0) ? 3 : 1; break;
      case 1: output += count*2; state = (count%4==0) ? 4 : 2; break;
      case 2: output += count*3; state = (count%2==0) ? 5 : 3; break;
      case 3: output += count*4; state = (count%7==0) ? 6 : 4; break;
      case 4: output += count*5; state = (count%3==0) ? 7 : 5; break;
      case 5: output += count*6; state = (count%4==0) ? 8 : 6; break;
      case 6: output += count*7; state = (count%2==0) ? 9 : 7; break;
      case 7: output += count*8; state = (count%7==0) ? 10 : 8; break;
      case 8: output += count*9; state = (count%4==0) ? 11 : 9; break;
      case 9: output += count*10; state = (count%5==0) ? 0 : 10; break;
      case 10: output += count*11; state = (count%6==0) ? 1 : 11; break;
      case 11: output += count*12; state = (count%6==0) ? 2 : 0; break;
    }
    count++;
  }
  sink(output);
  return 0;
}
