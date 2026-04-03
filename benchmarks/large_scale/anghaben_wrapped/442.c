#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int cmpval(const void *a, const void *b) { return *(int *)a - *(int *)b; }

int *findDuplicates(int *nums, int numsSize, int *returnSize)
{
    int i;
    qsort(nums, numsSize, sizeof(int), cmpval);
    int *retArr = malloc(numsSize * sizeof(int));
    *returnSize = 0;
    for (i = 0; i < numsSize - 1;)
    {
        if (nums[i] == nums[i + 1])
        {
            retArr[*returnSize] = nums[i];
            *returnSize = *returnSize + 1;
            i = i + 2;
        }
        else
        {
            i = i + 1;
        }
    }
    return retArr;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = cmpval(0, 0);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
