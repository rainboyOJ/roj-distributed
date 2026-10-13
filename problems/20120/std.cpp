#include <bits/stdc++.h>
using namespace std;
#define ll long long
char buf[1 << 21], *p1 = buf, *p2 = buf;
#define getchar() (p1==p2&&(p2=(p1=buf)+fread(buf,1,1<<21,stdin),p1==p2)?EOF:*p1++)
inline int read() {
int s = 0;
char ch = getchar();
while (ch < '0' || ch > '9')
ch = getchar();
while (ch >= '0' && ch <= '9')
s *= 10, s += ch ^ 48, ch = getchar();
return s;
}
struct HaitangSuki {
ll t0[510003], t1[10003], t2[1003], all;
void add(int x, ll k) {
t0[x] += k, t1[x >> 7] += k, t2[x >> 14] += k, all += k;
}
ll query(int x) {
ll res = all;
int d2 = x >> 14;
for (int i = 0; i < d2; ++i)
res -= t2[i];
int d1 = x >> 7;
for (int i = (d2 << 7); i < d1; ++i)
res -= t1[i];
for (int i = (d1 << 7); i <= x; ++i)
res -= t0[i];
return res;
}
} T;
struct node {
int op, l, r, x;
} a[500003];
vector<pair<int, int>> v[500003];
ll ans[500003];
int b[510003];
int pos[710][1003];
int val[710][1003];
ll pre[710][1003];
int cov[710], tag[710], last[710], len[710];
const int B = 900;
void build(int x, int tl, int tr) {
int d = 0;

for (int i = 1; i <= B; ++i)
if (pos[x][i] < tl || pos[x][i] > tr)
pos[x][++d] = pos[x][i];
for (int i = tl; i <= tr; ++i)
pos[x][++d] = i;
len[x] = 0;
for (int i = 1; i <= B; ++i) {
int j = i;
while ( j < B && b[pos[x][i]] == b[pos[x][ j + 1]])
++j;
val[x][++len[x]] = b[pos[x][i]],
pre[x][len[x]] = pre[x][len[x] - 1]
+ 1ll * ( j - i + 1) * a[val[x][len[x]]].x;
i = j;
}
return ;
}
struct query {
int x, p, v;
} c[500003], d[500003];
int buc[1024];
void down(int x, int t) {
if (!tag[x] || last[x] == t) {
last[x] = t;
return;
}
int l = x * B, r = (x + 1) * B - 1;
if (cov[x]) {
int mul = 0;
for (int i = last[x]; i < t; ++i) {
mul += (a[i].op == 2 && a[i].l < l && a[i].r > r);
for (auto [y, z] : v[i])
if (cov[x] >= y)
ans[z] += 1ll * a[cov[x]].x * B * mul;
}
T.add(cov[x], 1ll * a[cov[x]].x * B * tag[x]);
} else {
int mul = 0, qc = 0;
for (int i = last[x]; i < t; ++i) {
mul += (a[i].op == 2 && a[i].l < l && a[i].r > r);
for (auto [y, z] : v[i])
if (mul && val[x][len[x]] >= c[i].x)

c[++qc] = (query) {
y, z, mul
};
}
memset(buc, 0, sizeof(buc));
for (int i = 1; i <= qc; ++i)
++buc[c[i].x & 1023];
for (int i = 1; i < 1024; ++i)
buc[i] += buc[i - 1];
for (int i = qc; i >= 1; --i)
d[buc[c[i].x & 1023]--] = c[i];
memset(buc, 0, sizeof(buc));
for (int i = 1; i <= qc; ++i)
++buc[d[i].x >> 10];
for (int i = 1; i < 1024; ++i)
buc[i] += buc[i - 1];
for (int i = qc; i >= 1; --i)
c[buc[d[i].x >> 10]--] = d[i];
for (int i = 1, j = 0; i <= qc; ++i) {
while ( j < len[x] && val[x][ j + 1] < c[i].x)
++j;
ans[c[i].p] += (pre[x][len[x]] - pre[x][ j]) * c[i].v;
}
for (int i = l; i <= r; ++i)
T.add(b[i], 1ll * a[b[i]].x * tag[x]);
}
tag[x] = 0, last[x] = t;
}
void brute(int x) {
if (!cov[x])
return ;
int l = x * B, r = (x + 1) * B - 1;
for (int i = l; i <= r; ++i)
b[i] = cov[x];
cov[x] = 0;
return ;
}
void update(int l, int r, int x) {
int pl = l / B, pr = r / B;

for (int i = pl; i <= pr; ++i)
down(i, x);
if (pl == pr) {
brute(pl);
for (int i = l; i <= r; ++i)
b[i] = x;
build(pl, l, r);
return ;
}
brute(pl), brute(pr);
for (int i = l; i < (pl + 1)*B; ++i)
b[i] = x;
for (int i = pr * B; i <= r; ++i)
b[i] = x;
build(pl, l, (pl + 1)*B), build(pr, pr * B, r);
for (int i = pl + 1; i < pr; ++i)
cov[i] = x;
}
void flush(int l, int r) {
int pl = l / B, pr = r / B;
if (pl == pr) {
if (cov[pl])
T.add(cov[pl], 1ll * (r - l + 1)*a[cov[pl]].x);
else
for (int i = l; i <= r; ++i)
T.add(b[i], a[b[i]].x);
return ;
}
if (cov[pl])
T.add(cov[pl], 1ll * ((pl + 1)*B - l)*a[cov[pl]].x);
else
for (int i = l; i < (pl + 1)*B; ++i)
T.add(b[i], a[b[i]].x);
for (int i = pl + 1; i < pr; ++i)
++tag[i];
if (cov[pr])
T.add(cov[pr], 1ll * (r - pr * B + 1)*a[cov[pr]].x);
else
for (int i = pr * B; i <= r; ++i)
T.add(b[i], a[b[i]].x);
return ;

}
signed main() {
int n = read(), m = read(), q = read();
for (int i = 1; i <= m; ++i) {
a[i].op = read(), a[i].l = read(), a[i].r = read();
if (a[i].op == 1)
a[i].x = read();
}
for (int i = 1, l, r; i <= q; ++i)
l = read(), r = read(), v[r].push_back({l, i});
for (int i = 0; i <= n / B; ++i) {
for (int j = 1; j <= B; ++j)
pos[i][ j] = i * B + j - 1;
build(i, 1, 0);
}
for (int i = 1; i <= m; ++i) {
if (a[i].op == 1)
update(a[i].l, a[i].r, i);
else
flush(a[i].l, a[i].r);
for (auto [l, p] : v[i])
ans[p] += T.query(l - 1);
}
for (int i = 0; i <= n / B; ++i)
down(i, m + 1);
for (int i = 1; i <= q; ++i)
printf("%lld\n", ans[i]);
return 0;
}


