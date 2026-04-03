#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
char buf[402], out[402];

int main() {
  for(int i=0;i<402-1;i++) buf[i]='a'+(i%26); buf[402-1]=0;
  int j=0,i=0,len=strlen(buf); while(i<len){int c=1;while(i+c<len&&buf[i]==buf[i+c])c++;
    out[j++]=buf[i]; out[j++]='0'+((c>9)?9:c); i+=c;} out[j]=0;
  int h=0; for(int i=0;i<402;i++) h=h*31+buf[i]; sink(h);
  return 0;
}
