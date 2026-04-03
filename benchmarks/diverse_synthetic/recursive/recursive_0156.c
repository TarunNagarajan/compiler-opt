#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
long long power(long long base,int exp,long long mod){
  long long r=1;base%=mod;while(exp>0){if(exp&1)r=r*base%mod;exp>>=1;base=base*base%mod;}return r;}
int main(){long long s=0;for(int i=1;i<1000;i++)s+=power(i,i%20+1,1000000007);
  sink((int)(s%1000000007));return 0;}
