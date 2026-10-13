#include <iostream>
#include <cmath>
#include <vector>
#define poly vector<int>
#define int long long
using namespace std;
const int N = 15, mod = 1e9 + 7;
int n, m, k, fac[1 << N], ifac[1 << N], in[1 << N], tot;
int h[1 << N], g[1 << N][N + 1];
inline int C(int n, int m) {
return n < m || m < 0 ? 0 : fac[n] * ifac[m] % mod * ifac[n - m] % mod;
}
inline int adc(int x, int v) {
return x + v >= mod ? x + v - mod : x + v;
}
inline void add(int &x, int v) {
x = adc(x, v);
}
inline bool check(int A, int B) {
return !(in[A] & B);
}
inline int sig(int x) {
return x & 1 ? mod - 1 : 1;
}
inline int Qpow(int a, int b) {
int ans = 1;
for (a %= mod; b; b >>= 1, a = a * a % mod)
if (b & 1)
ans = ans * a % mod;
return ans;
}
inline int Inv(int x) {
return Qpow(x, mod - 2);
}
namespace Lagrange {
inline poly operator +(poly a, poly b) {
poly c(max((int)a.size(), (int)b.size()));
for (int i = 0; i < (int)c.size(); i++) {
if ((int)a.size() > i)
add(c[i], a[i]);
if ((int)b.size() > i)
add(c[i], b[i]);
}
return c;
}
inline poly operator *(poly a, poly b) {
poly c((int)a.size() + (int)b.size() - 1);
for (int i = 0; i < (int)a.size(); i++)

for (int j = 0; j < (int)b.size(); j++)
add(c[i + j], a[i]*b[ j] % mod);
return c;
}
inline poly operator *(poly A, int b) {
for (auto &u : A)
u = u * b % mod;
return A;
}
int I[N];
inline int calc(const poly &A, int x) {
x %= mod;
int ans = 0;
for (int i = (int)A.size() - 1; ~i; --i)
ans = (ans * x + A[i]) % mod;
return ans;
}
inline poly solve(poly X, poly Y, int n) {
poly B{1}, ans, A(n + 1);
for (int i = 0; i <= n; i++)
B = B * (poly) {mod - X[i], 1}, I[i] = Inv(X[i]);
for (int i = 0; i <= n; i++) {
A[0] = B[0] * Inv(mod - X[i]) % mod;
for (int j = 1; j <= n; j++)
A[ j] = (A[ j - 1] - B[ j] + mod) * I[i] % mod;
ans = ans + A * (Y[i] * Inv(calc(A, X[i])) % mod);
}
return ans;
}
}
int F[1 << N], G[1 << N], pw[N + 1];
inline int solve(int val) {
pw[0] = 1;
for (int j = 1; j <= n; ++j)
pw[ j] = pw[ j - 1] * val % mod;
for (int T = 1; T <= tot; ++T) {
G[T] = F[T] = 0;
for (int j = 0; j <= n; ++j)
add(G[T], g[T][ j]*sig( j + 1) % mod * pw[ j] % mod);
}
F[0] = 1;

for (int S = 1; S <= tot; ++S)
for (int T = S; T; T = (T - 1)&S)
if (check(S - T, T))
add(F[S], F[S - T] * G[T] % mod);
return F[tot];
}
signed main() {
freopen("timeline.in", "r", stdin);
freopen("timeline.out", "w", stdout);
ios::sync_with_stdio(false);
cin.tie(0), cout.tie(0);
cin >> n >> m >> k, fac[0] = fac[1] = ifac[0] = ifac[1] = 1, tot = (1 << n) - 1;
for (int i = 2; i < (1 << N); ++i)
fac[i] = fac[i - 1] * i % mod, ifac[i] = (mod - mod / i) * ifac[mod % i] % mod;
for (int i = 2; i < (1 << N); ++i)
ifac[i] = ifac[i - 1] * ifac[i] % mod;
for (int i = 1, u, v; i <= m; ++i)
cin >> u >> v, --u, --v, in[1 << v] |= 1 << u;
h[0] = g[0][0] = 1;
for (int S = 1; S <= tot; ++S)
in[S] |= in[S - (S & -S)] | in[S & -S];
for (int S = 1; S <= tot; ++S)
for (int i = 0; i < n; ++i)
if (S >> i & 1 && check(1 << i, S - (1 << i)))
add(h[S], h[S - (1 << i)]);
for (int i = 1; i <= n; ++i)
for (int S = 1; S <= tot; ++S)
for (int T = S; T; T = (T - 1)&S)
if ((T & -T) == (S & -S) && check(S - T, T) && check(T, S - T))
add(g[S][i], g[S - T][i - 1] * h[T] % mod);
poly X(n + 1), Y(n + 1);
for (int i = 0; i <= n; ++i)
X[i] = i + 1, Y[i] = solve(i + 1);
poly f = Lagrange::solve(X, Y, n);
int ans = 0;
for (int i = 1; i <= min(k + 1, n); ++i)
add(ans, fac[k]*fac[k + 1] % mod * ifac[k + 1 - i] % mod * f[i] % mod);
cout << ans *ifac[n + k] % mod << "\n";
}


