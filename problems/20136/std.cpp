#include <algorithm>
#include <cstdio>
namespace Main {
using namespace std;
typedef long long LL;
typedef unsigned long long UL;
LL read() {
LL res = 0, ch;
bool flg = 0;
for (ch = getchar(); (ch < '0' || ch > '9') && ch != '-';)
ch = getchar();
if (ch == '-') {
ch = getchar();
flg = 1;
}
for (; ch >= '0' && ch <= '9'; ch = getchar())
res = (res << 1) + (res << 3) + (ch & 15);
return res * (flg ? -1 : 1);
}
constexpr static bool T = 1;
constexpr static LL N = 1 << 17, INF = 1e18;
LL n, m, a[N], res[N];
pair<LL, LL> c[N];
LL dp(LL k, LL mx) {
if (k >> n)
return a[k] < mx ? INF : 0;
LL l = dp(k << 1, mx), r = dp(k << 1 | 1, mx);
return l + min(a[k], r);
}
LL calc(LL k, LL mx, LL v) {
LL res = dp(k, max(v, mx));
if (k & 1 && k > 1 && v < mx)
res = min(res, dp(k, v) + a[k >> 1]);
return res;
}
void dfs(LL k, LL mx) {
if (k >> n) {
if (a[k] < mx)

m -= a[k >> 1];
res[++res[0]] = a[k];
return;
}
LL l = k, r = k, p;
while (!(l >> n))
l <<= 1;
while (!(r >> n))
r = r << 1 | 1;
for (LL i = l; i <= r; ++i)
c[i] = {a[i], i};
sort(c + l, c + r + 1);
for (LL mid; l < r;)
calc(k, mx, c[mid = (l + r + 1) >> 1].first) <= m ? l = mid : r = mid - 1;
m -= calc(k, mx, c[l].first);
res[++res[0]] = mx = a[p = c[l].second];
for (; p != k; p >>= 1) {
m += min(p & 1 ? INF : a[p >> 1], dp(p ^ 1, mx));
dfs(p ^ 1, mx);
}
return;
}
void solve() {
n = read();
m = read();
for (LL i = 1; i < 1 << (n + 1); ++i)
a[i] = read();
res[0] = 0;
dfs(1, 0);
for (int i = 1; i <= res[0]; ++i)
printf("%lld ", res[i]);
putchar('\n');
return;
}
void main() {
freopen("maze.in", "r", stdin);
freopen("maze.out", "w", stdout);
for (int t = T ? read() : 1; t; --t)

solve();
fclose(stdin);
fclose(stdout);
return;
}
} // namespace Main
int main() {
Main::main();
return 0;
}


