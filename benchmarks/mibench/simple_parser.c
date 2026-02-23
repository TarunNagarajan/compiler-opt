#include <stdio.h>
#include <string.h>
#include <stdbool.h>

typedef enum {
    STATE_IDLE,
    STATE_HEADER,
    STATE_BODY,
    STATE_FOOTER,
    STATE_ERROR
} State;

bool parse_char(char c, State* state, int* count) {
    switch (*state) {
        case STATE_IDLE:
            if (c == '[') {
                *state = STATE_HEADER;
                return true;
            }
            break;
        case STATE_HEADER:
            if (c == ']') {
                *state = STATE_BODY;
                return true;
            } else if (c >= '0' && c <= '9') {
                (*count)++;
                return true;
            }
            *state = STATE_ERROR;
            break;
        case STATE_BODY:
            if (c == '{') {
                return true;
            } else if (c == '}') {
                *state = STATE_FOOTER;
                return true;
            } else if (c == ';') {
                (*count) += 2;
                return true;
            }
            break;
        case STATE_FOOTER:
            if (c == '.') {
                *state = STATE_IDLE;
                return true;
            }
            break;
        case STATE_ERROR:
            return false;
    }
    return true;
}

int main() {
    const char* input = "[123]{abc;def;ghi}.[456]{jk;lm}.";
    int total_processed = 0;
    
    for (int i = 0; i < 10000; i++) {
        State current_state = STATE_IDLE;
        int count = 0;
        for (int j = 0; input[j] != '\0'; j++) {
            if (!parse_char(input[j], &current_state, &count)) {
                break;
            }
        }
        total_processed += count;
    }
    
    return total_processed % 256;
}
