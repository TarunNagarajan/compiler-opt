#include <stdio.h>
#include <stdint.h>

uint32_t reverse_bits(uint32_t n) {
    n = ((n >> 1) & 0x55555555) | ((n << 1) & 0xAAAAAAAA);
    n = ((n >> 2) & 0x33333333) | ((n << 2) & 0xCCCCCCCC);
    n = ((n >> 4) & 0x0F0F0F0F) | ((n << 4) & 0xF0F0F0F0);
    n = ((n >> 8) & 0x00FF00FF) | ((n << 8) & 0xFF00FF00);
    n = ((n >> 16) & 0x0000FFFF) | ((n << 16) & 0xFFFF0000);
    return n;
}

uint32_t count_set_bits(uint32_t n) {
    uint32_t count = 0;
    while (n > 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}

uint32_t interleave_bits(uint16_t x, uint16_t y) {
    uint32_t z = 0;
    for (int i = 0; i < 16; i++) {
        z |= (x & (1 << i)) << i;
        z |= (y & (1 << i)) << (i + 1);
    }
    return z;
}

int main() {
    uint32_t result = 0;
    for (uint32_t i = 0; i < 100000; i++) {
        uint32_t rev = reverse_bits(i);
        uint32_t cnt = count_set_bits(rev);
        uint32_t inl = interleave_bits(i & 0xFFFF, rev & 0xFFFF);
        result ^= rev ^ cnt ^ inl;
    }
    return result % 256;
}
