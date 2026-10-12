#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

inline int64 ones_from_len(int64 x) {
    if (x == 2) return 2;
    if (x == 3) return 3;
    if (x & 1)  return 1;   // 奇数 ≥5
    return 0;               // 偶数 ≥4
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int64> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    int64 init_ones = 0;
    int64 sum_all = 0;
    for (int i = 0; i < n; ++i) {
        sum_all += a[i];
        if (a[i] == 1) ++init_ones;
    }

    int m;
    cin >> m;
    vector<int64> k(m);
    for (int i = 0; i < m; ++i) cin >> k[i];

    for (int i = 0; i < m; ++i) {
        assert(k[i] <= sum_all); 
    }

    unordered_map<int64, int64> cnt;
    cnt.reserve(static_cast<size_t>(n) * 32);
    for (int64 x : a) {
        for (int d = 0; (x >> d) >= 2; ++d) {
            int64 len = x >> d;       
            cnt[len] += 1LL << d;     
        }
    }

    vector<pair<int64,int64>> vec;
    vec.reserve(cnt.size());
    for (auto &kv : cnt) vec.emplace_back(kv.first, kv.second);
    sort(vec.begin(), vec.end(),
         [](const pair<int64,int64>& p1, const pair<int64,int64>& p2){
             return p1.first > p2.first;
         });

    size_t sz = vec.size();
    vector<int64> pref_proc(sz), pref_one(sz);
    int64 proc = 0, ones = 0;
    for (size_t i = 0; i < sz; ++i) {
        int64 len  = vec[i].first;
        int64 c    = vec[i].second;
        int64 add1 = c * ones_from_len(len);
        proc += c;
        ones += add1;
        pref_proc[i] = proc;
        pref_one [i] = ones;
    }

    ostringstream out;
    for (int i = 0; i < m; ++i) {
        int64 need = k[i];

        if (need <= init_ones) {
            out << 0 << '\n';
            continue;
        }
        need -= init_ones; 

        size_t pos = lower_bound(pref_one.begin(), pref_one.end(), need) - pref_one.begin();

        if (pos == sz) {
            out << (sz ? pref_proc.back() : 0) << '\n';
            continue;
        }

        int64 len   = vec[pos].first;
        int64 g     = ones_from_len(len);  
        int64 prev1 = (pos ? pref_one [pos-1] : 0);
        int64 prevp = (pos ? pref_proc[pos-1] : 0);

        if (g == 0) {
            size_t q = pos;
            while (q < sz && ones_from_len(vec[q].first) == 0) ++q;
            if (q == sz) { 
                out << pref_proc.back() << '\n';
                continue;
            }
            int64 g2 = ones_from_len(vec[q].first);
            int64 prev1b = (q ? pref_one [q-1] : 0);
            int64 prevpb = (q ? pref_proc[q-1] : 0);
            int64 t2 = (need - prev1b + g2 - 1) / g2;
            out << (prevpb + t2) << '\n';
            continue;
        }

        int64 t = (need - prev1 + g - 1) / g; 
        int64 ans = prevp + t;
        out << ans << '\n';
    }

    cout << out.str();
    return 0;
}
