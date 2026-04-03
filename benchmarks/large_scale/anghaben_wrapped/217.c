#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
int numcmp(const void *a, const void *b) { return *(int *)a - *(int *)b; }

bool containsDuplicate(int *nums, int numsSize)
{
    int i;
    qsort(nums, numsSize, sizeof(int), numcmp);
    for (i = 0; i < numsSize - 1; i++)
    {
        if (nums[i] == nums[i + 1])
            return 1;
    }
    return 0;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = numcmp(0, 0);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
