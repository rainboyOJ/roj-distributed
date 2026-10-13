// 如何不分析性质，暴力通过这道题
// what is matter? never mind.
//#pragma GCC optimize("Ofast")
//#pragma GCC optimize("unroll-loops")
//#pragma GCC target("sse,sse2,sse3,sse4,popcnt,abm,mmx,avx,avx2")
#include <bits/stdc++.h>
#define For(i,a,b) for(int i=(a);i<=(b);++i)
#define Rep(i,a,b) for(int i=(a);i>=(b);--i)
#define ll long long
//#define int long long
//#define ull unsigned long long
using namespace std;
inline int read() {
char c = getchar();
int x = 0;
bool f = 0;
for (; !isdigit(c); c = getchar())
f ^= !(c ^ 45);
for (; isdigit(c); c = getchar())
x = (x << 1) + (x << 3) + (c ^ 48);
if (f)
x = -x;
return x;
}
int mod;
typedef unsigned long long ull;
namespace FM {
typedef __uint128_t L;
struct FastMod {
ull b, m;
FastMod(ull b): b(b), m(ull((L(1) << 64) / b)) {}
ull reduce(ull a) {
ull q = (ull)((L(m) * a) >> 64), r = a - q * b;
return r >= b ? r - b : r;
}
};
FastMod F(2);
}
struct modint {
int x;
modint(int o = 0) {
x = o;
}
modint &operator = (int o) {
return x = o, *this;
}
modint &operator +=(modint o) {
return x = x + o.x >= mod ? x + o.x - mod : x + o.x, *this;
}
modint &operator -=(modint o) {
return x = x - o.x < 0 ? x - o.x + mod : x - o.x, *this;

}
modint &operator *=(modint o) {
return x = FM::F.reduce(1ull * x * o.x), *this;
}
modint &operator ^=(int b) {
modint a = *this, c = 1;
for (; b; b >>= 1, a *= a)
if (b & 1)
c *= a;
return x = c.x, *this;
}
modint &operator /=(modint o) {
return *this *= o ^= mod - 2;
}
friend modint operator +(modint a, modint b) {
return a += b;
}
friend modint operator -(modint a, modint b) {
return a -= b;
}
friend modint operator *(modint a, modint b) {
return a *= b;
}
friend modint operator /(modint a, modint b) {
return a /= b;
}
friend modint operator ^(modint a, int b) {
return a ^= b;
}
friend bool operator ==(modint a, int b) {
return a.x == b;
}
friend bool operator !=(modint a, int b) {
return a.x != b;
}
bool operator !() {
return !x;
}
modint operator - () {
return x ? mod - x : 0;
}
bool operator <(const modint &b)const {
return x < b.x;
}
};
inline modint qpow(modint x, int y) {
return x ^ y;
}
void initmod() {
mod = read(), FM::F = FM::FastMod(mod);
}
vector<modint> fac, ifac, iv;
inline void initC(int n) {
if (iv.empty())

fac = ifac = iv = vector<modint>(2, 1);
int m = iv.size();
++n;
if (m >= n)
return;
iv.resize(n), fac.resize(n), ifac.resize(n);
For(i, m, n - 1) {
iv[i] = iv[mod % i] * (mod - mod / i);
fac[i] = fac[i - 1] * i, ifac[i] = ifac[i - 1] * iv[i];
}
}
inline modint C(int n, int m) {
if (m < 0 || n < m)
return 0;
return initC(n), fac[n] * ifac[m] * ifac[n - m];
}
inline modint sign(int n) {
return (n & 1) ? (mod - 1) : (1);
}
#define fi first
#define se second
#define pb push_back
#define mkp make_pair
typedef pair<int, int>pii;
typedef vector<int>vi;
#define maxn 500005
#define inf 0x3f3f3f3f
//(2,2m,-2m-2,-m*m-2m+1,2m,m*m)
int n;
modint m;
modint f[maxn];
signed main() {
n = read(), m = read(), initmod();
f[2] = (m + 1) * (m + 1);
f[3] = m * m * m / 3 + m * m * 2 + m * 8 / 3 + 1;
f[4] = m * m * m * 7 / 3 + m * m * 5 + m * 11 / 3 + 1;
f[5] = m * m * m * m * 7 / 12 + m * m * m * 17 / 3 + m * m * 89 / 12 + m * 13 / 3 + 1;
f[6] = m * m * m * m * 25 / 6 + m * m * m * 38 / 3 + m * m * 71 / 6 + m * 16 / 3 + 1;
f[7] = m * m * m * m * m * 5 / 6 + m * m * m * m * 37 / 3 + m * m * m * 133 / 6 + m * m * 47 / 3 + m * 6 + 1;
For(i, 8, n)f[i] = f[i - 1] * 2 + f[i - 2] * 2 * m + f[i - 3] * ((-m) * 2 - 2) + f[i - 4] * ((
-m) * m - m * 2 + 1) + f[i - 5] * m * 2 + f[i - 6] * m * m;
cout << f[n].x;
return 0;
}


