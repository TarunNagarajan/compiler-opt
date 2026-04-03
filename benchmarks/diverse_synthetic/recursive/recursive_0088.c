#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
long long memo[25];
long long fib(int n){if(n<=1)return n;if(memo[n])return memo[n];return memo[n]=fib(n-1)+fib(n-2);}
int main(){long long r=fib(24);sink((int)(r%1000000007));return 0;}
