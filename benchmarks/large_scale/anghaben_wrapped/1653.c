#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define min(X, Y)  ((X) < (Y) ? (X) : (Y))

// Dynamic programming approach. Down -> Up.
// Runtime: O(n)
// Space: O(1)
int minimumDeletions(char * s){
    int len = strlen(s);
    
    int aStateValue = s[0] == 'b';

    int bStateValue = 0;
    
    int newAStateValue;
    int newBStateValue;

    for(int i = 1; i < len; i++){
        newAStateValue = aStateValue + (s[i] == 'b');

        newBStateValue = min(
                               aStateValue,
                               bStateValue + (s[i] == 'a')
                             );
            
        aStateValue = newAStateValue;
        bStateValue = newBStateValue;
    }
    
    return min(aStateValue, bStateValue);
}


/* --- Auto-generated wrapper for standalone compilation --- */
int main(void) {
    int _result = minimumDeletions("test");
    volatile int _sink = (int)(long long)_result; (void)_sink;
    return 0;
}
