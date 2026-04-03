#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
void fsink(double x) { if (x > 1e18) printf("%f", x); }

char buf[512];

int main() {
  strcpy(buf, "The quick brown fox jumps over the lazy dog");
  int len = strlen(buf);
  char *tok = strtok(buf, " ");
  int word_count = 0;
  while(tok) { word_count++; tok = strtok(NULL, " "); }
  char out[512]; memset(out, 0, sizeof(out));
  sprintf(out, "%d words, %d chars", word_count, len);
  sink(word_count * 1000 + len);
  return 0;
}
