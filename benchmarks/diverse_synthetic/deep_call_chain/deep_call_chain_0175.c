#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
int state_0(int val, int steps);
int state_1(int val, int steps);
int state_2(int val, int steps);
int state_3(int val, int steps);
int state_4(int val, int steps);
int state_0(int val, int steps) {
  if(steps<=0) return val;
  val = val * 2 + 8;
  if(val%4==0) return state_2(val, steps-1);
  return state_1(val, steps-1);
}
int state_1(int val, int steps) {
  if(steps<=0) return val;
  val = val * 4 + 9;
  if(val%2==0) return state_3(val, steps-1);
  return state_2(val, steps-1);
}
int state_2(int val, int steps) {
  if(steps<=0) return val;
  val = val * 2 + 8;
  if(val%3==0) return state_4(val, steps-1);
  return state_3(val, steps-1);
}
int state_3(int val, int steps) {
  if(steps<=0) return val;
  val = val * 3 + 4;
  if(val%3==0) return state_0(val, steps-1);
  return state_4(val, steps-1);
}
int state_4(int val, int steps) {
  if(steps<=0) return val;
  val = val * 3 + 1;
  if(val%3==0) return state_1(val, steps-1);
  return state_0(val, steps-1);
}
int main() { sink(state_0(1, 143)); return 0; }
