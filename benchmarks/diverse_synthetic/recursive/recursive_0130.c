#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
typedef struct Node{int val;int left,right;} Node;
Node tree[255]; int tree_size=0;
int build(int depth){if(depth<=0)return -1;int n=tree_size++;tree[n].val=n;
  tree[n].left=build(depth-1);tree[n].right=build(depth-1);return n;}
int sum(int n){if(n<0)return 0;return tree[n].val+sum(tree[n].left)+sum(tree[n].right);}
int main(){int root=build(7);sink(sum(root));return 0;}
