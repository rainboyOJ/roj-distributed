#include <bits/stdc++.h>
#define Pr pair<int,int>
#define fi first
#define nd second
using namespace std;
typedef long long LL;
Pr operator + (Pr A, Pr B) {
return {A.fi + B.fi, A.nd + B.nd};
}
Pr operator - (Pr A, Pr B) {
return {A.fi - B.fi, A.nd - B.nd};
}
inline int read() {
char ch = getchar();
while (!isdigit(ch) && ch != '-')
ch = getchar();
int x = 0, ff = 1;
if (ch == '-')
ff = -1, ch = getchar();
while (isdigit(ch))
x = (x << 3) + (x << 1) + (ch ^ 48), ch = getchar();
return x * ff;
}
const int N = 5e5 + 5;
int n, Q, c[N], el[N], hv[N], ld[N], rd[N], tot, b[N];
vector<int> e[N];
void dfs(int u) {
b[ld[u] = ++tot] = u;
if (c[u])
hv[u]++;
for (int v : e[u])
hv[v] = hv[u], dfs(v);
rd[u] = tot;
}
bool isf(int u) {
return !el[u] || c[u];
}
namespace SegT {
#define lc(p) p<<1
#define rc(p) p<<1|1
#define ls(p) lc(p),L,mid
#define rs(p) rc(p),mid+1,R
struct node {
int mn, mx, sf, pr, tg;
Pr sv;
void setz(int x) {

mx = tg;
sf = mx;
pr = -1;
if (isf(x))
mn = mx + (!c[x]), sv = {mx - mn, 1};
else
mn = -1;
}
void addt(int w) {
tg += w;
if (~mn)
mn += w, mx += w, sf += w, pr += w;
}
} tr[N << 2];
void pushdn(int p) {
if (tr[p].tg) {
tr[lc(p)].addt(tr[p].tg);
tr[rc(p)].addt(tr[p].tg);
tr[p].tg = 0;
}
}
Pr ask(int p, int L, int R, int mx, int mn) {
if (!~tr[p].mn || tr[p].mx < mx)
return {0, 0};
if (tr[p].mn != mn || L == R)
return {tr[p].mx - mn, 1};
int mid = (L + R) / 2, l = lc(p), r = rc(p);
pushdn(p);
if (!~tr[l].mn || tr[l].mx < mx)
return ask(rs(p), mx, mn);
if (!~tr[r].mn)
return ask(ls(p), mx, mn);
Pr bf = (tr[l].mn > tr[r].mn) ? (Pr) {
tr[l].mx - tr[p].mn, 1
}:
tr[l].sv;
return tr[p].sv - bf + ask(ls(p), mx, mn);
}
void pushup(int p, int rl, int R) {
node l = tr[lc(p)], r = tr[rc(p)];
if (!~l.mn) {
tr[p] = r;
tr[p].tg = 0;
return ;
}

if (!~r.mn) {
tr[p] = l;
tr[p].tg = 0;
return ;
}
tr[p].mn = min(l.mn, r.mn);
tr[p].mx = max(l.mx, r.mx);
tr[p].sf = r.sf;
tr[p].pr = l.pr;
Pr lv = l.sv;
int lsv = l.sf, rpv = r.pr;
if (l.mn > r.mn)
tr[p].pr = max(l.mx, r.pr), lv = {l.mx - tr[p].mn, 1}, lsv = l.mx;
if (l.mn < r.mn)
tr[p].sf = max(l.sf, r.mx), rpv = r.mx;
tr[p].sv = lv + ask(rc(p), rl, R, l.mx, tr[p].mn);
if (lsv == l.mx && lsv <= rpv)
tr[p].sv = tr[p].sv - (Pr) {
lsv - tr[p].mn, 1
};
}
void build(int p, int L, int R) {
if (L == R) {
tr[p].tg = hv[b[L]];
tr[p].setz(b[L]);
return ;
}
int mid = (L + R) / 2;
build(ls(p));
build(rs(p));
pushup(p, mid + 1, R);
}
void Madd(int p, int L, int R, int lt, int rt, int w) {
if (L > rt || R < lt)
return ;
if (L >= lt && R <= rt) {
tr[p].addt(w);
return ;
}
int mid = (L + R) / 2;
pushdn(p);
Madd(ls(p), lt, rt, w);
Madd(rs(p), lt, rt, w);
pushup(p, mid + 1, R);
}
void Mset(int p, int L, int R, int kx) {
if (L == R) {

tr[p].setz(b[L]);
return ;
}
int mid = (L + R) / 2;
pushdn(p);
(kx <= mid) ? Mset(ls(p), kx) : Mset(rs(p), kx);
pushup(p, mid + 1, R);
}
int mxv, mnv, sfv;
Pr Qry(int p, int L, int R, int lt, int rt) {
if (L > rt || R < lt || !~tr[p].mn)
return {0, 0};
if (p == 1)
mxv = 0, mnv = -1, sfv = -1;
if (L >= lt && R <= rt) {
if (!~mnv)
mnv = tr[p].mn;
Pr res = ask(p, L, R, mxv, mnv);
int rpv = tr[p].pr;
if (tr[p].mn != mnv)
rpv = tr[p].mx;
if (sfv == mxv && rpv >= sfv)
res = res - (Pr) {
mxv - mnv, 1
};
mxv = max(mxv, tr[p].mx);
sfv = (tr[p].mn != mnv) ? max(sfv, tr[p].mx) : tr[p].sf;
return res;
}
int mid = (L + R) / 2;
Pr s;
pushdn(p);
s = Qry(ls(p), lt, rt);
return s + Qry(rs(p), lt, rt);
}
int Qcnt(int p, int L, int R, int lt, int rt) {
if (p == 1)
mxv = 0;
if (mxv || !~tr[p].mn || L > rt || R < lt)
return 0;
if (L >= lt && R <= rt) {
if (tr[p].mn > tr[p].mx)
return tr[p].sv.nd;

if (L == R) {
mxv = 1;
return 0;
}
}
int mid = (L + R) / 2, s;
pushdn(p);
s = Qcnt(ls(p), lt, rt);
return s + Qcnt(rs(p), lt, rt);
}
} using namespace SegT;
int main() {
freopen("sleep.in", "r", stdin);
freopen("sleep.out", "w", stdout);
n = read();
Q = read();
for (int i = 1; i <= n; i++) {
c[i] = read();
el[i] = read();
e[i].resize(el[i]);
for (int j = 0; j < el[i]; j++)
e[i][ j] = read();
}
dfs(1);
build(1, 1, n);
while (Q--) {
int o = read() - 1, x = read();
if (!o)
c[x] ^= 1, Madd(1, 1, n, ld[x], rd[x], c[x] ? 1 : -1), Mset(1, 1, n, ld[x]);
else {
Pr res = Qry(1, 1, n, ld[x], rd[x]);
printf("%d\n", res.fi + Qcnt(1, 1, n, ld[x], rd[x]) + res.nd + (res.nd > 1));
}
}
return 0;
}


