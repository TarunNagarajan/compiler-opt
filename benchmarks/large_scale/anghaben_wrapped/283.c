#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void moveZeroes(int *nums, int numsSize)
{
    int i = 0, start = 0;

    for (i = 0; i < numsSize; i++)
    {
        if (nums[i])
            nums[start++] = nums[i];
    }

    for (start; start < numsSize; start++)
    {
        nums[start] = 0;
    }
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    moveZeroes(42, 42);
    volatile int _sink = 0; (void)_sink;
    return 0;
}
