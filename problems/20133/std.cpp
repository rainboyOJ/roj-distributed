#include <bits/stdc++.h>
using namespace std;
const int N = 100005;
int ax[N], ay[N];
struct AAA {
long long l, r;
};
long long Ceil(long long a, long long b) {
if (a < 0) {
a = -a;
b = -b;
}
if (b < 0)
return a / b;
return (a % b == 0 ? a / b : a / b + 1);
}
long long Floor(long long a, long long b) {
if (a < 0) {
a = -a;
b = -b;
}
if (b < 0)
return (a % b == 0 ? a / b : a / b - 1);
return a / b;
}
AAA solve(long long a, long long b, bool tag) {
if (tag) {
if (a > 0)
return AAA{0, Floor(b, a)};
else if (a < 0)
return AAA{max(0ll, Ceil(b, a)), INT64_MAX};
else {
if (0 <= b)
return AAA{0, INT64_MAX};
else
return AAA{1, 0};
}
} else {
if (a > 0)
return AAA{max(0ll, Ceil(b, a)), INT64_MAX};
else if (a < 0)
return AAA{0, Floor(b, a)};
else {
if (0 >= b)
return AAA{0, INT64_MAX};
else
return AAA{1, 0};
}
}
}

AAA merge(AAA aa, AAA bb) {
return AAA{max(aa.l, bb.l), min(aa.r, bb.r)};
}
int main() {
ios::sync_with_stdio(false);
cin.tie(nullptr);
cout.tie(nullptr);
freopen("wind.in", "r", stdin);
freopen("wind.out", "w", stdout);
int T;
cin >> T;
while (T--) {
int n, k, x, y;
long long sx = 0, sy = 0;
cin >> n >> k >> x >> y;
for (int i = 0; i < n; ++i) {
cin >> ax[i] >> ay[i];
sx += ax[i];
sy += ay[i];
}
long long nx = 0, ny = 0, ans = INT64_MAX;
for (int r = 0; r < n; ++r) {
AAA res1 = merge(merge(solve(sx, x - nx, true), solve(sy, y - ny, true)), solve(1ll * n * k + sx + sy,
+x + y - nx - ny - 1ll * r * k, false));
AAA res2 = merge(merge(solve(sx, x - nx, true), solve(sy, y - ny, false)), solve(1ll * n * k + sx - sy,
+x - y - nx + ny - 1ll * r * k, false));
AAA res3 = merge(merge(solve(sx, x - nx, false), solve(sy, y - ny, true)), solve(1ll * n * k - sx + sy,
-x + y + nx - ny - 1ll * r * k, false));
AAA res4 = merge(merge(solve(sx, x - nx, false), solve(sy, y - ny, false)), solve(1ll * n * k - sx - sy,
-x - y + nx + ny - 1ll * r * k, false));
if (res1.l <= res1.r)
ans = min(ans, res1.l * n + r);
if (res2.l <= res2.r)
ans = min(ans, res2.l * n + r);
if (res3.l <= res3.r)
ans = min(ans, res3.l * n + r);
if (res4.l <= res4.r)
ans = min(ans, res4.l * n + r);
nx += ax[r];
ny += ay[r];
}
if (ans == INT64_MAX)
cout << "-1\n";
else
cout << ans << '\n';

}
return 0;
}


