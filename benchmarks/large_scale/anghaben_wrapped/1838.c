#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define max(a,b) (((a)>(b))?(a):(b))

int compare(const int* i, const int* j)
{
    return *i - *j;
}

// Sort + prefix sum + windows sliding
// Runtime: O(n*log(n))
// Space: O(n)
int maxFrequency(int* nums, int numsSize, int k){
    qsort(nums, numsSize, sizeof (int), (int(*) (const void*, const void*)) compare);
    long* prefixSum = malloc(numsSize * sizeof(long));
    
    prefixSum[0] = nums[0];
    for(int i = 0; i < numsSize - 1; i++){
        prefixSum[i + 1] = prefixSum[i] + nums[i];
    }

    int leftWindowPosition = 0;
    int result = 0;
    
    for(int rightWindowPosition = 0; rightWindowPosition < numsSize; rightWindowPosition++){
        long rightSum = prefixSum[rightWindowPosition];
        long leftSum = prefixSum[leftWindowPosition];

        while ((long)nums[rightWindowPosition] * (rightWindowPosition - leftWindowPosition) - (rightSum - leftSum) > k){
            leftWindowPosition += 1;
        }

        result = max(result, rightWindowPosition - leftWindowPosition + 1);
    }

    free(prefixSum);
    return result;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = compare(NULL, NULL);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
