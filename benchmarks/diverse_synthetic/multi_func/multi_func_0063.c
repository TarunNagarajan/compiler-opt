#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 115
int data[N];

int check_bounds(int x) { return x >= 0 && x < 115; }
int check_even(int x) { return x % 2 == 0; }
int check_prime_ish(int x) { if(x<2)return 0; for(int d=2;d*d<=x;d++)if(x%d==0)return 0; return 1; }
int validate(int x) { return check_bounds(x) && (check_even(x) || check_prime_ish(x)); }

int main() {
  for(int i=0;i<N;i++) data[i]=i*3;
  int valid=0; for(int i=0;i<N;i++) valid += validate(data[i]);
  sink(valid);
  return 0;
}
