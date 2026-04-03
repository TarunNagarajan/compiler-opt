#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
bool isValid(char *s)
{
    int i, k = 0, len = strlen(s);
    char *store = calloc(len, sizeof(char));

    for (i = 0; s[i] != '\0'; i++)
    {
        switch (s[i])
        {
        case '(':
        case '{':
        case '[':
            store[k++] = s[i];
            break;
        case ')':
            if (k < 1 || store[--k] != '(')
                goto out;
            break;
        case '}':
            if (k < 1 || store[--k] != '{')
                goto out;
            break;
        case ']':
            if (k < 1 || store[--k] != '[')
                goto out;
            break;
        }
    }
out:
    free(store);
    return s[i] == '\0' && k == 0;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    bool _result = isValid('x');
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
