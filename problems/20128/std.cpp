#include <iostream>
#include <vector>
#define pb push_back
const int p = 998244353;
int n, fl, k, rs, a[3050], f[3050], ct[3050];
std::vector <int> e[3050], o[3050];
namespace IO {
char buf[400000], *it = buf;
void rd(int &x) {
for (x = 0; !isdigit(*it);)
++it;
for (; isdigit(*it);)
x = x * 10 + *it++ -'0';
}
} using IO::rd;
inline void gm(int &x, int y) {
x += y;
x > p ? x -= p : 0;
}
inline void gr(std::vector<int> &vc, int x, int fa, int d) {
gm(vc[d], f[x]);
for (auto v : e[x])
if (v != fa && a[v] == a[x])
gr(vc, v, x, d + 1);
}
inline void dp(std::vector<int> &vc, int x, int fa, int k, int d) {
f[x] = 1ll * f[x] * (vc[d] + vc[d + (a[x] < k ? -1 : 1)]) % p;
for (auto v : e[x])
if (v != fa && a[v] == a[x])
dp(vc, v, x, k, d + 1);
}
inline void dfs(int x, int fa) {
ct[a[x]] += a[x] != a[fa];
if (ct[a[x]] >= 2)
return void(fl = 1);
for (auto v : e[x])
if (v != fa) {
dfs(v, x);
if (a[v] != a[x]) {
std::vector<int>vc(n + 5);
gr(vc, v, x, 1);
dp(vc, x, v, a[v], 1);
}
}
}
int main() {
fread(IO::buf, 1, 380000, stdin);
int T;

rd(T);
while (T--) {
rd(n), rd(k);
rs = fl = 0;
for (int i = 1; i <= n; i++)
e[i].clear(), o[i].clear(), ct[i] = 0;
for (int i = 1, x, y; i < n; i++)
rd(x), rd(y), e[x].pb(y), e[y].pb(x);
for (int i = 1; i <= n; i++)
rd(a[i]), o[a[i]].pb(i);
for (int i = 1; i <= n; i++)
f[i] = 1;
dfs(1, 0);
for (int i = 1; i <= k; i++)
if (!ct[i]) {
fl = 1;
break;
}
if (fl) {
puts("0\n");
continue;
}
for (auto v : o[a[1]])
gm(rs, f[v]);
printf("%d\n", rs);
}
}


