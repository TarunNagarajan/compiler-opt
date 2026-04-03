#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void rotate(int *nums, int numsSize, int k)
{
    for (int i = 1; i <= k; i++)
    {
        int j;
        int lastElement;
        lastElement = nums[numsSize - 1];
        for (j = numsSize - 1; j > 0; j--)
        {
            nums[j] = nums[j - 1];
        }
        nums[0] = lastElement;
    }
}

/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    rotate(42, 42, 42);
    volatile int _sink = 0; (void)_sink;
    return 0;
}
