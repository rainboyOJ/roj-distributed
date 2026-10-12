#include <bits/stdc++.h>
using namespace std;
const int MOD = 1000000007;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<int> a(m), b(m);
    for (int i = 0; i < m; ++i) cin >> a[i];
    for (int i = 0; i < m; ++i) cin >> b[i];
    vector<int> pos(m + 1, -1);
    for (int i = 0; i < m; ++i) pos[b[i]] = i;
    vector<int> seg;
    int i = 0, L = 0;
    bool ok = true;
    while (i < m) {
        int p = pos[a[i]];
        int r = p - L + 1;
        if (r <= 0 || i + r > m) { ok = false; break; }
        for (int t = 0; t < r; ++t) {
            if (a[i + t] != b[p - t]) { ok = false; break; }
        }
        if (!ok) break;
        seg.push_back(r);
        i += r;
        L += r;
    }
    if (!ok) { cout << 0 << '\n'; return 0; }
    if ((int)seg.size() > n) { cout << 0 << '\n'; return 0; }
    for (int r : seg) if (r > n) { cout << 0 << '\n'; return 0; }
    vector<vector<int>> C(n + 1, vector<int>(n + 1, 0));
    for (int x = 0; x <= n; ++x) {
        C[x][0] = 1;
        C[x][x] = 1;
        for (int y = 1; y < x; ++y) {
            C[x][y] = C[x - 1][y - 1] + C[x - 1][y];
            if (C[x][y] >= MOD) C[x][y] -= MOD;
        }
    }
    long long ans = C[n][(int)seg.size()];
    for (int r : seg) ans = ans * C[n][r] % MOD;
    cout << ans << '\n';
    return 0;
}