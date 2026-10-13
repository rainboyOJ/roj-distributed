#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 2005, P = 998244353, Hs = 7193, Ph = 1e9 + 9;
char buf[1 << 23], *p1 = buf, *p2 = buf;
#define getchar() (p1==p2&&(p2=(p1=buf)+fread(buf,1,1<<23,stdin),p1==p2)?EOF:*p1++)
template<class rd>
void read(rd &x) {
char c = getchar();
for (; c < 48 || c > 57; c = getchar());
for (x = 0; c > 47 && c < 58; c = getchar())
x = (x << 1) + (x << 3) + (c ^ 48);
}
int tid, n, m, e[N][N], sz[N], ans = 1, p[N], cp, va[N], rv[N];
int fac[N], inv[N], ifac[N], g[N], w[N], pw[N];
bool vis[N], vp[N];
ll k;
int ksm(int x, ll y) {
int res = 1;
for (; y; y >>= 1, x = 1ll * x * x % P)
if (y & 1)
res = 1ll * res * x % P;
return res;
}
inline void Add(int &x, int y) {
if ((x += y) >= P)
x -= P;
}
int C(int n, int m) {
return 1ll * fac[n] * ifac[m] % P * ifac[n - m] % P;
}
int qC(ll n, int m, int q) {
int res = 1;
for (int i = 1, p = 1; i <= m; ++i)
p = 1ll * p * q % P, res = 1ll * res * (P + 1 - p) % P;
res = ksm(res, P - 2);
for (int i = 1, p = ksm(q, n - m); i <= m; ++i)
p = 1ll * p * q % P, res = 1ll * res * (P + 1 - p) % P;
return res;
}
void init() {
fac[0] = fac[1] = ifac[0] = ifac[1] = inv[0] = inv[1] = 1;
for (int i = 2; i <= n; ++i)
fac[i] = 1ll * fac[i - 1] * i % P, inv[i] = 1ll * (P - P / i) * inv[P % i] % P,
ifac[i] = 1ll * ifac[i - 1] * inv[i] % P;

for (int i = 1; i <= n; ++i) {
int x = i, y = 1;
for (int j = 2, ct; j * j <= x; ++j)
if (x % j == 0) {
ct = 1, x /= j;
while (x % j == 0)
x /= j, ++ct;
y = 1ll * y * qC(ct + k - 1, ct, inv[ j]) % P;
}
if (x > 1)
y = 1ll * y * qC(k, 1, inv[x]) % P;
w[i] = 1ll * y * ksm(i, k - 1) % P * fac[i - 1] % P;
}
}
void dfs(int x) {
vp[x] = true, p[++cp] = x, rv[x] = cp;
for (int i = 1; i <= m; ++i)
if (!vp[e[x][i]])
dfs(e[x][i]);
}
void gtv(int x) {
cp = 0, dfs(x), sz[x] = cp;
for (int i = 1; i <= cp; ++i)
for (int j = 1; j <= m; ++j)
va[x] = (1ll * Hs * va[x] + rv[e[p[i]][ j]]) % Ph;
}
int calc(int s, int c) {
g[0] = pw[0] = 1;
int v = ksm(s, k - 1);
for (int i = 1; i <= c; ++i)
pw[i] = 1ll * pw[i - 1] * s % P, g[i] = 0;
for (int i = 1; i <= c; ++i)
pw[i] = 1ll * w[i] % P * v % P * pw[i] % P;
for (int i = 1; i <= c; ++i)
for (int j = 1; j <= i; ++j)
Add(g[i], 1ll * g[i - j]*pw[ j] % P * C(i - 1, j - 1) % P);
return g[c];
}
int main() {
freopen("wormhole.in", "r", stdin);
freopen("wormhole.out", "w", stdout);
read(tid), read(n), read(m), read(k);
init();

for (int i = 1, u, v, w; i <= n * m; ++i) {
read(u), read(v), read(w);
e[u][w] = v;
}
for (int i = 1; i <= n; ++i)
if (!vp[i])
gtv(i);
for (int i = 1; i <= n; ++i)
if (sz[i] && !vis[i]) {
vis[i] = true;
int ct = 1;
for (int j = i + 1; j <= n; ++j)
if (sz[ j] && !vis[ j] && sz[ j] == sz[i] && va[ j] == va[i]) {
vis[ j] = true;
++ct;
}
ans = 1ll * ans * calc(sz[i], ct) % P;
}
printf("%d\n", ans);
return 0;
}


