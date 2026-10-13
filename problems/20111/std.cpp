#include "train.h"
#include <bits/stdc++.h>
#define ull unsigned long long
#define ll long long
#define pb push_back
#define mkp make_pair
#define fi first
#define se second
#define inf 1e9
#define infll 1000000000000000000ll
#define pii pair<int,int>
#define F(i,a,b) for(int i=a;i<=(b);i++)
#define dF(i,a,b) for(int i=a;i>=(b);i--)
#define wh(lzm) while(lzm--)
#define cmh(sjy) while(sjy--)
#define lowbit(x) (x&(-x))
#define HH printf("\n")
#define eb emplace_back
using namespace std;
ll read() {
ll x = 0, f = 1;
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
void chkmin(int &x, int y) {
x = min(x, y);
}
void chkmax(int &x, int y) {
x = max(x, y);
}
void chkmin(ll &x, ll y) {
x = min(x, y);
}
void chkmax(ll &x, ll y) {
x = max(x, y);
}
const int mod = 998244353, maxn = 500005;
namespace DS {
int B = 600, bel[maxn], bl[maxn], br[maxn], suf[maxn], sum[maxn], N;
void build(int siz) {
N = siz, B = sqrt(N);
F(i, 1, N) bel[i] = (i - 1) / B + 1;
F(i, 1, bel[N]) bl[i] = (i - 1) * B + 1, br[i] = min(i * B, N);

}
void add(int pos, int val = 1) {
dF(i, bel[pos], 1) suf[i] += val;
dF(i, pos, bl[bel[pos]]) sum[i] += val;
}
ll query(int x) {
return (x > N) ? 0 : suf[bel[x] + 1] + sum[x];
}
}
namespace seg {
int ls[maxn << 5], rs[maxn << 5], siz;
ll mn[maxn << 5], lz[maxn << 5];
void pushdown(int o) {
if (lz[o])
lz[ls[o]] += lz[o], lz[rs[o]] += lz[o], mn[ls[o]] += lz[o], mn[rs[o]] += lz[o], lz[o] = 0;
}
int build(int l, int r) {
int o = ++siz;
mn[o] = infll;
if (l == r)
return o;
int mid = (l + r) >> 1;
ls[o] = build(l, mid), rs[o] = build(mid + 1, r);
return o;
}
void update(int o, int l, int r, int ql, int qr, ll val) {
if (ql > qr || !o)
return;
if (ql <= l && qr >= r)
return lz[o] += val, mn[o] += val, void();
int mid = (l + r) >> 1;
pushdown(o);
if (ql <= mid)
update(ls[o], l, mid, ql, qr, val);
if (qr > mid)
update(rs[o], mid + 1, r, ql, qr, val);
mn[o] = min(mn[ls[o]], mn[rs[o]]);
}
ll query(int o, int l, int r, int ql, int qr) {
if (ql > qr || !o)
return infll;
if (ql <= l && qr >= r)
return mn[o];
int mid = (l + r) >> 1;
pushdown(o);
ll res = infll;

if (ql <= mid)
res = query(ls[o], l, mid, ql, qr);
if (qr > mid)
chkmin(res, query(rs[o], mid + 1, r, ql, qr));
return res;
}
}
int n, m, cmh, Root[maxn];
ll a[maxn], f[maxn], ans = -1;
struct Edge {
int u, v, l, r;
ll w;
bool operator<(const Edge &rhs)const {
return l < rhs.l;
}
} e[maxn];
struct Dinner {
int l, r;
bool operator<(const Dinner &rhs) {
return r < rhs.r;
}
} q[maxn];
int lsh[maxn], tot;
void Discretization() {
F(i, 1, m) lsh[++tot] = e[i].l, lsh[++tot] = e[i].r;
F(i, 1, cmh) lsh[++tot] = q[i].l, lsh[++tot] = q[i].r;
sort(lsh + 1, lsh + tot + 1), tot = unique(lsh + 1, lsh + tot + 1) - lsh - 1;
F(i, 1, m) e[i].l = lower_bound(lsh + 1, lsh + tot + 1, e[i].l) - lsh;
F(i, 1, m) e[i].r = lower_bound(lsh + 1, lsh + tot + 1, e[i].r) - lsh;
F(i, 1, cmh) q[i].l = lower_bound(lsh + 1, lsh + tot + 1, q[i].l) - lsh;
F(i, 1, cmh) q[i].r = lower_bound(lsh + 1, lsh + tot + 1, q[i].r) - lsh;
}
vector<int>vec[maxn];
int deg[maxn], Limit = 330, Rid[maxn];
ll solve(int N, int M, int W, std::vector<int>T, std::vector<int> X, std::vector<int> Y, std::vector<int> A,
std::vector<int> B, std::vector<int> C, std::vector<int> L, std::vector<int> R) {
n = N, m = M, cmh = W, Limit = 1500;
F(i, 1, n) a[i] = T[i - 1];
F(i, 1, m) e[i] = (Edge) {
X[i - 1] + 1, Y[i - 1] + 1, A[i - 1], B[i - 1], C[i - 1]
};
F(i, 1, cmh) q[i] = (Dinner) {
L[i - 1], R[i - 1]
};
Discretization(), sort(e + 1, e + m + 1), sort(q + 1, q + cmh + 1);
e[0] = (Edge) {1, 1, 0, 0, 0}, e[m + 1] = (Edge) {
n, n, tot + 1, tot + 1, 0
};
F(i, 0, m) vec[e[i].v].push_back(i), ++deg[e[i].v];
vector<int>Division;
F(i, 1, n) {
assert(deg[i] == (int)vec[i].size());

sort(vec[i].begin(), vec[i].end(), [&](int x, int y) {
return e[x].r < e[y].r;
});
F( j, 0, deg[i] - 1) Rid[vec[i][ j]] = j;
if (deg[i] >= Limit)
Division.push_back(i);
}
DS::build(tot);
for (int i : Division)
Root[i] = seg::build(0, deg[i] - 1);
F(i, 1, m + 1) f[i] = infll;
int p = 0;
F(i, 1, m + 1) {
for (; p < cmh && q[p + 1].r < e[i].l; ++p) {
DS::add(q[p + 1].l);
for (int u : Division)
if (!vec[u].empty() && e[vec[u][0]].r < q[p + 1].l) {
int pos = 0, l = 0, r = deg[u] - 1;
while (l <= r) {
int mid = (l + r) >> 1;
if (e[vec[u][mid]].r < q[p + 1].l)
pos = mid, l = mid + 1;
else
r = mid - 1;
}
seg::update(Root[u], 0, deg[u] - 1, 0, pos, a[u]);
}
}
const int u = e[i].u;
if (vec[e[i].u].empty() || e[vec[e[i].u][0]].r > e[i].l)
continue;
if (deg[u] < Limit) {
for (int j : vec[u]) {
if (e[ j].r > e[i].l)
break;
chkmin(f[i], f[ j] + DS::query(e[ j].r + 1)*a[u] + e[i].w);
}
} else {
int pos = 0, l = 0, r = deg[u] - 1;
while (l <= r) {
int mid = (l + r) >> 1;
if (e[vec[u][mid]].r <= e[i].l)

pos = mid, l = mid + 1;
else
r = mid - 1;
}
f[i] = seg::query(Root[u], 0, deg[u] - 1, 0, pos) + e[i].w;
}
const int v = e[i].v;
if (i <= m && deg[v] >= Limit)
seg::update(Root[v], 0, deg[v] - 1, Rid[i], Rid[i], f[i] - infll);
}
ll ans = f[m + 1];
if (ans > 1e16)
ans = -1;
return ans;
}


