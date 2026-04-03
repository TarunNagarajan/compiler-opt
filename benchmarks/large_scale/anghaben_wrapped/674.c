#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int findLengthOfLCIS(int *nums, int numsSize)
{
    int maxval = 1, i, count = 1;
    if (numsSize == 0)
        return 0;
    for (i = 1; i < numsSize; i++)
    {
        if (nums[i] > nums[i - 1])
        {
            count++;
            if (count >= maxval)
                maxval = count;
        }
        else
        {
            count = 1;
        }
    }
    return maxval;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = findLengthOfLCIS(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
