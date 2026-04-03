#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int *cmpval(const void *a, const void *b) { return *(int *)b - *(int *)a; }

int findKthLargest(int *nums, int numsSize, int k)
{
    qsort(nums, numsSize, sizeof(int), cmpval);
    return nums[k - 1];
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = findKthLargest(42, 42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
