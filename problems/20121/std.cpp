#include <bits/stdc++.h>
using namespace std;
inline char gc() {
static char buf[100000], *p1 = buf, *p2 = buf;
return p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, 100000, stdin), p1 == p2) ? EOF : *p1++;
}
inline int read() {
int res, f = 1;
char c;
while ((c = gc()) < '0' || c > '9')
if (c == '-')
f = -1;
res = c - '0';
while ((c = gc()) >= '0' && c <= '9')
res = res * 10 + c - '0';
return res * f;
}
const int N = 11, M = (1 << N) + 5;
int n, m, d[2][M][M];
int main() {
n = read(), m = (1 << n) - 1;
for (int i = 0; i <= m; i++)
for (int j = 0; j <= m; j++)
d[0][i][ j] = read();
int f = 1;
for (int i = 1 << (n - 2); i; i >>= 1, f ^= 1) {
for (int x = 0; x <= m; x++)
for (int y = 0; y <= m; y++)
d[f][x][y] = d[f ^ 1][x][y];
for (int x = 0; x <= m; x++)
for (int y = 0; y <= m; y++) {
int t = d[f ^ 1][x][y];
d[f][(x + m + 1 - i)&m][y] ^= t;
d[f][(x + i)&m][y] ^= t;
d[f][x][(y + m + 1 - i)&m] ^= t;
d[f][x][(y + i)&m] ^= t;
}
}
f ^= 1;
int cnt = 0;
for (int i = 0; i <= m; i++)
for (int j = 0; j <= m; j++)
if (d[f][i][ j])
cnt++;

printf("%d\n", cnt);
for (int i = 0; i <= m; i++)
for (int j = 0; j <= m; j++)
if (d[f][i][ j])
printf("%d %d\n", i, j);
return 0;
}


