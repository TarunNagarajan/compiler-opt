#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
char buf[134], out[134];

int main() {
  for(int i=0;i<134-1;i++) buf[i]='a'+(i%26); buf[134-1]=0;
  buf[50]=' '; buf[100]=' '; buf[150]=' ';
  int wc=0,in_word=0; for(int i=0;buf[i];i++){if(buf[i]==' ')in_word=0;else if(!in_word){wc++;in_word=1;}}
  sink(wc);
  int h=0; for(int i=0;i<134;i++) h=h*31+buf[i]; sink(h);
  return 0;
}
