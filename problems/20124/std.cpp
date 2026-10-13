#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N = 3005, MOD = 998244353;
int n, m, sz[N], leaf[N], f[N], g[N];
int c[N][N], p2[N], b2[N], ans;
vector<int>e[N];
void Init(int n) {
for (int i = 0 ; i <= n ; i++) {
c[i][0] = 1;
for (int j = 1 ; j <= i ; j++)
c[i][ j] = (c[i - 1][ j] + c[i - 1][ j - 1]) % MOD;
}
p2[0] = b2[0] = 1;
for (int i = 1 ; i <= n ; i++)
p2[i] = p2[i - 1] * 2 % MOD;
for (int i = 1 ; i <= n ; i++)
b2[i] = (ll)b2[i - 1] * p2[n] % MOD;
}
int Qpow(int x, int p) {
if (x == 2)
return (ll)p2[p % n] * b2[p / n] % MOD;
int res = 1;
for (; p ; p >>= 1, x = (ll)x * x % MOD)
if (p & 1)
res = (ll)res * x % MOD;
return res;
}
void Dfs(int u, int fa) {
sz[u] = 1, leaf[u] = e[u].size() == 1u;
if (leaf[u])
return ;
for (int v : e[u])
if (v != fa)
Dfs(v, u);
f[0] = 1;
auto add = [&](int &x, const ll & y) {
x = (x + y) % MOD;
};
for (int v : e[u]) {
if (v == fa)
continue ;

memset(g, 0, sizeof g);
for (int i = 0 ; i <= leaf[u] ; i++)
for (int j = 0 ; j <= leaf[v] ; j++)
add(g[i + j], (ll)f[i] * c[leaf[v]][ j] % MOD * Qpow(2, (sz[v] - 1) * sz[v] / 2 + (sz[v] - j) * (sz[u] - i)));
memcpy(f, g, sizeof g);
leaf[u] += leaf[v], sz[u] += sz[v];
}
int s = n - sz[u], t = m - leaf[u];
for (int i = 0 ; i <= leaf[u] ; i++)
add(ans, ll(i & 1 ? MOD - 1 : 1) * f[i] % MOD * Qpow(Qpow(2, sz[u] - i) - 1, t) % MOD
* Qpow(2, s * (s - 1) / 2 + (s - t) * (sz[u] - i)));
if (!fa)
return ;
for (int i = 0 ; i <= leaf[u] ; i++)
add(ans, ll(i & 1 ? 1 : MOD - 1) * c[leaf[u]][i] % MOD * Qpow(Qpow(2, sz[u] - i) - 1, t) % MOD
* Qpow(2, sz[u] * (sz[u] - 1) / 2 + s * (s - 1) / 2 + (s - t) * (sz[u] - i)));
}
int main() {
ios::sync_with_stdio(0);
cin.tie(0), cout.tie(0);
cin >> n;
Init(n);
for (int i = 1 ; i < n ; i++) {
int u, v;
cin >> u >> v;
e[u].push_back(v);
e[v].push_back(u);
}
if (n == 2)
return cout << "1\n", 0;
for (int i = 1 ; i <= n ; i++)
if (e[i].size() == 1u)
m++;
for (int i = 1 ; i <= n ; i++)
if (e[i].size() != 1u) {
Dfs(i, 0);
break ;
}
cout << ans << "\n";
return 0;
}


