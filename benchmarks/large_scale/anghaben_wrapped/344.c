#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void reverseString(char *s, int sSize)
{
    int last = sSize - 1, i;
    for (i = 0; i < last; i++)
    {
        char tmp = s[i];
        s[i] = s[last];
        s[last] = tmp;
        last--;
    }
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    reverseString('x', 42);
    volatile int _sink = 0; (void)_sink;
    return 0;
}
