#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
int state_0(int val, int steps);
int state_1(int val, int steps);
int state_2(int val, int steps);
int state_3(int val, int steps);
int state_4(int val, int steps);
int state_5(int val, int steps);
int state_6(int val, int steps);
int state_0(int val, int steps) {
  if(steps<=0) return val;
  val = val * 4 + 6;
  if(val%3==0) return state_2(val, steps-1);
  return state_1(val, steps-1);
}
int state_1(int val, int steps) {
  if(steps<=0) return val;
  val = val * 4 + 7;
  if(val%3==0) return state_3(val, steps-1);
  return state_2(val, steps-1);
}
int state_2(int val, int steps) {
  if(steps<=0) return val;
  val = val * 5 + 6;
  if(val%5==0) return state_4(val, steps-1);
  return state_3(val, steps-1);
}
int state_3(int val, int steps) {
  if(steps<=0) return val;
  val = val * 4 + 6;
  if(val%5==0) return state_5(val, steps-1);
  return state_4(val, steps-1);
}
int state_4(int val, int steps) {
  if(steps<=0) return val;
  val = val * 3 + 5;
  if(val%2==0) return state_6(val, steps-1);
  return state_5(val, steps-1);
}
int state_5(int val, int steps) {
  if(steps<=0) return val;
  val = val * 3 + 1;
  if(val%5==0) return state_0(val, steps-1);
  return state_6(val, steps-1);
}
int state_6(int val, int steps) {
  if(steps<=0) return val;
  val = val * 5 + 8;
  if(val%4==0) return state_1(val, steps-1);
  return state_0(val, steps-1);
}
int main() { sink(state_0(1, 191)); return 0; }
