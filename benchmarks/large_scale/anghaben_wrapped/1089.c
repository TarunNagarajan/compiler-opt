#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void duplicateZeros(int *arr, int arrSize)
{
    int i, start = 0;
    int *tmp = malloc(arrSize * sizeof(int));
    /* Copy arr into tmp arr */
    for (i = 0; i < arrSize; i++)
    {
        tmp[i] = arr[i];
    }
    i = 0;
    for (start = 0; start < arrSize; start++)
    {
        arr[start] = tmp[i];
        if (tmp[i] == 0)
        {
            start++;
            if (start < arrSize)
                arr[start] = 0;
        }
        i++;
    }
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    duplicateZeros(42, 42);
    volatile int _sink = 0; (void)_sink;
    return 0;
}
