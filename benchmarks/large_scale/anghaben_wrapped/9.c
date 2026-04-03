#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
bool isPalindrome(int x)
{
    if (x < 0 || (x % 10 == 0 && x != 0))
    {
        return false;
    }

    int revertedNumber = 0;
    while (x > revertedNumber)
    {
        revertedNumber = revertedNumber * 10 + x % 10;
        x /= 10;
    }

    return x == revertedNumber || x == revertedNumber / 10;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    bool _result = isPalindrome(42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
