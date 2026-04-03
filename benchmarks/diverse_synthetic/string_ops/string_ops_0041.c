#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
char buf[476], out[476];

int main() {
  for(int i=0;i<476-1;i++) buf[i]='a'+(i%26); buf[476-1]=0;
  int len=strlen(buf); for(int i=0;i<len/2;i++){char t=buf[i];buf[i]=buf[len-1-i];buf[len-1-i]=t;}
  int h=0; for(int i=0;i<476;i++) h=h*31+buf[i]; sink(h);
  return 0;
}
