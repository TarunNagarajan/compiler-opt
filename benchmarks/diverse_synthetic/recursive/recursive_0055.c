#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void merge(int*a,int l,int m,int r){int tmp[256];int i=l,j=m+1,k=0;
  while(i<=m&&j<=r){if(a[i]<=a[j])tmp[k++]=a[i++];else tmp[k++]=a[j++];}
  while(i<=m)tmp[k++]=a[i++]; while(j<=r)tmp[k++]=a[j++];
  for(int p=0;p<k;p++)a[l+p]=tmp[p];}
void msort(int*a,int l,int r){if(l<r){int m=(l+r)/2;msort(a,l,m);msort(a,m+1,r);merge(a,l,m,r);}}
int main(){int a[128]; for(int i=0;i<128;i++)a[i]=128-i;
  msort(a,0,127); sink(a[0]+a[127]); return 0;}
