#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int findMaxConsecutiveOnes(int* nums, int numsSize){
    int i=0;
    int maxCount=0;
    int count = 0;
    
    while(i<numsSize){
        
        while(i<numsSize && nums[i]!=0){
            count++;
            i++;
        }
        
        if(maxCount<=count){
         maxCount = count;   
        }
        
        count = 0;
        while(i<numsSize && nums[i]==0){
            i++;
        }
        
    }
    return maxCount;
    
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = findMaxConsecutiveOnes(NULL, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
