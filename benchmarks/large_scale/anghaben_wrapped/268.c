#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int missingNumber(int *nums, int numsSize)
{
    int i, actual_sum = 0, sum = 0;
    for (i = 0; i < numsSize; i++)
    {
        sum = sum + nums[i];
        actual_sum = actual_sum + i;
    }
    return actual_sum + numsSize - sum;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = missingNumber(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
