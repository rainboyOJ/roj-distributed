#include <bits/stdc++.h>
#define pii std::pair<int, int>
#define fi first
#define se second
#define pb push_back
typedef long long i64;
const i64 iinf = 0x3f3f3f3f, linf = 0x3f3f3f3f3f3f3f3f;
const int N = 1e5 + 10;
i64 n, q, rt, mx;
std::vector<int> e[N];
i64 m[N], w[N], dep[N], g[N], h[N];
i64 f[N][4];
void dfs(int u, int fa) {
dep[u] = dep[fa] + 1;
mx = std::max(mx, dep[u]);
g[dep[u]] += w[u];
i64 sum = 0;
if (e[u].size() == 1 && u != rt) {
f[u][2] = w[u];
f[u][3] = m[u];
h[dep[u]] += f[u][2];
//
std::cout << fa << " " << u << " " << std::max(f[u][0], f[u][0]) << "\n";
return;
}
for (auto v : e[u]) {
if (v == fa)
continue;
dfs(v, u);
f[u][0] += f[v][2];
sum += std::max({f[v][0], f[v][1], f[v][3]});
}
for (auto v : e[u]) {
if (v == fa)
continue;
f[u][1] = std::max(f[u][1], f[v][0] + (sum - std::max({f[v][0], f[v][1], f[v][3]})));
}
sum = 0;
for (auto v : e[u]) {
if (v == fa)
continue;
sum += std::max(f[v][1], f[v][3]);
}
f[u][1] += w[u];
f[u][3] = m[u] + sum;

f[u][2] = std::max({f[u][0], f[u][1], f[u][3] - m[u] + w[u]});
// std::cout << fa << " " << u << " " << std::max(f[u][0], f[u][0]) << "\n";
h[dep[u]] += f[u][2];
}
void Solve() {
std::cin >> n >> q;
for (int i = 1; i <= n; i++)
std::cin >> m[i];
for (int i = 1; i <= n; i++)
std::cin >> w[i], w[i] = std::max(w[i], m[i]);
std::cin >> rt;
for (int i = 1; i < n; i++) {
int u, v;
std::cin >> u >> v;
e[u].pb(v), e[v].pb(u);
}
dfs(rt, 0);
for (int i = 1; i <= n; i++)
g[i] += g[i - 1];
while (q--) {
i64 L;
std::cin >> L;
L = std::min(mx - 1, L);
std::cout << g[L] + h[L + 1] << "\n";
}
}
int main() {
freopen("tree.in", "r", stdin);
freopen("tree.out", "w", stdout);
std::ios::sync_with_stdio(false);
std::cin.tie(nullptr);
Solve();
return 0;
}


