#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
double powPositive(double x, int n){
    if (n == 1){
        return x;
    }

    double val = powPositive(x, n / 2);
    double result = val * val;
    
    // if n is odd
    if (n & 1 > 0){
        result *= x;
    }

    return result;
}

// Divide and conquer.
// Runtime: O(log(n))
// Space: O(1)
double myPow(double x, int n){
    if (n == 0){
        return 1;
    }

    const int LOWER_BOUND = -2147483648;

    // n is the minimum int, couldn't be converted in -n because maximum is 2147483647.
    // this case we use (1 / pow(x, -(n + 1))) * n
    if (n == LOWER_BOUND){
        return 1 / (powPositive(x, -(n + 1)) * x);
    }

    // 1 / pow(x, -(n + 1))
    if (n < 0){
        return 1 / powPositive(x, -n);
    }

    return powPositive(x, n);
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    double _result = powPositive(1.0, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
