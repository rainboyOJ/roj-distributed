#include <bits/stdc++.h>
using namespace std;

struct Seg {
    int n;
    vector<long long> t;
    void build(const vector<long long>& a) {
        n = (int)a.size() - 1;
        t.assign(4 * n + 4, 0);
        build(1, 1, n, a);
    }
    void build(int p, int l, int r, const vector<long long>& a) {
        if (l == r) { t[p] = a[l]; return; }
        int m = (l + r) >> 1;
        build(p << 1, l, m, a);
        build(p << 1 | 1, m + 1, r, a);
        t[p] = llabs(t[p << 1] - t[p << 1 | 1]);
    }
    void add(int L, int R, long long v) { add(1, 1, n, L, R, v); }
    void add(int p, int l, int r, int L, int R, long long v) {
        if (R < l || r < L) return;
        if (L <= l && r <= R) { if (l == r) t[p] += v; return; }
        int m = (l + r) >> 1;
        add(p << 1, l, m, L, R, v);
        add(p << 1 | 1, m + 1, r, L, R, v);
        t[p] = llabs(t[p << 1] - t[p << 1 | 1]);
    }
    long long root() const { return t[1]; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    int N = 1 << n;
    vector<long long> a(N + 1);
    for (int i = 1; i <= N; ++i) cin >> a[i];

    vector<Seg> blk(n);
    for (int k = 0; k < n; ++k) {
        int L = (1 << k) + 1, R = (1 << (k + 1));
        vector<long long> sub(R - L + 2);
        for (int i = L; i <= R; ++i) sub[i - L + 1] = a[i];
        blk[k].build(sub);
    }
    long long val1 = a[1];

    while (q--) {
        int l, r;
        long long x;
        cin >> l >> r >> x;
        if (l <= 1 && 1 <= r) val1 += x;
        for (int k = 0; k < n; ++k) {
            int L = (1 << k) + 1, R = (1 << (k + 1));
            int gl = max(l, L), gr = min(r, R);
            if (gl <= gr) {
                int ql = gl - L + 1, qr = gr - L + 1;
                blk[k].add(ql, qr, x);
            }
        }
        long long C = val1, need = 0;
        for (int k = 0; k < n; ++k) {
            long long V = blk[k].root();
            need = max(need, V - C);
            C -= V;
        }
        if (need < 0) need = 0;
        cout << need << '\n';
    }
    return 0;
}
