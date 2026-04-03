#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
// Forward declaration of isBadVersion API.
bool isBadVersion(int version);

int firstBadVersion(int n)
{
    int low = 1, high = n;
    while (low <= high)
    {
        int mid = low + (high - low) / 2;
        if (isBadVersion(mid))
        {
            high = mid - 1;
        }
        else
        {
            low = mid + 1;
        }
    }
    return low;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = firstBadVersion(42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
