#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
char buf[356], out[356];

int main() {
  for(int i=0;i<356-1;i++) buf[i]='a'+(i%26); buf[356-1]=0;
  for(int i=0;buf[i];i++) if(buf[i]>='a'&&buf[i]<='z') buf[i]='a'+(buf[i]-'a'+17)%26;
  int h=0; for(int i=0;i<356;i++) h=h*31+buf[i]; sink(h);
  return 0;
}
