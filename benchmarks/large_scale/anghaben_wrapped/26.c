#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int removeDuplicates(int *nums, int numsSize)
{
    int count = 0, i;
    for (i = 1; i < numsSize; i++)
    {
        if (nums[i] == nums[i - 1])
            count++;
        else
            nums[i - count] = nums[i];
    }
    return numsSize - count;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = removeDuplicates(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
