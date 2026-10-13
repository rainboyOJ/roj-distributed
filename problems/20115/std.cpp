#include <bits/stdc++.h>
using namespace std;
const int N = 3e3 + 10;
const int INF = 0x3f3f3f3f;
const int P = 998244353;
int t, n, a[N][N], b[N][N], c[N][N], d[N];
int res1[N], res2[N], res3[N];
mt19937 Rand(time(0));
bool check(void) {
for (int i = 1; i <= n; ++i)
d[i] = Rand() % P, res1[i] = res2[i] = res3[i] = 0;
for (int i = 1; i <= n; ++i)
for (int j = 1; j <= n; ++j)
res1[i] = (res1[i] + 1ll * d[ j] * a[ j][i]) % P;
for (int i = 1; i <= n; ++i)
for (int j = 1; j <= n; ++j)
res2[i] = (res2[i] + 1ll * res1[ j] * b[ j][i]) % P;
for (int i = 1; i <= n; ++i)
for (int j = 1; j <= n; ++j)
res3[i] = (res3[i] + 1ll * d[ j] * c[ j][i]) % P;
for (int i = 1; i <= n; ++i)
if (res2[i] != res3[i])
return 0;
return 1;
}
int main(void) {
ios::sync_with_stdio(0);
int T;
cin >> T;
while (T--) {
cin >> n;
for (int i = 1; i <= n; ++i)
for (int j = 1; j <= n; ++j)
cin >> a[i][ j];
for (int i = 1; i <= n; ++i)
for (int j = 1; j <= n; ++j)
cin >> b[i][ j];
for (int i = 1; i <= n; ++i)
for (int j = 1; j <= n; ++j)
cin >> c[i][ j];
cout << (check() ? "Yes\n" : "No\n");

}
return 0;
}


