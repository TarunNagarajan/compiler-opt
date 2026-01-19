#include <stdio.h>

int square(int x) {
    return x * x;
}

int sum_of_squares(int n) {
    int total = 0;
    for (int i = 1; i <= n; i++) {
        total += square(i);
    }
    return total;
}

void matrix_multiply(int a[3][3], int b[3][3], int c[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            c[i][j] = 0;
            for (int k = 0; k < 3; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
}

int main() {        
    int result = sum_of_squares(10);
    printf("Sum of squares 1-10: %d\n", result);
    
    int a[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int b[3][3] = {{9, 8, 7}, {6, 5, 4}, {3, 2, 1}};
    int c[3][3];
    
    matrix_multiply(a, b, c);
    printf("Matrix C[0][0]: %d\n", c[0][0]);
    
    return 0;
}
