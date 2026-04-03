#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// Bit manipulation.
// - Find the bit length of n using log2
// - Create bit mask of bit length of n
// - Retun ~n and bit of ones mask
// Runtime: O(log2(n))
// Space: O(1)

int bitwiseComplement(int n){
    if (n == 0){
        return 1;
    }

    int binary_number_length = ceil(log2(n));
    return (~n) & ((1 << binary_number_length) - 1);
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = bitwiseComplement(42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
