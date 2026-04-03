#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
bool isVowel(char chr){
    switch(chr){
        case 'a':
        case 'e':
        case 'i':
        case 'o':
        case 'u':
        case 'A':
        case 'E':
        case 'I':
        case 'O':
        case 'U':
            return true;
    }
    
    return false;
}

// Counting
// Runtime: O(n)
// Space: O(1)
bool halvesAreAlike(char * s){
    int lenS = strlen(s);
    int halfVowels = 0;
    int currVowels = 0;
    
    for (int i = 0; i < lenS; i++){
        if (isVowel(s[i])){
            currVowels++;
        }
        
        if (2 * (i + 1) == lenS){
            halfVowels = currVowels;
        }
    }
    
    return 2 * halfVowels == currVowels;
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    bool _result = isVowel('x');
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
