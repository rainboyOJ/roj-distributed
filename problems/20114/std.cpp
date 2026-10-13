#include <bits/stdc++.h>
#define ll long long
#define mid (l+r>>1)
#define rep(x,y,z) for(int x=(y);x<=(z);x++)
#define per(x,y,z) for(int x=(y);x>=(z);x--)
#define repn(x) rep(x,1,n)
#define repm(x) rep(x,1,m)
#define pb push_back
#define e(x) for(int i=h[x],y=to[i];i;i=nxt[i],y=to[i])
#define E(x) for(auto y:p[x])
inline int read() {
int s = 0, w = 1;
char c = getchar();
while (c < 48 || c > 57) {
if (c == '-')
w = -1;
c = getchar();
}
while (c >= 48 && c <= 57)
s = (s << 1) + (s << 3) + c - 48, c = getchar();
return s * w;
}
using namespace std;
const int N = 2e5 + 5, inf = (1LL << 31) - 1;
struct nod {
int x, d;
} S;
struct node {
nod mx, se, th;
} a[N];
inline bool cmp(nod a, nod b) {
return a.d <= b.d;
}
inline void insert(node &x, nod k) {
if (cmp(x.mx, k))
x.th = x.se, x.se = x.mx, x.mx = k;
else if (cmp(x.se, k))
x.th = x.se, x.se = k;
else if (cmp(x.th, k))
x.th = k;
}
int n, m, h[N], to[N << 1], nxt[N << 1], cnt, dep[N], f[N][19], t[N], d[N];
inline void add_(int a, int b) {
to[++cnt] = b, nxt[cnt] = h[a], h[a] = cnt;
to[++cnt] = a, nxt[cnt] = h[b], h[b] = cnt;
}
inline void dfs(int x, int fa) {
dep[x] = dep[fa] + 1, f[x][0] = fa;
rep(i, 1, 18)f[x][i] = f[f[x][i - 1]][i - 1];

e(x)if (y ^ fa)
dfs(y, x), insert(a[x], {a[y].mx.x, a[y].mx.d + 1});
}
struct spe {
int y;
nod k;
};
inline void Dfs(int x, int fa, nod k) {
vector<spe>p;
nod pr = k;
insert(a[x], k), k.d++;
if (cmp(k, {x, 1}))
k = {x, 1};
e(x)if (y ^ fa) {
nod nw = a[y].mx;
nw.d += 2, p.pb({y, k});
if (cmp(k, nw))
k = nw;
}
k = pr, k.d++;
if (cmp(k, {x, 1}))
k = {x, 1};
int siz = p.size();
per(i, siz - 1, 0) {
int y = p[i].y;
nod nw = a[y].mx;
nw.d += 2;
if (cmp(p[i].k, k))
p[i].k = k;
Dfs(y, x, p[i].k);
if (cmp(k, nw))
k = nw;
}
}
vector<int>p[N], q[N];
struct que {
int a, b, c;
} b[N], g[N];
inline void ad(int x, int k) {
x = n + 1 - x;
while (x <= n + 1)
t[x] = cmp(a[t[x]].th, a[k].th) ? k : t[x], x += x & -x;
}
inline int query(int x) {
x = n + 1 - x;
int ans = 0;

while (x)
ans = cmp(a[ans].th, a[t[x]].th) ? t[x] : ans, x -= x & -x;
return ans;
}
inline void sor(int &a, int &b, int &c) {
int d = max({a, b, c}), e = min({a, b, c}), s = a + b + c;
a = d, b = s - d - e, c = e;
}
inline void jump(int &x, int dep) {
int p = 0;
while (dep) {
if (dep & 1)
x = f[x][p];
p++, dep >>= 1;
}
}
inline int lca(int x, int y) {
if (dep[x] < dep[y])
swap(x, y);
jump(x, dep[x] - dep[y]);
per(i, 18, 0)if (f[x][i]^f[y][i])
x = f[x][i], y = f[y][i];
return x == y ? x : f[x][0];
}
inline int dist(int x, int y) {
return dep[x] + dep[y] - dep[lca(x, y)] * 2;
}
inline int getp(int x, int y, int d) {
int la = lca(x, y);
int dx = dep[x] - dep[la], dy = dep[y] - dep[la], dis = dx + dy;
if (dx >= d)
return jump(x, d), x;
return jump(y, dis - d), y;
}
inline bool che(int a, int b, int c, int i) {
return dist(a, b) == g[i].a && dist(a, c) == g[i].b && dist(b, c) == g[i].c;
}
inline void solve(int &a, int &b, int &c, int i) {
if (che(a, b, c, i))
return;
if (che(a, c, b, i))
return swap(b, c), void();
if (che(b, a, c, i))
return swap(a, b), void();

if (che(b, c, a, i))
return swap(a, b), swap(b, c), void();
if (che(c, a, b, i))
return swap(a, c), swap(b, c), void();
swap(a, c);
}
inline void Main() {
n = read(), S.d = -inf, a[0].th = S;
repn(i)a[i] = {{i, 0}, S, S};
rep(i, 2, n)add_(read(), read());
dfs(1, 0), Dfs(1, 0, S);
repn(i)insert(a[i], {i, 0}), insert(a[i], {i, 0}), p[a[i].mx.d].pb(i);
m = read();
repm(i) {
int x = read(), y = read(), z = read();
b[i] = {(x + y - z) / 2, (x - y + z) / 2, (-x + y + z) / 2}, g[i] = {x, y, z}, sor(b[i].a, b[i].b, b[i].c),
q[b[i].a].pb({i});
}
per(i, n, 0) {
E(i)ad(a[y].se.d, y);
for (auto y : q[i])
d[y] = query(b[y].b);
}
repm(i) {
int x = d[i], u = getp(x, a[x].mx.x, b[i].a), v = getp(x, a[x].se.x, b[i].b), w = getp(x, a[x].th.x, b[i].c);
solve(u, v, w, i), printf("%d %d %d\n", u, v, w);
}
}
signed main() {
int T = 1;
while (T--)
Main();
return 0;
}


