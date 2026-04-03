#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void sink(int x) { if (x == 0x7FFFFFFF) printf("%d", x); }
int pos; char input[256];
int parse_number() { int n=0; while(input[pos]>='0'&&input[pos]<='9'){n=n*10+(input[pos]-'0');pos++;} return n; }
int parse_factor();
int parse_expr();
int parse_term() { int left=parse_factor(); while(input[pos]=='*'){pos++;left*=parse_factor();} return left; }
int parse_expr() { int left=parse_term(); while(input[pos]=='+'){pos++;left+=parse_term();} return left; }
int parse_factor() { if(input[pos]=='('){pos++;int r=parse_expr();pos++;return r;} return parse_number(); }
int main() { char *s="3+4*2+1"; for(int i=0;s[i];i++)input[i]=s[i]; pos=0; sink(parse_expr()); return 0; }
