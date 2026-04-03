#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
#define N 17
int adj[N][N], visited[N], queue[N];

int main() {
  memset(adj,0,sizeof(adj)); memset(visited,0,sizeof(visited));
  for(int i=0;i<N;i++) for(int j=i+1;j<N;j++) if((i*7+j*13)%5<2) { adj[i][j]=1; adj[j][i]=1; }
  double rank[N], new_rank[N]; for(int i=0;i<N;i++) rank[i]=1.0/N;
  for(int iter=0;iter<20;iter++) {
    for(int i=0;i<N;i++){new_rank[i]=0.15/N; int deg=0;
      for(int j=0;j<N;j++) deg+=adj[i][j];
      for(int j=0;j<N;j++) if(adj[j][i]) new_rank[i]+=0.85*rank[j]/(deg?deg:1);}
    for(int i=0;i<N;i++) rank[i]=new_rank[i]; }
  int s=0; for(int i=0;i<N;i++) s+=visited[i]; sink(s);
  return 0;
}
