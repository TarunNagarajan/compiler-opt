#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
bool isAnagram(char *s, char *t)
{
    int n = strlen(s);
    int m = strlen(t);

    int cnt_s[1000], cnt_t[1000];
    for (int c = 97; c < 97 + 26; c++) cnt_s[c] = cnt_t[c] = 0;

    for (int i = 0; i < n; i++) cnt_s[s[i]]++;

    for (int i = 0; i < m; i++) cnt_t[t[i]]++;

    for (int c = 97; c < 97 + 26; c++)
        if (cnt_s[c] != cnt_t[c])
            return false;

    return true;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    bool _result = isAnagram('x', 'x');
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
