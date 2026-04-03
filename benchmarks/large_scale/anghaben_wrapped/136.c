#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int singleNumber(int *nums, int numsSize)
{
    int i, result = 0;
    for (i = 0; i < numsSize; i++) result = result ^ nums[i];
    return result;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = singleNumber(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
