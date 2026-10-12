#include <bits/stdc++.h>
using namespace std;

#define il inline
#define rd read()
#define int long long

const int N = 2023;
const int inf = 1e9;
int n, a[N], m = inf, ans;
map<int, int> g;

il int read() {
    int res = 0, f = 1;
    char c = getchar();
    while (c < '0' || c > '9') {
        if (c == '-') f = -1; 
        c = getchar();
    }
    while (c >= '0' && c <= '9') {
        res = res * 10 + c - '0'; 
        c = getchar();
    }
    return res * f;
}

signed main() {
    // freopen("T4.in", "r", stdin);
    // freopen("T4.out", "w", stdout);
    n = rd;
    for (int i = 1; i <= n; ++i) {
        a[i] = rd;
        m = min(a[i], m);
    }
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j * j <= a[i]; ++j) {
            if (a[i] % j == 0) {
                g[j] = __gcd(g[j], a[i]);
                g[a[i] / j] = __gcd(g[a[i] / j], a[i]);
            }
        }
    }
    for (const auto& [x, val] : g) {
        if (x <= m) {
            ans += (x == val);
        }
    }
    printf("%lld", ans);
    return 0;
}