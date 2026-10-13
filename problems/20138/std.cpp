#include <algorithm>
#include <stdio.h>
#include <vector>
typedef long long llt;
typedef unsigned uint;
typedef unsigned long long ullt;
typedef bool bol;
typedef char chr;
typedef void voi;
typedef double dbl;
template<typename T>bol _max(T &a, T b) {
return (a < b) ? a = b, true : false;
}
template<typename T>bol _min(T &a, T b) {
return (b < a) ? a = b, true : false;
}
template<typename T>T lowbit(T n) {
return n & -n;
}
template<typename T>T gcd(T a, T b) {
return b ? gcd(b, a % b) : a;
}
template<typename T>T lcm(T a, T b) {
return (a != 0 || b != 0) ? a / gcd(a, b) * b : (T)0;
}
template<typename T>T exgcd(T a, T b, T &x, T &y) {
if (b != 0) {
T ans = exgcd(b, a % b, y, x);
y -= a / b * x;
return ans;
} else
return y = 0, x = 1, a;
}
template<typename T>T power(T base, T index, T mod) {
T ans = 1 % mod;
while (index) {
if (index & 1)
ans = ans * base % mod;
base = base * base % mod, index >>= 1;
}
return ans;
}
using ulllt = __uint128_t;
ulllt read() {
ulllt ans = 0;
chr c;
do
c = getchar();
while (c > '9' || c < '0');

do
ans = ans * 10 + (c^'0'), c = getchar();
while (c >= '0' && c <= '9')
;
return ans;
}
voi print(ulllt v) {
if (v >= 10)
print(v / 10);
putchar(v % 10 + '0');
}
// Your shadow Gets in the way of my light
ulllt A[100005], ans;
uint B[100005];
ullt SB[100005];
uint n, m, k;
voi dfs(uint b, uint l, uint r, uint m, ulllt v, ulllt up, ulllt t) {
if (!~b) {
_max(ans, std::min(v, t));
return;
}
bol ok = false;
ulllt w0 = (ulllt)1 << b;
if (SB[r] - SB[l] <= m) {
_max(ans, std::min({v, t, (l == r ? (ulllt)1 << k : A[l] + up)}) + w0 * 2 - 1);
return;
}
uint mid = l;
if (!(A[r - 1] >> b & 1))
mid = r;
else if (!(A[l] >> b & 1)) {
uint r0 = r - 1;
while (mid < r0) {
uint t = (mid + r0) >> 1;
if (A[t] >> b & 1)
r0 = t;
else
mid = t + 1;
}
}
if (t + w0 > v) {
if (SB[r] - SB[mid] <= m) {
ulllt s = std::min(t, mid == r ? (ulllt)1 << k : A[mid] + up) + w0;

if (v < s)
dfs(b - 1, l, mid, m - (SB[r] - SB[mid]), v | w0, up | w0, s), ok = true;
}
if (SB[mid] - SB[l] <= m) {
ulllt s = std::min(t, l == mid ? (ulllt)1 << k : A[l] + up);
if (v < s)
dfs(b - 1, mid, r, m - (SB[mid] - SB[l]), v | w0, up, s), ok = true;
}
}
if (ok)
return;
dfs(b - 1, l, mid, m, v, up, t), dfs(b - 1, mid, r, m, v, up | w0, t + w0);
}
voi solve() {
scanf("%u%u%u", &n, &m, &k);
std::vector<std::pair<ulllt, uint>>P(n);
for (uint i = 0; i < n; i++)
P[i].first = read();
for (uint i = 0; i < n; i++)
scanf("%u", &P[i].second);
std::sort(P.begin(), P.end());
for (uint i = 0; i < n; i++)
A[i] = P[i].first, B[i] = P[i].second, SB[i + 1] = SB[i] + B[i];
if (SB[n] <= m) {
print(((ulllt)1 << k) - 1 + A[0]);
putchar('\n');
return;
}
ans = 0, dfs(k - 1, 0, n, m, 0, 0, (ulllt)1 << k), print(ans), putchar('\n');
}
int main() {
freopen("xor.in", "r", stdin);
freopen("xor.out", "w", stdout);
uint t;
scanf("%*u%u", &t);
while (t--)
solve();
return 0;
}


