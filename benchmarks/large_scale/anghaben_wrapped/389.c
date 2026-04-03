#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char findTheDifference(char *s, char *t)
{
    int sum1 = 0, sum2 = 0;
    int i;
    for (i = 0; i < strlen(s); i++) sum1 += s[i];
    for (i = 0; i < strlen(t); i++) sum2 += t[i];
    return (char)(sum2 - sum1);
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    char _result = findTheDifference('x', 'x');
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
