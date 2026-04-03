#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
bool check(int* nums, int numsSize){
    if (numsSize == 1) {
        return true;
    }
    
    bool wasShift = false;
    for(int i = 1; i < numsSize; i++) {
        if (nums[i - 1] > nums[i]) {
            if (wasShift) {
                return false;
            }

            wasShift = true;
        }
    }
                
    return !wasShift || nums[0] >= nums[numsSize-1];
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    bool _result = check(NULL, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
