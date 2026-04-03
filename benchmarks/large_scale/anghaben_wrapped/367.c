#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
bool isPerfectSquare(int num)
{
    for (long i = 1; i * i <= num; i++)
        if (i * i == num)
            return true;
    return false;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    bool _result = isPerfectSquare(42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
