#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

int main() {
  double s = 0.0;
  for(int i=1;i<142;i++) {
    s += sqrt((double)i) * log((double)i + 1.0);
    s += sin((double)i * 0.01) * cos((double)i * 0.02);
    s += pow((double)i, 0.5) + fabs(s - (double)(i*i));
  }
  fsink(s);
  return 0;
}
