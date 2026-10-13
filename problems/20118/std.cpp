#include <bits/stdc++.h>
#define N 1000004
#define INF 1000000000000000000
using namespace std;
typedef long long ll;
int n, E, id[N], stk[N], tp, q[N], bit[N + 1];
ll ans, pre[N];
struct Pnt {
int a, b, c;
} p[N];
struct Seg {
int l, r;
ll mx, tg;
} tr[N * 4];
void buildST(int u, int l, int r) {
tr[u].l = l;
tr[u].r = r;
tr[u].mx = E;
if (l == r) {
return;
}
int md = (l + r) / 2;
buildST(u * 2, l, md);
buildST(u * 2 + 1, md + 1, r);
}
void pushdown(int u) {
if (tr[u].tg == 0) {
return;
}
ll num = tr[u].tg;
tr[u].tg = 0;
tr[u * 2].tg += num;
tr[u * 2].mx += num;
tr[u * 2 + 1].tg += num;
tr[u * 2 + 1].mx += num;
}
void add1(int u, int l, int r, ll num) {
if (tr[u].l > r || tr[u].r < l) {
return;
}
if (l <= tr[u].l && tr[u].r <= r) {
tr[u].tg += num;
tr[u].mx += num;
return;
}
pushdown(u);

add1(u * 2, l, r, num);
add1(u * 2 + 1, l, r, num);
tr[u].mx = max(tr[u * 2].mx, tr[u * 2 + 1].mx);
}
int find(int u) {
if (tr[u].l == tr[u].r) {
return tr[u].l;
}
pushdown(u);
if (tr[u * 2].mx < 0) {
return find(u * 2 + 1);
} else {
return find(u * 2);
}
}
void add2(int x) {
while (x <= n + 1) {
bit[x]++;
x += (x & (-x));
}
}
ll qry(int x) {
int res = 0;
while (x) {
res += bit[x];
x -= (x & (-x));
}
return res;
}
bool cmp(const int &a, const int &b) {
return (pre[a] < pre[b] || (pre[a] == pre[b] && a < b));
}
int main() {
// freopen("top.in", "r", stdin);
// freopen("top.out", "w", stdout);
scanf("%d %d", &n, &E);
for (int i = 1; i <= n; i++) {
scanf("%d", &p[i].a);
}
for (int i = 1; i <= n; i++) {
scanf("%d", &p[i].b);
p[i].c = min(p[i].a, p[i].b);
}
for (int i = 1; i <= n; i++) {

pre[i] = pre[i - 1] + p[i].b - p[i].a;
id[i] = i;
}
id[0] = 0;
buildST(1, 1, n + 1);
for (int i = 1; i <= n; i++) {
ll val = p[i].b - p[i].a;
if (val < 0) {
add1(1, 1, i, val);
}
add1(1, i, i, -p[i].c);
while (tp > 0 && p[stk[tp]].c < p[i].c) {
add1(1, stk[tp - 1] + 1, stk[tp], p[stk[tp]].c - p[i].c);
tp--;
}
stk[++tp] = i;
q[i] = find(1) - 1;
}
sort(id, id + n + 1, cmp);
ll ans = 0;
for (int ii = 0; ii <= n; ii++) {
int i = id[ii];
int pos = q[i];
add2(i + 1);
if (i > 0)
ans += qry(i) - qry(pos);
}
printf("%lld\n", ans);
return 0;
}


