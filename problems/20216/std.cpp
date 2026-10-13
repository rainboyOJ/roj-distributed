#include <bits/stdc++.h>
#pragma GCC optimize("Ofast")
#define ffor(i, l, r) for (register int i = (l), i##_end = (r); i <= i##_end; i++)
#define rfor(i, l, r) for (register int i = (l), i##_end = (r); i >= i##_end; i--)
#define file(name, dat) freopen(name ".in", "r", stdin), freopen(name dat, "w", stdout)
using namespace std;
using ll = long long;
const int INF = 1e9, N = 1e6 + 10;
#include <cstdio>
struct IO {
    static const int N = 1 << 22;
    char buf[N], pbuf[N], *p1 = buf, *p2 = buf, *pp = pbuf;
#define gc() (p1 == p2 && (p2 = (p1 = buf) + fread(buf, 1, N, stdin), p1 == p2) ? EOF : *p1++)
    template <typename T>
    void read(T& x) {
        x = 0;
        char ch;
        int f = 0;
        while ((ch = gc()) < '0' || ch > '9') f |= (ch == '-');
        while (x = (x << 1) + (x << 3) + (ch ^ 48), (ch = gc()) >= '0' && ch <= '9')
            ;
        if (f)
            x = ~x + 1;
    }
    void putc(char c) {
        if (pp - pbuf == N)
            fwrite(pbuf, 1, N, stdout), pp = pbuf;
        *pp++ = c;
    }
    void puts(const char* s) {
        while (*s) putc(*s), ++s;
        putc('\n');
    }
    template <typename T>
    void print(T x) {
        static int st[20];
        int tp = 0;
        if (x < 0)
            putc('-'), x = ~x + 1;
        do
            st[++tp] = x % 10, x /= 10;
        while (x);
        while (tp) putc(st[tp--] + '0');
    }
    ~IO() { fwrite(pbuf, pp - pbuf, 1, stdout); }
} io;

template <typename T>
struct Queue {
    T d[N], l, r;
    inline Queue() { l = 0, r = -1; }
    inline void push(int x) { d[++r] = x; }
    inline T size() { return r - l + 1; }
    inline T front() { return d[l]; }
    inline void pop() { l++; }
    inline void clear() { l = 0, r = -1; }
};
int mem[4 * N], ms = 0;
struct Vector {
    int l, r;
    Vector() { l = ms, r = l - 1, ms += 4; }
    void push_back(int x) { mem[++r] = x; }
    inline int* begin() { return &mem[l]; }
    inline int* end() { return &mem[r + 1]; }
    inline void clear() { r = l - 1; }
};
int t;
int n, d, L, R, Q;
int dis[N];
Vector fro[N];
Queue<int> q;
int fa[N];
inline int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
inline int mod(int x) {
    while (x < 0) x += n;
    while (x >= n) x -= n;
    return x;
}
inline void upd(int l, int r, int c) {
    if (l > r)
        return upd(0, r, c), upd(l, n - 1, c);
    for (int i = find(l); i <= r; i = find(i)) {
        dis[i] = c;
        fa[i] = i + 1;
        q.push(i);
    }
}
inline void bfs() {
    q.clear();
    ffor(i, 0, n - 1) dis[i] = INF;
    upd(mod(0 - R), mod(0 - L), 0);
    while (q.size()) {
        int u = q.front();
        q.pop();
        for (int v : fro[u]) {
            upd(mod(v - R), mod(v - L), dis[u] + 1);
        }
    }
}
inline void Do() {
    io.read(n), io.read(d), io.read(L), io.read(R), io.read(Q);
    ffor(i, 0, n) fa[i] = i;
    ffor(i, 0, n - 1) fro[i].clear();
    d %= n;
    ffor(i, 0, n - 1) { fro[(1ll * i * d) % n].push_back(i); }
    bfs();
    while (Q--) {
        int xi, ans = INF;
        io.read(xi);
        ans = dis[xi];
        if (ans > n + 1)
            ans = -1;
        io.print(ans), io.putc('\n');
    }
}
int main() {
    ios::sync_with_stdio(false), cin.tie(0), cout.tie(0);
    file("calculate", ".out");
    io.read(t);
    while (t--) Do();
    return 0;
}