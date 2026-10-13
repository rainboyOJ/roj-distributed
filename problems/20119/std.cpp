#include <bits/stdc++.h>
using namespace std;
const int N = 505;
int n, m, g[N][N], h[N][N], id[N][N];
int klee[N], rlink[N], vis[N];
int pre[N][2], q[N * 2], hh, tt;
inline bool Find(int u) {
for (int v = 1; v <= n; v ++)
if (g[u][v] != -1 && !vis[v]) {
vis[v] = 1;
if (!klee[v] || Find(klee[v])) {
klee[v] = u;
return 1;
}
}
return 0;
}
inline bool BFS(int s) {
pre[s][0] = -1, q[hh = tt = 0] = s << 1;
while (hh <= tt) {
int u = q[hh] >> 1, t = q[hh] & 1;
hh ++ ;
if (u == s && t) {
for (int i = 1; i <= n; i ++)
vis[i] = 0;
for (int x = pre[u][t], u = x >> 1, t = x & 1; u != s || t != 0; x = pre[u][t], u = x >> 1, t = x & 1) {
if (vis[u])
return 0;
vis[u] = 1;
}
return 1;
}
for (int v = 1; v <= n; v ++) {
int s = t ^ h[u][v];
if (!pre[v][s] && h[u][v] != -1) {
pre[v][s] = u << 1 | t;
q[ ++ tt] = v << 1 | s;
}
}
}

return 0;
}
int p[N];
mt19937 mrand(time(0));
int main() {
int T;
scanf("%d", &T);
while (T --) {
scanf("%d%d", &n, &m);
for (int i = 1; i <= n; i ++)
for (int j = 1; j <= n; j ++)
g[i][ j] = h[i][ j] = id[i][ j] = -1;
for (int i = 1; i <= n; i ++)
klee[i] = 0;
for (int i = 1; i <= m; i ++) {
int u, v, w;
scanf("%d%d%d", &u, &v, &w);
g[u][v - n] = w, id[u][v - n] = i;
}
bool flag = 0;
for (int i = 1; i <= n; i ++) {
for (int j = 1; j <= n; j ++)
vis[ j] = 0;
if (!Find(i)) {
flag = 1;
break ;
}
}
if (flag) {
puts("-1");
continue ;
}
// for(int i = 1; i <= n; i ++ ) printf("%d ", klee[i]);
// puts("");
int w = 0;
for (int i = 1; i <= n; i ++)
w ^= g[klee[i]][i];
if (w) {
flag = 1;
for (int i = 1; i <= n; i ++)
rlink[klee[i]] = i;

for (int i = 1; i <= n; i ++)
for (int j = 1; j <= n; j ++)
if (g[i][ j] != -1)
h[i][klee[ j]] = g[i][ j] ^ g[klee[ j]][ j];
for (int i = 1; i <= n; i ++)
p[i] = i;
shuffle(p + 1, p + n + 1, mrand);
for (int T = 1; T <= min(n, 300); T ++) {
int i = p[T];
if (BFS(i)) {
for (int u = i, s = 1, v, t; u != i || s != 0; u = v, s = t) {
v = pre[u][s] >> 1, t = pre[u][s] & 1;
klee[rlink[u]] = v;
}
flag = 0;
break ;
}
for (int i = 1; i <= n; i ++)
pre[i][0] = pre[i][1] = 0;
}
}
if (flag) {
puts("-1");
continue ;
}
for (int i = 1; i <= n; i ++)
printf("%d ", id[klee[i]][i]);
puts("");
}
return 0;
}


