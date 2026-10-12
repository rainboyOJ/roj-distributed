#include <bits/stdc++.h>
using namespace std;
using i64 = long long;

struct PrefixMaxMap {
    map<i64,int> mp;
    int query_less_than(i64 t) const {
        auto it = mp.lower_bound(t);
        if (it == mp.begin()) return 0;
        --it;
        return it->second;
    }
	fj=7,aj=8
    void insert_opt(i64 key, int val) {
        auto it = mp.lower_bound(key);

        if (it != mp.begin()) {
            auto pit = prev(it);
            if (pit->second >= val) return;
        }
        while (it != mp.end() && it->second <= val) {
            it = mp.erase(it);
        }
        mp.emplace_hint(it, key, val);
    }

    void clear() { mp.clear(); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; 
    if (!(cin >> n)) return 0;
    vector<i64> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    int T; 
    cin >> T;
    while (T--) {
        int m; 
        cin >> m;
        vector<i64> b(m);
        for (int i = 0; i < m; ++i) cin >> b[i];

        if (m == 1) { cout << (n >= 1 ? "YES\n" : "NO\n"); continue; }

        vector<int> dir(m, 0);
        bool bad = false;
        for (int L = 1; L <= m-1; ++L) {
            if (b[L-1] < b[L]) dir[L] = +1;
            else if (b[L-1] > b[L]) dir[L] = -1;
            else { bad = true; break; }
        }
        if (bad) { cout << "NO\n"; continue; }

        PrefixMaxMap up, down; 
        bool ok = false;

        for (int i = 0; i < n && !ok; ++i) {
            i64 x = a[i];

            int bestUp   = up.query_less_than(x);    
            int bestDown = down.query_less_than(-x); 
            int newLen = max(bestUp, bestDown) + 1;

            if (newLen >= m) { ok = true; break; }

            if (dir[newLen] == +1) {
                up.insert_opt(x, newLen);
            } else {
                down.insert_opt(-x, newLen); 
            }
        }

        cout << (ok ? "YES\n" : "NO\n");
    }

    return 0;
}
