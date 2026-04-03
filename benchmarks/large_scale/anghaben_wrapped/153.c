#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int findMin(int *nums, int numsSize)
{
    int low = 0, high = numsSize - 1;
    while (low < high)
    {
        int mid = low + (high - low) / 2;
        /* minimum is on left side */
        if (nums[mid] < nums[high])
            high = mid;
        /* minimum is on right side */
        else
            low = mid + 1;
    }
    return nums[low];
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = findMin(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
