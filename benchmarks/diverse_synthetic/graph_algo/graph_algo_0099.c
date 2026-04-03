#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
#define N 61
int adj[N][N], visited[N], queue[N];

int main() {
  memset(adj,0,sizeof(adj)); memset(visited,0,sizeof(visited));
  for(int i=0;i<N;i++) for(int j=i+1;j<N;j++) if((i*7+j*13)%5<2) { adj[i][j]=1; adj[j][i]=1; }
  int stack[N], top=0; stack[top++]=0; visited[0]=1;
  while(top>0) { int u=stack[--top];
    for(int v=0;v<N;v++) if(adj[u][v]&&!visited[v]){visited[v]=1;stack[top++]=v;} }
  int s=0; for(int i=0;i<N;i++) s+=visited[i]; sink(s);
  return 0;
}
