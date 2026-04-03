#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// Prefix sum.
// Collect sum fromleft part and compare it with left sum.
// Runtime: O(n)
// Space: O(1)
int waysToSplitArray(int* nums, int numsSize){
    long sumNums = 0;
    for (int i = 0; i < numsSize; i++){
        sumNums += nums[i];
    }
    
    long prefixSum = 0;
    int result = 0;
    for (int i = 0; i < numsSize - 1; i++){
        prefixSum += nums[i];
        if (prefixSum >= sumNums - prefixSum){
            result += 1;
        }
    }

    return result;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = waysToSplitArray(NULL, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
