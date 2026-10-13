#include <bits/stdc++.h>
using namespace std;
using LL = long long;
using ULL = unsigned long long;
#define F(i, l, r) for (int i = (l); i <= (r); ++i)
#define FF(i, r, l) for (int i = (r); i >= (l); --i)
#define MAX(a, b) ((a) = max(a, b))
#define MIN(a, b) ((a) = min(a, b))
#define SZ(a) ((int)((a).size()) - 1)
constexpr int N = 200005, BB = 420, MOD = 998244353;
ULL kpow(ULL x, ULL k = MOD - 2) {
x = x % MOD;
ULL r = 1;
while (k) {
if (k & 1)
r = r * x % MOD;
x = x * x % MOD;
k >>= 1;
}
return r;
}
int t;
int p[N], q[N];
array<int, 3> a[N];
ULL res[N], fac[N], ifac[N], iv[N];
ULL C(int n, int r) {
if (0 <= r && r <= n)
return fac[n] * ifac[r] % MOD * ifac[n - r] % MOD;
return 0;
}
signed main(void) {
// freopen(".in", "r", stdin);
// freopen(".out", "w", stdout);
ios::sync_with_stdio(0), cin.tie(nullptr);
fac[0] = 1;
F(i, 1, 200001) fac[i] = fac[i - 1] * i % MOD, iv[i] = kpow(i);
ifac[200000] = kpow(fac[200000]);
FF(i, 200000, 1) ifac[i - 1] = ifac[i] * i % MOD;
cin >> t;

F(i, 1, t) {
cin >> p[i] >> q[i];
if (q[i] > p[i] - q[i])
a[i] = {0, 0, i};
else
a[i] = {p[i] - q[i], p[i] - q[i] - q[i], i};
}
sort(a + 1, a + t + 1, [](array<int, 3> x, array<int, 3> y) {
if (x[0] / BB != y[0] / BB)
return x[0] < y[0];
return x[1] < y[1];
});
int cn = 0, cm = 0;
ULL A = 1, B = 0;
F(i, 1, t) {
if (cm > a[i][1]) {
cn = 0, cm = 0;
A = 1, B = 0;
}
int recn = cn, recm = cm;
ULL recA = A, recB = B;
while (cn < a[i][0]) {
++cn;
ULL x = (A + B) % MOD, y = ((cm + 1) * x + (cn - cm) * B) % MOD;
A = x, B = y;
if (cn % BB == 0)
recn = cn, recA = A, recB = B;
}
while (cm < a[i][1]) {
++cm;
ULL x = (B + MOD - cm * A % MOD) * iv[cn - cm + 1] % MOD, y = (B + MOD - x) % MOD;
A = x, B = y;
}
res[a[i][2]] = A;
cn = recn, cm = recm;
A = recA, B = recB;
while (cm < a[i][1] && cm < cn) {
++cm;
ULL x = (B + MOD - cm * A % MOD) * iv[cn - cm + 1] % MOD, y = (B + MOD - x) % MOD;
A = x, B = y;
}
}
F(i, 1, t) {
if (q[i] > p[i] - q[i])

cout << 0 << '\n';
else
cout << res[i] * C(p[i] - q[i], q[i]) % MOD *fac[q[i]] % MOD << '\n';
}
return 0;
}


