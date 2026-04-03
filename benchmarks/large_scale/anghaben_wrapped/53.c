#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int maxcmp(int a, int b) { return a >= b ? a : b; }

int maxSubArray(int *nums, int numsSize)
{
    int maxSoFar = nums[0], maxEndingHere = nums[0];
    for (int i = 1; i < numsSize; i++)
    {
        maxEndingHere = maxcmp(maxEndingHere + nums[i], nums[i]);
        maxSoFar = maxcmp(maxSoFar, maxEndingHere);
    }
    return maxSoFar;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = maxcmp(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
