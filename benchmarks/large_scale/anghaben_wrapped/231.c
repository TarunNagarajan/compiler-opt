#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
// Without loops/recursion.
// Runtime: O(1)
// Space: O(1)
bool isPowerOfTwo(int n){
    return (n > 0) && ((n & (n - 1)) == 0);
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    bool _result = isPowerOfTwo(42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
