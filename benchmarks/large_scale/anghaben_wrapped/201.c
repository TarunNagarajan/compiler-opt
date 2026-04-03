#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int rangeBitwiseAnd(int m, int n)
{
    while (m < n)
    {
        n &= n - 1;
    }
    return n;
}

/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = rangeBitwiseAnd(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
