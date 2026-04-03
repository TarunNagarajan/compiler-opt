#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int cmpval(const void *a, const void *b) { return *(int *)a - *(int *)b; }
int arrayPairSum(int *nums, int numsSize)
{
    int sum = 0, i;
    qsort(nums, numsSize, sizeof(int), cmpval);
    for (i = 0; i < numsSize; i = i + 2) sum = sum + nums[i];
    return sum;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = cmpval(0, 0);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
