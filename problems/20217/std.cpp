// QwQ
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
using namespace std;
#define fi first
#define se second
typedef pair<int, int> PII;
typedef long long LL;
typedef unsigned long long ull;
template <typename T>
void inline read(T& x) {
    x = 0;
    int f = 1;
    char ch;
    while ((ch = getchar()) > '9' || ch < '0')
        if (ch == '-')
            f = -1;
    while (ch >= '0' && ch <= '9') x = x * 10 + (ch ^ '0'), ch = getchar();
    x *= f;
};

const int N = 1e5 + 5, M = 2e4 + 5, mod = 998244353;

void add(int& x, int y) {
    x += y;
    if (x >= mod)
        x -= mod;
}

struct ques {
    int l, r, m, id;
} Q[N], Q1[N], Q2[N];

int n, q, v[M], w[M], mx = 500, s1[N], s2[N], f[M][505], g[M][505];

void solve(int l, int r, int ql, int qr) {
    if (ql > qr)
        return;
    if (l == r) {
        for (int i = ql; i <= qr; i++)
            if (Q[i].m >= w[Q[i].l])
                s1[Q[i].id] = v[Q[i].l], s2[Q[i].id] = 1;
        return;
    }
    int mid = (l + r) / 2;
    for (int j = 0; j <= mx; j++) f[mid][j] = 0, g[mid][j] = 1;
    for (int i = mid + 1; i <= r; i++)
        for (int j = 0; j <= mx; j++) {
            f[i][j] = f[i - 1][j], g[i][j] = g[i - 1][j];
            if (j < w[i])
                continue;
            if (f[i - 1][j - w[i]] + v[i] > f[i][j])
                g[i][j] = g[i - 1][j - w[i]];
            else if (f[i - 1][j - w[i]] + v[i] == f[i][j])
                add(g[i][j], g[i - 1][j - w[i]]);
            f[i][j] = max(f[i][j], f[i - 1][j - w[i]] + v[i]);
        }
    for (int j = 1; j <= mx; j++) f[mid][j] = -1e9, g[mid][j] = 0;
    f[mid][w[mid]] = v[mid], g[mid][w[mid]] = 1;
    for (int i = mid - 1; i >= l; i--)
        for (int j = 0; j <= mx; j++) {
            f[i][j] = f[i + 1][j], g[i][j] = g[i + 1][j];
            if (j < w[i])
                continue;
            if (f[i + 1][j - w[i]] + v[i] > f[i][j])
                g[i][j] = g[i + 1][j - w[i]];
            else if (f[i + 1][j - w[i]] + v[i] == f[i][j])
                add(g[i][j], g[i + 1][j - w[i]]);
            f[i][j] = max(f[i][j], f[i + 1][j - w[i]] + v[i]);
        }
    int t1 = 0, t2 = 0;
    for (int i = ql; i <= qr; i++)
        if (Q[i].r <= mid)
            Q1[++t1] = Q[i];
        else if (Q[i].l > mid)
            Q2[++t2] = Q[i];
        else {
            int r1 = 0, r2 = 0;
            for (int j = 0; j <= Q[i].m; j++) {
                if (f[Q[i].l][j] + f[Q[i].r][Q[i].m - j] > r1)
                    r2 = 1LL * g[Q[i].l][j] * g[Q[i].r][Q[i].m - j] % mod;
                else if (f[Q[i].l][j] + f[Q[i].r][Q[i].m - j] == r1)
                    r2 = (r2 + 1LL * g[Q[i].l][j] * g[Q[i].r][Q[i].m - j] % mod) % mod;
                r1 = max(r1, f[Q[i].l][j] + f[Q[i].r][Q[i].m - j]);
            }
            if (r1 <= 0)
                r2 = 0;
            s1[Q[i].id] = r1, s2[Q[i].id] = r2;
        }
    for (int i = 1; i <= t1; i++) Q[ql + i - 1] = Q1[i];
    for (int i = 1; i <= t2; i++) Q[ql + t1 + i - 1] = Q2[i];
    solve(l, mid, ql, ql + t1 - 1);
    solve(mid + 1, r, ql + t1, ql + t1 + t2 - 1);
}

int main() {
    freopen("knapsack.in", "r", stdin);
    freopen("knapsack.out", "w", stdout);
    read(n);
    for (int i = 1; i <= n; i++) read(v[i]), read(w[i]);
    read(q);
    for (int i = 1; i <= q; i++) {
        read(Q[i].l), read(Q[i].r), read(Q[i].m);
        Q[i].id = i;
    }
    solve(1, n, 1, q);
    for (int i = 1; i <= q; i++) printf("%d %d\n", s1[i], s2[i]);
    return (0 - 0);  // QwQ
}