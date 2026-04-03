#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 68
int data[N];

typedef struct { int sum; int count; int min_val; int max_val; } Stats;

void stats_init(Stats *s) { s->sum=0; s->count=0; s->min_val=2147483647; s->max_val=-2147483647; }
void stats_add(Stats *s, int val) { s->sum+=val; s->count++; if(val<s->min_val)s->min_val=val; if(val>s->max_val)s->max_val=val; }
int stats_mean(Stats *s) { return s->count>0 ? s->sum/s->count : 0; }
int stats_range(Stats *s) { return s->max_val - s->min_val; }

int main() {
  for(int i=0;i<N;i++) data[i]=i*2-61;
  Stats st; stats_init(&st);
  for(int i=0;i<N;i++) stats_add(&st, data[i]);
  sink(stats_mean(&st) + stats_range(&st));
  return 0;
}
