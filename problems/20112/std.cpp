#include <bits/stdc++.h>
#define I using
#define love namespace
#define Elaina std
#define ll long long
I love Elaina;
const int N = 20;
const ll mod = 998244353;
const ll inv2 = 499122177;
ll read() {
ll x = 0, f = 1;
char ch = getchar();
while (ch < '0' || ch > '9') {
if (ch == '-')
f = -1;
ch = getchar();
}
while (ch >= '0' && ch <= '9') {
x = (x << 3) + (x << 1) + ch - '0';
ch = getchar();
}
return x * f;
}
ll n, m, c, a[N], x, y, to[1 << 15], p2[60], ip2[60], g[1 << 15], cnt[1 << 15], minp[1 << 15], lg[1 << 15],
popcnt[1 << 15], ans;
unordered_map<int, ll>f[1 << 15];
vector<ll>qwq;
int lowbit(int x) {
return x & (-x);
}
ll calc() {
ll res = 0, F[2][2], cur = 0, cnt, t0;
for (ll i = 59; i >= 0; i--) {
F[cur][0] = t0 = 1, F[cur][1] = cnt = 0;
for (ll tmp : qwq) {
cur ^= 1;
if (tmp & (1ll << i)) {
cnt++;
F[cur][0] = (1ll * p2[i] * F[cur ^ 1][1] % mod + 1ll * ((tmp & ((1ll << i) - 1)) + 1) % mod * F[cur ^ 1][0] %
mod) % mod;
F[cur][1] = (1ll * p2[i] * F[cur ^ 1][0] % mod + 1ll * ((tmp & ((1ll << i) - 1)) + 1) % mod * F[cur ^ 1][1] %
mod) % mod;
} else
F[cur][0] = 1ll * ((tmp & ((1ll << i) - 1)) + 1) % mod * F[cur ^ 1][0] % mod,
F[cur][1] = 1ll * ((tmp & ((1ll << i) - 1)) + 1) % mod * F[cur ^ 1][1] % mod;
t0 = 1ll * ((tmp & ((1ll << i) - 1)) + 1) % mod * t0 % mod;
}
F[cur][0] = (F[cur][0] - t0 + mod) % mod;
if (cnt)
res = (res + 1ll * ip2[i] * F[cur][(cnt & 1) ^ ((bool)(c & (1ll << i)))] % mod) % mod;
if ((cnt & 1) != (bool)(c & (1ll << i)))
break;
if (!i)

res = (res + 1) % mod;
}
return res;
}
int main() {
p2[0] = ip2[0] = 1, lg[0] = -1;
for (int i = 1; i < (1 << 15); i++)
lg[i] = lg[i >> 1] + 1, popcnt[i] = popcnt[i >> 1] + (i & 1);
for (int i = 1; i < 60; i++)
p2[i] = 2ll * p2[i - 1] % mod, ip2[i] = 1ll * inv2 * ip2[i - 1] % mod;
n = read(), m = read(), c = read();
for (int i = 0; i < n; i++)
a[i] = read();
for (int i = 1; i <= m; i++) {
x = read() - 1, y = read() - 1;
to[x] |= (1 << y), to[y] |= (1 << x);
}
for (int sta = 1; sta < (1 << n); sta++)
for (int i = 0; i < n; i++)
if (sta & (1 << i))
cnt[sta] += popcnt[sta & to[i]];
for (int sta = 1; sta < (1 << n); sta++) {
int S = sta ^ lowbit(sta);
if (!cnt[S])
g[sta] = (g[sta] - g[sta ^ S] + mod) % mod;
for (int T = (S - 1)&S; T; T = (T - 1)&S)
if (!cnt[S ^ T])
g[sta] = (g[sta] - g[T | (sta ^ S)] + mod) % mod;
g[sta] = (g[sta] + (!cnt[sta])) % mod;
}
for (int sta = 0; sta < (1 << n); sta++) {
if (sta == lowbit(sta))
minp[sta] = lg[sta];
else
minp[sta] = (a[minp[sta ^ lowbit(sta)]] < a[lg[lowbit(sta)]]) ? minp[sta ^ lowbit(sta)] : lg[lowbit(sta)];
}
f[0][0] = 1;
for (int sta = (1 << n) - 1; sta; sta--) {
for (pair<int, ll>tmp : f[((1 << n) - 1)^sta]) {
int S = sta ^ lowbit(sta);
f[((1 << n) - 1)^S][tmp.first | (sta ^ S)] = (f[((1 << n) - 1)^S][tmp.first |
(sta ^ S)] + 1ll * tmp.second * g[sta ^ S] % mod) % mod;
for (int T = S; T; T = (T - 1)&S) {
int nT = T | (sta ^ S), nS = (((1 << n) - 1)^sta) | nT;
f[nS][tmp.first | ((popcnt[nT] & 1) * (1 << minp[nT]))] = (f[nS][tmp.first | ((popcnt[nT] & 1) *
(1 << minp[nT]))] + 1ll * ((popcnt[T] & 1) * a[minp[nT]] + 1) % mod * tmp.second % mod * g[nT] % mod) % mod;
}
}
}
for (pair<int, ll>tmp : f[(1 << n) - 1]) {

qwq.clear();
for (int i = 0; i < n; i++)
if (tmp.first & (1 << i))
qwq.push_back(a[i]);
ans = (ans + 1ll * tmp.second * calc() % mod) % mod;
}
printf("%lld", ans);
return 0;
}


