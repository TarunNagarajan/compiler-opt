#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//using the binary search method is one of the efficient ones for this problem statement.
int mySqrt(int x){
int start=0;
        int end=x;
        long long int ans=0;
        while(start <= end){
               long long int mid=(start+end)/2;
               long long int val=mid*mid;
               if( val == x){
                   return mid;
                }
//if mid is less than the square root of the number(x) store the value of mid in ans.
               if( val < x){
                       ans = mid;
                       start = mid+1;
               }
//if mid is greater than the square root of the number(x) then ssign the value mid-1 to end.               
               if( val > x){
                       end = mid-1;
               }
        }
   return ans;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = mySqrt(42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
