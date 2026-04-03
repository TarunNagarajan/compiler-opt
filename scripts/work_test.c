#include <stdio.h>

void main_test(int n) {
    volatile int x = 0;
    for (int i = 0; i < n; i++) {
        x += (i * 123) % 456;
    }
}

int main() {
    main_test(100000); // 100k loop to take some time
    return 0;
}
