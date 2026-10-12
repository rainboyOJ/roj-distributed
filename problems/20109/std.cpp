#include<bits/stdc++.h> 

using namespace std;

const int K = 40;

const int KEK = 1 << 23;

long long memo[KEK + 228];

long long calc_dp(long long mask, vector<long long>& inside) {
    if (mask < KEK && memo[mask]) {
        return memo[mask];
    }
    int mx_bit = 63 - __builtin_clzll(mask);
    long long ans = calc_dp((mask ^ (1ll << mx_bit)) & (~inside[mx_bit]), inside) + 
    calc_dp(mask ^ (1ll << mx_bit), inside);
    if (mask < KEK)
        memo[mask] = ans;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    


    int n;
    cin >> n;
    vector<long long> A(n);
    for (int i = 0; i < n; ++i)
        cin >> A[i];
    long long total_and = (1ll << K) - 1;
    for (int i = 0; i < n; ++i)
        total_and &= A[i];
    for (int i = 0; i < n; ++i)
        A[i] ^= total_and;
    vector<long long> ands(K);
    for (long long x : A) {
        for (int i = 0; i < K; ++i) {
            if (x & (1ll << i)) {
                if (ands[i] != 0)
                    ands[i] &= x;
                else
                    ands[i] = x;
            }
        }
    }
    vector<long long> vals;
    for (int i = 0; i < K; ++i) {
        if (ands[i])
            vals.emplace_back(ands[i]);
    }
    sort(vals.begin(), vals.end());
    vals.resize(unique(vals.begin(), vals.end()) - vals.begin());
    int m = vals.size();
    vector<long long> inside(m);
    for (int i = 0; i < m; ++i) {
        for (int j = i + 1; j < m; ++j) {
            if ((vals[i] & vals[j]) == vals[i])
                inside[j] |= 1ll << i;
        }
    }
    memo[0] = 1;
    cout << calc_dp((1ll << m) - 1, inside) << '\n';
    return 0;
}

