#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int peakIndexInMountainArray(int *A, int ASize)
{
    int low = 1, high = ASize;
    while (low <= high)
    {
        int mid = low + (high - low) / 2;
        if (A[mid - 1] < A[mid] && A[mid] > A[mid + 1])
            return mid;
        else if (A[mid - 1] < A[mid] && A[mid] < A[mid + 1])
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = peakIndexInMountainArray(42, 42);
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
