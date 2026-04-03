#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void swap(int *x, int *y){
    if (x==y)
        return;
   *x = *x + *y;
    *y= *x - *y;
    *x= *x - *y;
}

void sortColors(int* arr, int n){
    int start=0, mid=0, end=n-1;
    while(mid<=end){
        if(arr[mid]==1)
            mid++;
        else if(arr[mid]==0){
            swap(&arr[mid],&arr[start]);
            mid++;
            start++;
        }
        else{
            swap(&arr[mid],&arr[end]);
            end--;
        }
    }
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    swap(42, 42);
    volatile int _sink = 0; (void)_sink;
    return 0;
}
