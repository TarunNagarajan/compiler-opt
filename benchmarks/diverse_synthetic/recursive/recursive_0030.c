#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void swap(int*a,int i,int j){int t=a[i];a[i]=a[j];a[j]=t;}
int partition(int*a,int lo,int hi){int p=a[hi],i=lo;
  for(int j=lo;j<hi;j++)if(a[j]<p){swap(a,i,j);i++;} swap(a,i,hi); return i;}
void qsort_impl(int*a,int lo,int hi){if(lo<hi){int p=partition(a,lo,hi);qsort_impl(a,lo,p-1);qsort_impl(a,p+1,hi);}}
int main(){int a[128]; for(int i=0;i<128;i++)a[i]=(i*37)%128;
  qsort_impl(a,0,127); sink(a[0]+a[127]); return 0;}
