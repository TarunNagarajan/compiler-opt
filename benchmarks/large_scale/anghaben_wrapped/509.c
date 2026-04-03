#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int fib(int N)
{
    if (N == 0)
        return 0;
    if (N == 1)
        return 1;
    return fib(N - 1) + fib(N - 2);
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = fib(42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
