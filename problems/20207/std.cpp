//
//  Created by mori
//
//  Coded with Visual Studio Code
//

#include <bits/stdc++.h>
using namespace std;

#define pii pair <int, int>
typedef vector <int> vci;
typedef long long ll;
typedef unsigned long long ull;
typedef __int128 lll;

#define rep(i, x, y) for (int i = (x); i <= (y); ++i)
#define per(i, x, y) for (int i = (x); i >= (y); --i)
#define cat const auto &
#define at auto &

template <typename T>
void ckmin (T &_0, T _1) { if (_1 < _0) _0 = _1; }

template <typename T>
void ckmax (T &_0, T _1) { if (_1 > _0) _0 = _1; }

int read () {
    int res = 0;
    bool f = false;
    char temp = getchar();
    for (; !isdigit(temp); temp = getchar()) f = temp == '-';
    for (; isdigit(temp); temp = getchar()) res = res * 10 + temp - '0';
    if (f) return -res;
    return res;
}

char gc () {
    char temp = getchar();
    while (temp == '\n' || temp == '\r' || temp == ' ') temp = getchar();
    return temp;
}

struct MODER {
    ll p, m;
    explicit MODER (ll tmp) : p (tmp), m (((lll)1 << 63) / p) {}
    ll operator () (ll x) {
        ll q = ((lll) x * m) >> 63;
        x -= p * q;
        if (x >= p) x -= p;
        return x;
    }
};

const string myfile = "imbalance";
void file () {
    string in = myfile + ".in", out = myfile + ".out";
    freopen(in.c_str(), "r", stdin); freopen(out.c_str(), "w", stdout);
}

constexpr int maxn = 2e6 + 5;
vci e[maxn], e1[maxn], e2[maxn];
bool vis[maxn];
int n;
ll ans;

int s[maxn];
int fd (int x) { return s[x] ? s[x] = fd(s[x]) : x; }

namespace BIT {
    int tr[maxn];
    #define lb(x) ((x)&(-x))
    void add (int x, int y) {
        for (int i = x; i <= n; i += lb(i)) tr[i] += y;
    }
    int query (int l, int r) {
        --l; int res = 0;
        while (r > l) res += tr[r], r -= lb(r);
        while (l > r) res -= tr[l], l -= lb(l);
        return res;
    }
} using namespace BIT;

int dfn[maxn], cnt, siz[maxn];
void dfs1 (int u) {
    dfn[u] = ++cnt, siz[u] = 1;
    for (cat v : e1[u]) dfs1(v), siz[u] += siz[v];
}
void dfs2 (int u) {
    ans += query(dfn[u], dfn[u] + siz[u] - 1);
    add(dfn[u], 1);
    for (cat v : e2[u]) dfs2(v);
    add(dfn[u], -1);
}

signed main () {
    file();
    n = read();
    rep (i, 2, n) {
        int u = read(), v = read();
        e[u].emplace_back(v);
        e[v].emplace_back(u);
    }

    per (u, n, 1) {
        for (cat v : e[u]) if (vis[v])
            e1[u].emplace_back(fd(v)), s[fd(v)] = u;
        vis[u] = true;
    } dfs1(1);

    memset(vis, 0, sizeof vis);
    memset(s, 0, sizeof s);

    rep (u, 1, n) {
        for (cat v : e[u]) if (vis[v])
            e2[u].emplace_back(fd(v)), s[fd(v)] = u;
        vis[u] = true;
    } dfs2(n);

    printf("%lld\n", ans);
    return 0;
}