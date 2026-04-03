"""
Generate a large, diverse set of self-contained C programs for world model training.
Each program compiles independently with `clang -S -emit-llvm` (no external deps).

Covers 12 code pattern categories to ensure the GNN sees diverse IR structures:
  1. Dense linear algebra (matmul, LU, Cholesky-like)
  2. Sparse/indirect access patterns
  3. Recursive algorithms (sort, tree ops, fibonacci variants)
  4. Control-flow heavy (state machines, dispatch tables)
  5. Struct-heavy data manipulation
  6. Pointer chasing / linked structures
  7. Bitwise / crypto-like operations
  8. SIMD-friendly parallel patterns
  9. Stencil computations (1D/2D)
  10. Graph algorithms (BFS/DFS on adjacency matrix)
  11. String/buffer manipulation
  12. Mixed arithmetic (int + float interleaved)
"""

import os
import random
import argparse
from pathlib import Path

OUTPUT_DIR = Path("benchmarks/diverse_synthetic")
NUM_PER_CATEGORY = 200  # 200 per category × 12 = 2400 programs


def header():
    return "#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\n"


def sink():
    return "void sink(int x) { if (x == 0x7FFFFFFF) printf(\"%d\", x); }\n"


def fsink():
    return "void fsink(double x) { if (x > 1e18) printf(\"%f\", x); }\n\n"


def gen_dense_linalg(seed):
    random.seed(seed)
    n = random.randint(16, 64)
    rows = random.randint(2, 4)
    code = header() + sink() + fsink()
    code += f"#define N {n}\n"
    code += "double A[N][N], B[N][N], C[N][N];\n\n"

    variant = random.choice(["matmul", "transpose_matmul", "lu_like", "symm"])
    code += "int main() {\n"
    code += "  for (int i=0;i<N;i++) for (int j=0;j<N;j++) { A[i][j]=i+j; B[i][j]=i*j+1; C[i][j]=0; }\n\n"

    if variant == "matmul":
        code += "  for (int i=0;i<N;i++) for (int j=0;j<N;j++) for (int k=0;k<N;k++)\n"
        code += "    C[i][j] += A[i][k] * B[k][j];\n"
    elif variant == "transpose_matmul":
        code += "  for (int i=0;i<N;i++) for (int j=0;j<N;j++) for (int k=0;k<N;k++)\n"
        code += "    C[i][j] += A[k][i] * B[k][j];\n"
    elif variant == "lu_like":
        code += "  for (int k=0;k<N-1;k++) for (int i=k+1;i<N;i++) {\n"
        code += "    A[i][k] /= (A[k][k] + 1e-10);\n"
        code += "    for (int j=k+1;j<N;j++) A[i][j] -= A[i][k]*A[k][j];\n  }\n"
    else:
        code += "  for (int i=0;i<N;i++) for (int j=0;j<=i;j++) {\n"
        code += "    double s=0; for (int k=0;k<N;k++) s+=A[i][k]*A[j][k];\n"
        code += "    C[i][j]=s; C[j][i]=s;\n  }\n"

    code += "  double t=0; for(int i=0;i<N;i++) t+=C[i][i]; fsink(t);\n  return 0;\n}\n"
    return code


def gen_sparse_access(seed):
    random.seed(seed)
    n = random.randint(100, 500)
    code = header() + sink()
    code += f"#define N {n}\nint data[N], idx[N], out[N];\n\n"
    code += "int main() {\n"
    code += f"  for(int i=0;i<N;i++) {{ data[i]=i*7%N; idx[i]=(i*13+7)%N; out[i]=0; }}\n"

    variant = random.choice(["gather", "scatter", "histogram", "indirect_chain"])
    if variant == "gather":
        code += "  for(int i=0;i<N;i++) out[i] = data[idx[i]];\n"
    elif variant == "scatter":
        code += "  for(int i=0;i<N;i++) out[idx[i]] += data[i];\n"
    elif variant == "histogram":
        code += f"  int bins[32] = {{0}};\n"
        code += f"  for(int i=0;i<N;i++) bins[data[i]%32]++;\n"
        code += "  int s=0; for(int i=0;i<32;i++) s+=bins[i]; sink(s);\n"
    else:
        code += "  int cur=0;\n  for(int i=0;i<N/2;i++) { cur=idx[cur]; out[i]=data[cur]; }\n"

    code += "  int t=0; for(int i=0;i<N;i++) t+=out[i]; sink(t);\n  return 0;\n}\n"
    return code


def gen_recursive(seed):
    random.seed(seed)
    code = header() + sink()
    variant = random.choice(["mergesort", "quicksort", "fib_memo", "tree_sum", "power",
                             "ackermann", "tower_hanoi", "binary_search_rec"])

    if variant == "mergesort":
        code += "void merge(int*a,int l,int m,int r){int tmp[256];int i=l,j=m+1,k=0;\n"
        code += "  while(i<=m&&j<=r){if(a[i]<=a[j])tmp[k++]=a[i++];else tmp[k++]=a[j++];}\n"
        code += "  while(i<=m)tmp[k++]=a[i++]; while(j<=r)tmp[k++]=a[j++];\n"
        code += "  for(int p=0;p<k;p++)a[l+p]=tmp[p];}\n"
        code += "void msort(int*a,int l,int r){if(l<r){int m=(l+r)/2;msort(a,l,m);msort(a,m+1,r);merge(a,l,m,r);}}\n"
        code += "int main(){int a[128]; for(int i=0;i<128;i++)a[i]=128-i;\n"
        code += "  msort(a,0,127); sink(a[0]+a[127]); return 0;}\n"
    elif variant == "quicksort":
        code += "void swap(int*a,int i,int j){int t=a[i];a[i]=a[j];a[j]=t;}\n"
        code += "int partition(int*a,int lo,int hi){int p=a[hi],i=lo;\n"
        code += "  for(int j=lo;j<hi;j++)if(a[j]<p){swap(a,i,j);i++;} swap(a,i,hi); return i;}\n"
        code += "void qsort_impl(int*a,int lo,int hi){if(lo<hi){int p=partition(a,lo,hi);qsort_impl(a,lo,p-1);qsort_impl(a,p+1,hi);}}\n"
        code += "int main(){int a[128]; for(int i=0;i<128;i++)a[i]=(i*37)%128;\n"
        code += "  qsort_impl(a,0,127); sink(a[0]+a[127]); return 0;}\n"
    elif variant == "fib_memo":
        n = random.randint(20, 40)
        code += f"long long memo[{n+1}];\n"
        code += f"long long fib(int n){{if(n<=1)return n;if(memo[n])return memo[n];return memo[n]=fib(n-1)+fib(n-2);}}\n"
        code += f"int main(){{long long r=fib({n});sink((int)(r%1000000007));return 0;}}\n"
    elif variant == "tree_sum":
        code += "typedef struct Node{int val;int left,right;} Node;\n"
        code += "Node tree[255]; int tree_size=0;\n"
        code += "int build(int depth){if(depth<=0)return -1;int n=tree_size++;tree[n].val=n;\n"
        code += "  tree[n].left=build(depth-1);tree[n].right=build(depth-1);return n;}\n"
        code += "int sum(int n){if(n<0)return 0;return tree[n].val+sum(tree[n].left)+sum(tree[n].right);}\n"
        code += "int main(){int root=build(7);sink(sum(root));return 0;}\n"
    elif variant == "ackermann":
        code += "int ack(int m,int n){if(m==0)return n+1;if(n==0)return ack(m-1,1);return ack(m-1,ack(m,n-1));}\n"
        code += "int main(){sink(ack(3,4));return 0;}\n"
    elif variant == "tower_hanoi":
        code += "int moves=0;\n"
        code += "void hanoi(int n,int from,int to,int aux){if(n<=0)return;hanoi(n-1,from,aux,to);moves++;hanoi(n-1,aux,to,from);}\n"
        code += "int main(){hanoi(15,0,2,1);sink(moves);return 0;}\n"
    elif variant == "binary_search_rec":
        n = random.randint(64, 256)
        code += f"int arr[{n}];\n"
        code += f"int bsearch_r(int lo,int hi,int target){{if(lo>hi)return -1;int m=(lo+hi)/2;if(arr[m]==target)return m;if(arr[m]<target)return bsearch_r(m+1,hi,target);return bsearch_r(lo,m-1,target);}}\n"
        code += f"int main(){{for(int i=0;i<{n};i++)arr[i]=i*3;int s=0;for(int q=0;q<{n*3};q+=7)s+=bsearch_r(0,{n-1},q);sink(s);return 0;}}\n"
    else:
        code += "long long power(long long base,int exp,long long mod){\n"
        code += "  long long r=1;base%=mod;while(exp>0){if(exp&1)r=r*base%mod;exp>>=1;base=base*base%mod;}return r;}\n"
        code += "int main(){long long s=0;for(int i=1;i<1000;i++)s+=power(i,i%20+1,1000000007);\n"
        code += "  sink((int)(s%1000000007));return 0;}\n"
    return code


def gen_control_flow(seed):
    random.seed(seed)
    n_states = random.randint(4, 12)
    code = header() + sink()
    code += "int main() {\n  int state=0, count=0, output=0;\n"
    code += f"  while(count < 1000) {{\n    switch(state) {{\n"
    for s in range(n_states):
        next1 = (s + 1) % n_states
        next2 = (s + 3) % n_states
        code += f"      case {s}: output += count*{s+1}; state = (count%{random.randint(2,7)}==0) ? {next2} : {next1}; break;\n"
    code += "    }\n    count++;\n  }\n  sink(output);\n  return 0;\n}\n"
    return code


def gen_struct_heavy(seed):
    random.seed(seed)
    nf = random.randint(3, 8)
    code = header() + sink()
    fields = [f"int f{i}" for i in range(nf)]
    code += f"typedef struct {{ {'; '.join(fields)}; }} Rec;\n\n"
    n = random.randint(50, 200)
    code += f"Rec arr[{n}];\n\n"
    code += "int main() {\n"
    code += f"  for(int i=0;i<{n};i++) {{ "
    for i in range(nf):
        code += f"arr[i].f{i}=i*{i+1}+{random.randint(0,10)}; "
    code += "}\n"

    variant = random.choice(["sort_field", "filter_sum", "transform"])
    if variant == "sort_field":
        code += f"  for(int i=0;i<{n}-1;i++) for(int j=i+1;j<{n};j++)\n"
        code += f"    if(arr[i].f0 > arr[j].f0) {{ Rec t=arr[i]; arr[i]=arr[j]; arr[j]=t; }}\n"
    elif variant == "filter_sum":
        code += f"  int s=0; for(int i=0;i<{n};i++) if(arr[i].f0 > {n//3}) {{ "
        for i in range(nf):
            code += f"s+=arr[i].f{i}; "
        code += "}\n"
    else:
        code += f"  for(int i=0;i<{n};i++) {{ "
        for i in range(min(nf, 4)):
            code += f"arr[i].f{i} = arr[i].f{i} * 3 + arr[i].f{(i+1)%nf}; "
        code += "}\n"

    code += f"  int t=0; for(int i=0;i<{n};i++) t+=arr[i].f0; sink(t);\n  return 0;\n}}\n"
    return code


def gen_pointer_chase(seed):
    random.seed(seed)
    n = random.randint(50, 200)
    code = header() + sink()
    code += f"typedef struct Node {{ int val; int next; }} Node;\nNode pool[{n}];\n\n"
    code += "int main() {\n"
    code += f"  for(int i=0;i<{n};i++) {{ pool[i].val=i*3; pool[i].next=(i+1)%{n}; }}\n"
    code += f"  // Scramble\n  for(int i=0;i<{n};i++) {{ int j=(i*7+13)%{n}; int t=pool[i].next; pool[i].next=pool[j].next; pool[j].next=t; }}\n"
    code += f"  int cur=0, sum=0;\n  for(int step=0;step<{n*2};step++) {{ sum+=pool[cur].val; cur=pool[cur].next; }}\n"
    code += "  sink(sum);\n  return 0;\n}\n"
    return code


def gen_bitwise(seed):
    random.seed(seed)
    code = header() + sink()
    n = random.randint(100, 500)
    code += f"unsigned int data[{n}];\n\n"
    code += "unsigned int rotl(unsigned int v, int n) { return (v << n) | (v >> (32-n)); }\n\n"
    code += "int main() {\n"
    code += f"  for(int i=0;i<{n};i++) data[i] = i * 0x9E3779B9u;\n"

    rounds = random.randint(4, 16)
    code += f"  for(int r=0;r<{rounds};r++) {{\n"
    code += f"    for(int i=0;i<{n};i++) {{\n"
    code += f"      data[i] ^= rotl(data[(i+1)%{n}], 7);\n"
    code += f"      data[i] += data[(i+{random.randint(2,n//2)})%{n}] >> 3;\n"
    code += f"      data[i] = rotl(data[i], 13);\n"
    code += "    }\n  }\n"
    code += f"  unsigned int h=0; for(int i=0;i<{n};i++) h^=data[i]; sink((int)h);\n  return 0;\n}}\n"
    return code


def gen_simd_friendly(seed):
    random.seed(seed)
    n = random.randint(256, 1024)
    code = header() + sink() + fsink()
    code += f"#define N {n}\nfloat A[N], B[N], C[N];\n\n"
    code += "int main() {\n"
    code += "  for(int i=0;i<N;i++){A[i]=(float)i;B[i]=(float)(N-i);C[i]=0;}\n"

    variant = random.choice(["saxpy", "dot", "normalize", "clamp_add"])
    if variant == "saxpy":
        alpha = random.uniform(0.5, 3.0)
        code += f"  for(int i=0;i<N;i++) C[i] = {alpha:.2f}f * A[i] + B[i];\n"
    elif variant == "dot":
        code += "  float d=0; for(int i=0;i<N;i++) d += A[i]*B[i]; fsink(d);\n"
    elif variant == "normalize":
        code += "  float norm=0; for(int i=0;i<N;i++) norm+=A[i]*A[i];\n"
        code += "  norm=1.0f/(norm+1e-8f); for(int i=0;i<N;i++) C[i]=A[i]*norm;\n"
    else:
        code += "  for(int i=0;i<N;i++){float v=A[i]+B[i]; C[i]=(v<0)?0:(v>1000)?1000:v;}\n"

    code += "  float t=0; for(int i=0;i<N;i++) t+=C[i]; fsink(t);\n  return 0;\n}\n"
    return code


def gen_stencil(seed):
    random.seed(seed)
    variant = random.choice(["1d_3pt", "1d_5pt", "2d_5pt", "2d_9pt"])
    code = header() + fsink()

    if variant.startswith("1d"):
        n = random.randint(200, 1000)
        code += f"#define N {n}\ndouble u[N], v[N];\n\n"
        code += "int main() {\n  for(int i=0;i<N;i++) u[i]=(double)i/N;\n"
        iters = random.randint(10, 100)
        code += f"  for(int t=0;t<{iters};t++) {{\n"
        if "3pt" in variant:
            code += "    for(int i=1;i<N-1;i++) v[i]=0.25*u[i-1]+0.5*u[i]+0.25*u[i+1];\n"
        else:
            code += "    for(int i=2;i<N-2;i++) v[i]=-u[i-2]+4*u[i-1]+10*u[i]+4*u[i+1]-u[i+2];\n"
        code += "    for(int i=0;i<N;i++) u[i]=v[i];\n  }\n"
        code += "  double s=0; for(int i=0;i<N;i++) s+=u[i]; fsink(s);\n  return 0;\n}\n"
    else:
        n = random.randint(16, 48)
        code += f"#define N {n}\ndouble u[N][N], v[N][N];\n\n"
        code += "int main() {\n  for(int i=0;i<N;i++) for(int j=0;j<N;j++) u[i][j]=(double)(i+j)/N;\n"
        iters = random.randint(5, 30)
        code += f"  for(int t=0;t<{iters};t++) {{\n"
        if "5pt" in variant:
            code += "    for(int i=1;i<N-1;i++) for(int j=1;j<N-1;j++)\n"
            code += "      v[i][j]=0.2*(u[i][j]+u[i-1][j]+u[i+1][j]+u[i][j-1]+u[i][j+1]);\n"
        else:
            code += "    for(int i=1;i<N-1;i++) for(int j=1;j<N-1;j++)\n"
            code += "      v[i][j]=(4*u[i][j]+u[i-1][j]+u[i+1][j]+u[i][j-1]+u[i][j+1]\n"
            code += "              +u[i-1][j-1]+u[i-1][j+1]+u[i+1][j-1]+u[i+1][j+1])/12.0;\n"
        code += "    for(int i=0;i<N;i++) for(int j=0;j<N;j++) u[i][j]=v[i][j];\n  }\n"
        code += "  double s=0; for(int i=0;i<N;i++) for(int j=0;j<N;j++) s+=u[i][j]; fsink(s);\n  return 0;\n}\n"
    return code


def gen_graph_algo(seed):
    random.seed(seed)
    n = random.randint(16, 64)
    code = header() + sink()
    code += f"#define N {n}\nint adj[N][N], visited[N], queue[N];\n\n"
    code += "int main() {\n"
    code += "  memset(adj,0,sizeof(adj)); memset(visited,0,sizeof(visited));\n"
    code += f"  for(int i=0;i<N;i++) for(int j=i+1;j<N;j++) if((i*7+j*13)%5<2) {{ adj[i][j]=1; adj[j][i]=1; }}\n"

    variant = random.choice(["bfs", "dfs_iter", "pagerank_like"])
    if variant == "bfs":
        code += "  int front=0,back=0; queue[back++]=0; visited[0]=1;\n"
        code += "  while(front<back) { int u=queue[front++];\n"
        code += "    for(int v=0;v<N;v++) if(adj[u][v]&&!visited[v]){visited[v]=1;queue[back++]=v;} }\n"
    elif variant == "dfs_iter":
        code += "  int stack[N], top=0; stack[top++]=0; visited[0]=1;\n"
        code += "  while(top>0) { int u=stack[--top];\n"
        code += "    for(int v=0;v<N;v++) if(adj[u][v]&&!visited[v]){visited[v]=1;stack[top++]=v;} }\n"
    else:
        code += "  double rank[N], new_rank[N]; for(int i=0;i<N;i++) rank[i]=1.0/N;\n"
        code += "  for(int iter=0;iter<20;iter++) {\n"
        code += "    for(int i=0;i<N;i++){new_rank[i]=0.15/N; int deg=0;\n"
        code += "      for(int j=0;j<N;j++) deg+=adj[i][j];\n"
        code += "      for(int j=0;j<N;j++) if(adj[j][i]) new_rank[i]+=0.85*rank[j]/(deg?deg:1);}\n"
        code += "    for(int i=0;i<N;i++) rank[i]=new_rank[i]; }\n"

    code += "  int s=0; for(int i=0;i<N;i++) s+=visited[i]; sink(s);\n  return 0;\n}\n"
    return code


def gen_string_ops(seed):
    random.seed(seed)
    code = header() + sink()
    n = random.randint(128, 512)
    code += f"char buf[{n}], out[{n}];\n\n"
    code += "int main() {\n"
    code += f"  for(int i=0;i<{n}-1;i++) buf[i]='a'+(i%26); buf[{n}-1]=0;\n"

    variant = random.choice(["reverse", "compress_rle", "count_words", "caesar"])
    if variant == "reverse":
        code += f"  int len=strlen(buf); for(int i=0;i<len/2;i++){{char t=buf[i];buf[i]=buf[len-1-i];buf[len-1-i]=t;}}\n"
    elif variant == "compress_rle":
        code += "  int j=0,i=0,len=strlen(buf); while(i<len){int c=1;while(i+c<len&&buf[i]==buf[i+c])c++;\n"
        code += "    out[j++]=buf[i]; out[j++]='0'+((c>9)?9:c); i+=c;} out[j]=0;\n"
    elif variant == "count_words":
        code += "  buf[50]=' '; buf[100]=' '; buf[150]=' ';\n"
        code += "  int wc=0,in_word=0; for(int i=0;buf[i];i++){if(buf[i]==' ')in_word=0;else if(!in_word){wc++;in_word=1;}}\n"
        code += "  sink(wc);\n"
    else:
        shift = random.randint(1, 25)
        code += f"  for(int i=0;buf[i];i++) if(buf[i]>='a'&&buf[i]<='z') buf[i]='a'+(buf[i]-'a'+{shift})%26;\n"

    code += f"  int h=0; for(int i=0;i<{n};i++) h=h*31+buf[i]; sink(h);\n  return 0;\n}}\n"
    return code


def gen_mixed_arithmetic(seed):
    random.seed(seed)
    n = random.randint(100, 500)
    code = header() + sink() + fsink()
    code += f"#define N {n}\nint ia[N]; float fa[N]; double da[N];\n\n"
    code += "int main() {\n"
    code += "  for(int i=0;i<N;i++){ia[i]=i;fa[i]=(float)i*0.5f;da[i]=(double)i*0.1;}\n"

    code += "  double acc=0; int iacc=0;\n"
    ops = random.randint(3, 8)
    for _ in range(ops):
        variant = random.choice(["int_to_float", "float_to_int", "mixed_reduce", "cast_chain"])
        if variant == "int_to_float":
            code += "  for(int i=0;i<N;i++) fa[i]+=(float)ia[i]*0.01f;\n"
        elif variant == "float_to_int":
            code += "  for(int i=0;i<N;i++) ia[i]+=(int)(fa[i]*10.0f);\n"
        elif variant == "mixed_reduce":
            code += "  for(int i=0;i<N;i++){iacc+=ia[i]; acc+=da[i]+(double)fa[i];}\n"
        else:
            code += "  for(int i=0;i<N;i++) da[i]=(double)((float)ia[i]*0.7f)+da[i]*0.3;\n"

    code += "  fsink(acc+(double)iacc);\n  return 0;\n}\n"
    return code


def gen_multi_func(seed):
    """Programs with 3-5 helper functions called from main().
    Exercises: inline, argpromotion, deadargelim, ipsccp."""
    random.seed(seed)
    code = header() + sink() + fsink()
    n = random.randint(64, 256)
    num_helpers = random.randint(3, 5)
    variant = random.choice(["pipeline", "map_reduce", "builder_pattern", "validator_chain"])

    code += f"#define N {n}\nint data[N];\n\n"

    if variant == "pipeline":
        # Chain of transformation functions
        for h in range(num_helpers):
            op = random.choice(["+", "*", "^", "|", "&"])
            c = random.randint(1, 15)
            code += f"void transform_{h}(int *arr, int len) {{\n"
            code += f"  for(int i=0;i<len;i++) arr[i] = arr[i] {op} {c};\n}}\n\n"
        code += "int main() {\n"
        code += f"  for(int i=0;i<N;i++) data[i]=i;\n"
        for h in range(num_helpers):
            code += f"  transform_{h}(data, N);\n"
        code += "  int s=0; for(int i=0;i<N;i++) s+=data[i]; sink(s);\n  return 0;\n}\n"

    elif variant == "map_reduce":
        # Separate map and reduce functions
        code += "int map_fn(int x) { return x * x + 1; }\n"
        code += "int reduce_fn(int acc, int x) { return acc + x; }\n"
        code += f"int filter_fn(int x) {{ return x % {random.randint(2,7)} != 0; }}\n\n"
        code += "void apply_map(int *arr, int len) { for(int i=0;i<len;i++) arr[i]=map_fn(arr[i]); }\n"
        code += "int apply_reduce(int *arr, int len) { int acc=0; for(int i=0;i<len;i++) if(filter_fn(arr[i])) acc=reduce_fn(acc,arr[i]); return acc; }\n\n"
        code += "int main() {\n"
        code += f"  for(int i=0;i<N;i++) data[i]=i;\n"
        code += "  apply_map(data, N);\n"
        code += "  int result = apply_reduce(data, N);\n"
        code += "  sink(result);\n  return 0;\n}\n"

    elif variant == "builder_pattern":
        # Struct + multiple init/process/finalize functions
        code += "typedef struct { int sum; int count; int min_val; int max_val; } Stats;\n\n"
        code += "void stats_init(Stats *s) { s->sum=0; s->count=0; s->min_val=2147483647; s->max_val=-2147483647; }\n"
        code += "void stats_add(Stats *s, int val) { s->sum+=val; s->count++; if(val<s->min_val)s->min_val=val; if(val>s->max_val)s->max_val=val; }\n"
        code += "int stats_mean(Stats *s) { return s->count>0 ? s->sum/s->count : 0; }\n"
        code += "int stats_range(Stats *s) { return s->max_val - s->min_val; }\n\n"
        code += "int main() {\n"
        code += f"  for(int i=0;i<N;i++) data[i]=i*{random.randint(2,10)}-{random.randint(0,100)};\n"
        code += "  Stats st; stats_init(&st);\n"
        code += "  for(int i=0;i<N;i++) stats_add(&st, data[i]);\n"
        code += "  sink(stats_mean(&st) + stats_range(&st));\n  return 0;\n}\n"

    else:  # validator_chain
        code += f"int check_bounds(int x) {{ return x >= 0 && x < {n}; }}\n"
        code += f"int check_even(int x) {{ return x % 2 == 0; }}\n"
        code += f"int check_prime_ish(int x) {{ if(x<2)return 0; for(int d=2;d*d<=x;d++)if(x%d==0)return 0; return 1; }}\n"
        code += "int validate(int x) { return check_bounds(x) && (check_even(x) || check_prime_ish(x)); }\n\n"
        code += "int main() {\n"
        code += f"  for(int i=0;i<N;i++) data[i]=i*3;\n"
        code += "  int valid=0; for(int i=0;i<N;i++) valid += validate(data[i]);\n"
        code += "  sink(valid);\n  return 0;\n}\n"

    return code


def gen_deep_call_chain(seed):
    """Programs with 4-6 levels of function nesting.
    Exercises: inline, tailcallelim, callsite-splitting, argpromotion."""
    random.seed(seed)
    code = header() + sink()
    depth = random.randint(4, 6)
    variant = random.choice(["accumulator", "decorator", "recursive_descent", "state_machine_funcs"])

    if variant == "accumulator":
        # Each level adds something and calls the next
        for d in range(depth):
            op = random.choice(["+", "^", "*"])
            c = random.randint(1, 10)
            if d == depth - 1:
                code += f"int level_{d}(int x) {{ return x {op} {c}; }}\n"
            else:
                code += f"int level_{d}(int x) {{ return level_{d+1}(x {op} {c}); }}\n"
        n = random.randint(100, 500)
        code += f"int main() {{ int s=0; for(int i=0;i<{n};i++) s+=level_0(i); sink(s); return 0; }}\n"

    elif variant == "decorator":
        # Each function wraps the next, adding pre/post processing
        code += f"int base_compute(int x) {{ return x * x; }}\n"
        for d in range(depth - 1):
            inner = f"level_{d+1}" if d < depth - 2 else "base_compute"
            pre_op = random.choice(["+1", "-1", "*2", "/2+1"])
            post_op = random.choice(["+3", "^0xFF", "%1000000007", "+7"])
            code += f"int level_{d}(int x) {{ int pre = x{pre_op}; int result = {inner}(pre); return result{post_op}; }}\n"
        n = random.randint(100, 500)
        code += f"int main() {{ int s=0; for(int i=0;i<{n};i++) s+=level_0(i); sink(s); return 0; }}\n"

    elif variant == "recursive_descent":
        # Mimics a recursive descent parser (common real-world pattern)
        code += "int pos; char input[256];\n"
        code += "int parse_number() { int n=0; while(input[pos]>='0'&&input[pos]<='9'){n=n*10+(input[pos]-'0');pos++;} return n; }\n"
        code += "int parse_factor();\n"
        code += "int parse_expr();\n"
        code += "int parse_term() { int left=parse_factor(); while(input[pos]=='*'){pos++;left*=parse_factor();} return left; }\n"
        code += "int parse_expr() { int left=parse_term(); while(input[pos]=='+'){pos++;left+=parse_term();} return left; }\n"
        code += "int parse_factor() { if(input[pos]=='('){pos++;int r=parse_expr();pos++;return r;} return parse_number(); }\n"
        code += 'int main() { char *s="3+4*2+1"; for(int i=0;s[i];i++)input[i]=s[i]; pos=0; sink(parse_expr()); return 0; }\n'

    else:  # state_machine_funcs
        # Each state is a function calling the next state
        n_states = depth + 1
        for s in range(n_states):
            next_s = (s + 1) % n_states
            code += f"int state_{s}(int val, int steps);\n"
        for s in range(n_states):
            next_s = (s + 1) % n_states
            alt_s = (s + 2) % n_states
            code += f"int state_{s}(int val, int steps) {{\n"
            code += f"  if(steps<=0) return val;\n"
            code += f"  val = val * {random.randint(2,5)} + {random.randint(1,10)};\n"
            code += f"  if(val%{random.randint(2,5)}==0) return state_{alt_s}(val, steps-1);\n"
            code += f"  return state_{next_s}(val, steps-1);\n}}\n"
        code += f"int main() {{ sink(state_0(1, {random.randint(50,200)})); return 0; }}\n"

    return code


def gen_library_heavy(seed):
    """Programs that call stdlib/math functions.
    Exercises: handling opaque library boundaries, not inlining across them."""
    random.seed(seed)
    code = '#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <math.h>\n\n'
    code += sink() + fsink()
    variant = random.choice(["malloc_array", "math_compute", "memcpy_heavy",
                             "qsort_stdlib", "string_processing", "mixed_alloc"])

    if variant == "malloc_array":
        n = random.randint(64, 256)
        code += f"int main() {{\n"
        code += f"  int *arr = (int*)malloc({n} * sizeof(int));\n"
        code += f"  if(!arr) return 1;\n"
        code += f"  for(int i=0;i<{n};i++) arr[i] = i * i;\n"
        code += f"  int s=0; for(int i=0;i<{n};i++) s+=arr[i];\n"
        code += f"  free(arr);\n"
        code += f"  sink(s);\n  return 0;\n}}\n"

    elif variant == "math_compute":
        n = random.randint(100, 500)
        code += f"int main() {{\n"
        code += f"  double s = 0.0;\n"
        code += f"  for(int i=1;i<{n};i++) {{\n"
        code += f"    s += sqrt((double)i) * log((double)i + 1.0);\n"
        code += f"    s += sin((double)i * 0.01) * cos((double)i * 0.02);\n"
        code += f"    s += pow((double)i, 0.5) + fabs(s - (double)(i*i));\n"
        code += f"  }}\n"
        code += f"  fsink(s);\n  return 0;\n}}\n"

    elif variant == "memcpy_heavy":
        n = random.randint(64, 256)
        code += f"#define N {n}\nint src[N], dst[N], buf[N];\n\n"
        code += f"int main() {{\n"
        code += f"  for(int i=0;i<N;i++) src[i]=i;\n"
        code += f"  memcpy(dst, src, N*sizeof(int));\n"
        code += f"  for(int i=0;i<N;i++) dst[i] *= 2;\n"
        code += f"  memmove(buf, dst+N/4, (N/2)*sizeof(int));\n"
        code += f"  memset(dst, 0, (N/4)*sizeof(int));\n"
        code += f"  int s=0; for(int i=0;i<N;i++) s+=dst[i]+buf[i%N];\n"
        code += f"  sink(s);\n  return 0;\n}}\n"

    elif variant == "qsort_stdlib":
        n = random.randint(64, 256)
        code += f"int arr[{n}];\n\n"
        code += f"int cmp(const void *a, const void *b) {{ return *(const int*)a - *(const int*)b; }}\n\n"
        code += f"int main() {{\n"
        code += f"  for(int i=0;i<{n};i++) arr[i]=({n}-i)*{random.randint(2,7)};\n"
        code += f"  qsort(arr, {n}, sizeof(int), cmp);\n"
        code += f"  sink(arr[0]+arr[{n-1}]);\n  return 0;\n}}\n"

    elif variant == "string_processing":
        code += "char buf[512];\n\n"
        code += "int main() {\n"
        code += '  strcpy(buf, "The quick brown fox jumps over the lazy dog");\n'
        code += "  int len = strlen(buf);\n"
        code += "  char *tok = strtok(buf, \" \");\n"
        code += "  int word_count = 0;\n"
        code += "  while(tok) { word_count++; tok = strtok(NULL, \" \"); }\n"
        code += "  char out[512]; memset(out, 0, sizeof(out));\n"
        code += "  sprintf(out, \"%d words, %d chars\", word_count, len);\n"
        code += "  sink(word_count * 1000 + len);\n  return 0;\n}\n"

    else:  # mixed_alloc
        n = random.randint(32, 128)
        code += "typedef struct { double x; double y; } Point;\n\n"
        code += f"int main() {{\n"
        code += f"  Point *pts = (Point*)calloc({n}, sizeof(Point));\n"
        code += f"  if(!pts) return 1;\n"
        code += f"  for(int i=0;i<{n};i++) {{ pts[i].x = sin(i*0.1); pts[i].y = cos(i*0.1); }}\n"
        code += f"  double total = 0;\n"
        code += f"  for(int i=0;i<{n}-1;i++) {{\n"
        code += f"    double dx = pts[i+1].x - pts[i].x;\n"
        code += f"    double dy = pts[i+1].y - pts[i].y;\n"
        code += f"    total += sqrt(dx*dx + dy*dy);\n"
        code += f"  }}\n"
        code += f"  free(pts);\n"
        code += f"  fsink(total);\n  return 0;\n}}\n"

    return code


def gen_scaled_composite(seed):
    """Compose 2-3 kernels from different categories into one larger program.
    Produces programs with 200-500+ IR instructions."""
    random.seed(seed)
    code = header() + sink() + fsink()
    n = random.randint(128, 512)
    code += f"#define N {n}\n"
    code += "int A[N], B[N], C[N];\n"
    code += "double fA[N], fB[N], fC[N];\n\n"

    # Helper functions (inter-procedural)
    code += "void init_int(int *arr, int len, int seed) { for(int i=0;i<len;i++) arr[i]=(i*seed+7)%1000; }\n"
    code += "void init_double(double *arr, int len, double base) { for(int i=0;i<len;i++) arr[i]=base+i*0.01; }\n"
    code += "int reduce_int(int *arr, int len) { int s=0; for(int i=0;i<len;i++) s+=arr[i]; return s; }\n"
    code += "double reduce_double(double *arr, int len) { double s=0; for(int i=0;i<len;i++) s+=arr[i]; return s; }\n\n"

    # Pick 2-3 kernels to compose
    num_kernels = random.randint(2, 3)
    kernel_pool = [
        # kernel, code
        ("matmul_flat", 
         "  /* Flat matmul */\n  int M=N/8>0?N/8:4;\n  for(int i=0;i<M;i++) for(int j=0;j<M;j++) { int s=0; for(int k=0;k<M;k++) s+=A[i*M+k]*B[k*M+j]; C[i*M+j]=s; }\n"),
        ("stencil_1d",
         "  /* 1D stencil */\n  for(int t=0;t<10;t++) { for(int i=1;i<N-1;i++) fC[i]=0.25*fA[i-1]+0.5*fA[i]+0.25*fA[i+1]; for(int i=0;i<N;i++) fA[i]=fC[i]; }\n"),
        ("saxpy",
         "  /* SAXPY */\n  for(int i=0;i<N;i++) fC[i] = 2.5*fA[i] + fB[i];\n"),
        ("branchy_filter",
         "  /* Branchy filter */\n  int valid=0; for(int i=0;i<N;i++) { if(A[i]%3==0 && A[i]>100) { C[valid++]=A[i]; } else if(A[i]%7==0) { C[valid++]=A[i]*2; } }\n"),
        ("histogram",
         "  /* Histogram */\n  int bins[64]={0}; for(int i=0;i<N;i++) bins[A[i]%64]++; for(int i=0;i<64;i++) C[i]=bins[i];\n"),
        ("prefix_sum",
         "  /* Prefix sum */\n  C[0]=A[0]; for(int i=1;i<N;i++) C[i]=C[i-1]+A[i];\n"),
        ("sort_bubble",
         "  /* Bubble sort (small) */\n  int sN=N>64?64:N; for(int i=0;i<sN-1;i++) for(int j=i+1;j<sN;j++) if(A[i]>A[j]){int t=A[i];A[i]=A[j];A[j]=t;}\n"),
    ]

    chosen = random.sample(kernel_pool, num_kernels)

    code += "int main() {\n"
    code += "  init_int(A, N, 3); init_int(B, N, 7);\n"
    code += "  init_double(fA, N, 1.0); init_double(fB, N, 2.0);\n\n"

    for name, kernel_code in chosen:
        code += kernel_code + "\n"

    code += "  int ri = reduce_int(C, N);\n"
    code += "  double rd = reduce_double(fC, N);\n"
    code += "  sink(ri); fsink(rd);\n"
    code += "  return 0;\n}\n"

    return code


GENERATORS = {
    "dense_linalg": gen_dense_linalg,
    "sparse_access": gen_sparse_access,
    "recursive": gen_recursive,
    "control_flow": gen_control_flow,
    "struct_heavy": gen_struct_heavy,
    "pointer_chase": gen_pointer_chase,
    "bitwise": gen_bitwise,
    "simd_friendly": gen_simd_friendly,
    "stencil": gen_stencil,
    "graph_algo": gen_graph_algo,
    "string_ops": gen_string_ops,
    "mixed_arith": gen_mixed_arithmetic,
    # --- NEW v5 categories ---
    "multi_func": gen_multi_func,
    "deep_call_chain": gen_deep_call_chain,
    "library_heavy": gen_library_heavy,
    "scaled_composite": gen_scaled_composite,
}


def main():
    parser = argparse.ArgumentParser(description="Generate diverse synthetic C benchmarks.")
    parser.add_argument("--count", type=int, default=NUM_PER_CATEGORY,
                        help="Number of benchmarks per category.")
    parser.add_argument("--output_dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--verify", action="store_true",
                        help="Verify each file compiles with clang.")
    parser.add_argument("--only-new", action="store_true",
                        help="Only generate the new v5 categories (multi_func, deep_call_chain, library_heavy, scaled_composite).")
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    failed = 0

    NEW_CATEGORIES = {"multi_func", "deep_call_chain", "library_heavy", "scaled_composite"}
    generators = GENERATORS
    if args.only_new:
        generators = {k: v for k, v in GENERATORS.items() if k in NEW_CATEGORIES}
        print(f"[GEN] --only-new: generating {len(generators)} new categories only")

    for cat_name, gen_fn in generators.items():
        cat_dir = output_dir / cat_name
        cat_dir.mkdir(exist_ok=True)
        print(f"[GEN] Category: {cat_name} ({args.count} programs)...")

        for i in range(args.count):
            filename = f"{cat_name}_{i:04d}.c"
            filepath = cat_dir / filename
            try:
                code = gen_fn(seed=i + hash(cat_name) % 100000)
                with open(filepath, "w") as f:
                    f.write(code)
                total += 1

                if args.verify and total % 50 == 0:
                    import subprocess
                    r = subprocess.run(
                        ["clang", "-S", "-emit-llvm", str(filepath), "-o", "/dev/null", "-Wno-everything"],
                        capture_output=True, timeout=5
                    )
                    status = "OK" if r.returncode == 0 else "FAIL"
                    if r.returncode != 0:
                        failed += 1
                    print(f"  [{status}] {filename}")

            except Exception as e:
                print(f"  [ERROR] {filename}: {e}")
                failed += 1

    print(f"\n[DONE] Generated {total} programs across {len(GENERATORS)} categories in {output_dir}")
    if args.verify:
        print(f"[VERIFY] {failed} compilation failures detected")


if __name__ == "__main__":
    main()
