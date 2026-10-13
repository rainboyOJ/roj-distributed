#include <bits/stdc++.h>
#define ll long long
#define pb push_back
#define fi first
#define se second
#define inf 1e9
#define infll 1e18
#define pii pair<int,int>
#define F(i,a,b) for(int i=a;i<=(b);i++)
#define dF(i,a,b) for(int i=a;i>=(b);i--)
#define wh(lzm) while(lzm--)
#define cmh(sjy) while(sjy--)
#define lowbit(x) (x&(-x))
#define HH printf("\n")
#define eb emplace_back
using namespace std;
int read() {
int x = 0, f = 1;
char c = getchar();
while (c < '0' || c > '9') {
if (c == '-')
f = -1;
c = getchar();
}
while (c >= '0' && c <= '9')
x = (x << 3) + (x << 1) + (c ^ 48), c = getchar();
return x * f;
}
const int mod = 998244353, maxn = 1005;
int n, R, C, a[maxn][maxn], nxt[maxn][maxn];
void dfs(int u, int v, int x, int y) {
if (!nxt[v][y])
return nxt[u][y] = v, nxt[v][y] = u, nxt[v][x] = 0, void();
int t = nxt[v][y];
if (nxt[t][x])
dfs(t, nxt[t][x], x, y);
else
nxt[t][y] = 0;
nxt[t][x] = v, nxt[v][x] = t;
nxt[v][y] = u, nxt[u][y] = v;
}
void ins(int u, int v) {
int mex1 = 1, mex2 = 1;
for (; nxt[u][mex1]; ++mex1);

for (; nxt[v][mex2]; ++mex2);
if (mex1 == mex2)
return nxt[u][mex1] = v, nxt[v][mex1] = u, void();
dfs(u, v, mex2, mex1);
}
int Fill_matrix() {
vector<int>vec(n + 1, C);
F(i, 1, R) F( j, 1, C) vec[a[i][ j]]--;
F(i, 1, n) if (vec[i] > n - R)
return 0;
F(i, 1, n << 1) F( j, 1, n << 1) nxt[i][ j] = 0;
F( j, 1, C) {
F(i, 1, n) vec[i] = 0;
F(i, 1, R) vec[a[i][ j]] = 1;
F(i, 1, n) if (!vec[i])
ins( j, C + i);
}
F(i, R + 1, n) F( j, 1, C) a[i][ j] = nxt[ j][i - R] - C;
return 1;
}
namespace subtaskB {
void solve() {
puts("Yes");
F(i, 1, n << 1) F( j, 1, n << 1) nxt[i][ j] = 0;
vector<int>vec(n + 1, 0);
F(i, 1, n) {
F( j, 1, n) vec[ j] = 0;
F( j, 1, C) vec[a[i][ j]] = 1;
F( j, 1, n) if (!vec[ j])
ins(i, n + j);
}
F(i, 1, n) F( j, C + 1, n) a[i][ j] = nxt[i][ j - C] - n;
F(i, 1, n) {
F( j, 1, n) printf("%d ", a[i][ j]);
puts("");
}
}
}
void solve() {
n = read(), R = read(), C = read();
F(i, 1, R) F( j, 1, C) a[i][ j] = read();
if ((R ^ n) && !Fill_matrix())
return puts("No"), void();
subtaskB::solve();
}
signed main() {
int sjy = read();

cmh(sjy) solve();
}


