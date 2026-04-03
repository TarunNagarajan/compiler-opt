#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int removeElement(int *nums, int numsSize, int val)
{
    int i, start = 0;
    for (i = 0; i < numsSize; i++)
    {
        if (nums[i] != val)
            nums[start++] = nums[i];
    }
    return start;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = removeElement(42, 42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
