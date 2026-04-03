#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

typedef struct { double x; double y; } Point;

int main() {
  Point *pts = (Point*)calloc(57, sizeof(Point));
  if(!pts) return 1;
  for(int i=0;i<57;i++) { pts[i].x = sin(i*0.1); pts[i].y = cos(i*0.1); }
  double total = 0;
  for(int i=0;i<57-1;i++) {
    double dx = pts[i+1].x - pts[i].x;
    double dy = pts[i+1].y - pts[i].y;
    total += sqrt(dx*dx + dy*dy);
  }
  free(pts);
  fsink(total);
  return 0;
}
