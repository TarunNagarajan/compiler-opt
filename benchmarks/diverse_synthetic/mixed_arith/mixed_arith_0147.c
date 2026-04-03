#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

#define N 379
int ia[N]; float fa[N]; double da[N];

int main() {
  for(int i=0;i<N;i++){ia[i]=i;fa[i]=(float)i*0.5f;da[i]=(double)i*0.1;}
  double acc=0; int iacc=0;
  for(int i=0;i<N;i++){iacc+=ia[i]; acc+=da[i]+(double)fa[i];}
  for(int i=0;i<N;i++){iacc+=ia[i]; acc+=da[i]+(double)fa[i];}
  for(int i=0;i<N;i++) fa[i]+=(float)ia[i]*0.01f;
  for(int i=0;i<N;i++) fa[i]+=(float)ia[i]*0.01f;
  for(int i=0;i<N;i++) da[i]=(double)((float)ia[i]*0.7f)+da[i]*0.3;
  for(int i=0;i<N;i++){iacc+=ia[i]; acc+=da[i]+(double)fa[i];}
  fsink(acc+(double)iacc);
  return 0;
}
