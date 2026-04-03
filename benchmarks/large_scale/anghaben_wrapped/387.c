#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int firstUniqChar(char *s)
{
    int *arr = calloc(256, sizeof(int));
    int i;
    for (i = 0; i < strlen(s); i++) arr[s[i]] = arr[s[i]] + 1;
    for (i = 0; i < strlen(s); i++)
    {
        if (arr[s[i]] == 1)
            return i;
    }
    return -1;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = firstUniqChar('x');
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
