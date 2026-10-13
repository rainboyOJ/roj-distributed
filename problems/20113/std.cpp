#include <bits/stdc++.h>
using namespace std;
using ll = long long;
#define int ll
const int maxn = 1e6 + 10, lm = 20;
struct {
int nxt, v;
} edge[maxn << 1];
int head[maxn], ec;
void add(int u, int v) {
edge[++ec] = {head[u], v};
head[u] = ec;
}
int n, Q, V[maxn];
int son[maxn], dfn[maxn], dfc;
int dfs1(int u) {
int len = 0;
for (int i = head[u]; i; i = edge[i].nxt) {
int v = edge[i].v, vl = dfs1(v);
if (vl > len)
len = vl, son[u] = v;
}
return len + 1;
}
int c1[maxn][lm], c0[maxn][lm];
ll f[maxn][lm], othbit[maxn];
struct QRY {
int id, k;
};
vector<QRY>q[maxn];
ll ans[maxn];
int dfs2(int u) {
int buf = dfn[u] = ++dfc, pr = 0, res = dfc;
if (son[u])
pr = dfc + 1, res = dfs2(son[u]);
for (int i = head[u]; i; i = edge[i].nxt) {
int v = edge[i].v;
if (v != son[u]) {
int cur = dfc, las = dfs2(v);
for (int j = cur + 1; j <= las; ++j) {
for (int k = 0; k < lm; ++k)
c1[buf + j - cur][k] += c1[ j][k],
c0[buf + j - cur][k] += c0[ j][k],
f[buf + j - cur][k] += f[ j][k];

othbit[buf + j - cur] += othbit[ j];
}
}
}
for (int i = 0; i < lm; ++i)
c1[buf][i] = c1[pr][i] + (V[u] >> i & 1),
c0[buf][i] = c0[pr][i] + (~V[u] >> i & 1);
othbit[buf] = othbit[pr] + ((V[u] >> lm) << lm);
for (int i = 0; i < lm; ++i) {
int ed = buf + (1 << i) > res ? 0 : buf + (1 << i);
int pred = buf + (1 << (i - 1)) > res ? 0 : buf + (1 << (i - 1));
f[buf][i] = ((c1[buf][i] - c1[ed][i]) << i)
+ (i ? f[buf][i - 1] + f[pred][i - 1]
+ (ll(c0[pred][i - 1] - c0[ed][i - 1]
- c1[pred][i - 1] + c1[ed][i - 1]) << (i - 1))
: 0);
}
for (auto[id, k] : q[u]) {
int va = 0, cur = buf;
k = min(k, res - buf) + 1;
int ed = (buf + k - 1 == res ? 0 : buf + k);
for (int i = lm - 1; ~i; --i)
if (k >> i & 1) {
va += f[cur][i];
cur += 1 << i;
va += ll(c0[cur == res + 1 ? 0 : cur][i] - c0[ed][i]) << i;
} else
va += ll(c1[cur == res + 1 ? 0 : cur][i] - c1[ed][i]) << i;
ans[id] = va + othbit[buf] - othbit[ed];
}
return res;
}
signed main() {
ios::sync_with_stdio(0), cin.tie(0);
cin >> n;
for (int i = 1; i <= n; ++i)
cin >> V[i];
for (int i = 2, f; i <= n; ++i)
cin >> f, add(f, i);
cin >> Q;
for (int i = 1, x, k; i <= Q; ++i)
cin >> x >> k, q[x].push_back({i, k});
dfs1(1), dfs2(1);

for (int i = 1; i <= Q; ++i)
cout << ans[i] << '\n';
}


