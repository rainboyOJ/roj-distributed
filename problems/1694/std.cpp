// 一本通 1694 回文串
//
// 记 A_x 为 A 的第 x 长后缀（长度 n-x+1），B_y 为 B 的第 y 长前缀（长度 m-y+1）。
// 对询问 (x,y)，设
//   st = x-1                 （A_x 在 A 中的起始下标，0-based）
//   yst = y-1                （B_y 反转后在 rev(B) 中的起始下标）
//   L  = m-y+1               （B_y 的长度）
//   P  = LCP(A[st..], rev(B)[yst..])
//
// S 取 A_x 的非空前缀，T 取 B_y 的非空后缀，S+T 回文。
// 按 |S|,|T| 大小分两类：
//   |S|<=|T| : 匹配部分要求 |S|<=P；中间（T 去掉末尾 |S| 个字符）须回文，
//              其末尾位置 e=L-|S|。故对每个 p=1..P 有 cntB[e]+1 种 q。
//   |S|> |T| : 匹配部分要求 |T|<=P；中间（S 去掉开头 |T| 个字符）须回文，
//              即 A[st+|T|..] 的回文前缀个数。故对 q=1..P 有 fA[st+q] 种 p。
//
// 于是 ans = sum_{e=L-P}^{L-1}(cntB[e]+1) + sum_{q=1}^{P} fA[st+q]
//          = (PG[L]-PG[L-P]) + (PF[x+P]-PF[x])
// 其中 cntB[e] = B[1..e] 的回文后缀个数，fA[i] = A[i..] 的回文前缀个数。

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <utility>
#include <iostream>
using namespace std;

typedef long long ll;

// ---------- Manacher ----------
static void manacher(const string &s, vector<int> &d1, vector<int> &d2) {
    int n = (int)s.size();
    d1.assign(n, 0);
    d2.assign(n, 0);
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
        while (i - k >= 0 && i + k < n && s[i - k] == s[i + k]) k++;
        d1[i] = k;
        if (i + k - 1 > r) { l = i - k + 1; r = i + k - 1; }
    }
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
        while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k]) k++;
        d2[i] = k;
        if (i + k - 1 > r) { l = i - k; r = i + k - 1; }
    }
}

// fA[i] (1-based, i=1..n): A[i..] 的非空回文前缀个数
static vector<ll> countStart(const string &s) {
    int n = (int)s.size();
    vector<int> d1, d2;
    manacher(s, d1, d2);
    vector<ll> diff(n + 2, 0);
    // 差分数组下标使用 1-based 起始位置
    for (int i = 0; i < n; i++) {
        // 奇回文：起始 1-based 在 [i-d1[i]+2, i+1]
        int lo = i - d1[i] + 2, hi = i + 1;
        diff[lo] += 1; diff[hi + 1] -= 1;
        // 偶回文：起始 1-based 在 [i-d2[i]+1, i]
        if (d2[i] > 0) {
            lo = i - d2[i] + 1; hi = i;
            diff[lo] += 1; diff[hi + 1] -= 1;
        }
    }
    vector<ll> f(n + 2, 0);
    ll cur = 0;
    for (int i = 1; i <= n; i++) { cur += diff[i]; f[i] = cur; }
    return f; // f[1..n]
}

// cntB[e] (1-based, e=0..m): B[1..e] 的非空回文后缀个数（cntB[0]=0）
static vector<ll> countEnd(const string &s) {
    int n = (int)s.size();
    vector<int> d1, d2;
    manacher(s, d1, d2);
    vector<ll> diff(n + 2, 0);
    // 差分数组下标使用 1-based 结束位置
    for (int i = 0; i < n; i++) {
        // 奇回文：结束 1-based 在 [i+1, i+d1[i]]
        int lo = i + 1, hi = i + d1[i];
        diff[lo] += 1; diff[hi + 1] -= 1;
        // 偶回文：结束 1-based 在 [i+1, i+d2[i]]
        if (d2[i] > 0) {
            lo = i + 1; hi = i + d2[i];
            diff[lo] += 1; diff[hi + 1] -= 1;
        }
    }
    vector<ll> c(n + 2, 0);
    ll cur = 0;
    for (int i = 1; i <= n; i++) { cur += diff[i]; c[i] = cur; }
    return c; // c[0]=0, c[1..n]
}

// ---------- 双模哈希 ----------
static const ll MOD1 = 1000000007LL;
static const ll MOD2 = 1000000009LL;

struct Hasher {
    int n;
    ll b1, b2;
    vector<ll> h1, h2, p1, p2;
    Hasher() {}
    Hasher(const string &s, ll base1, ll base2) { build(s, base1, base2); }
    void build(const string &s, ll base1, ll base2) {
        n = (int)s.size();
        b1 = base1; b2 = base2;
        h1.assign(n + 1, 0); h2.assign(n + 1, 0);
        p1.assign(n + 1, 1); p2.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            ll v = (unsigned char)s[i];
            h1[i + 1] = (h1[i] * b1 + v) % MOD1;
            h2[i + 1] = (h2[i] * b2 + v) % MOD2;
            p1[i + 1] = p1[i] * b1 % MOD1;
            p2[i + 1] = p2[i] * b2 % MOD2;
        }
    }
    // [l, r] 0-based
    pair<ll, ll> get(int l, int r) const {
        ll a = (h1[r + 1] - h1[l] * p1[r - l + 1]) % MOD1; if (a < 0) a += MOD1;
        ll b = (h2[r + 1] - h2[l] * p2[r - l + 1]) % MOD2; if (b < 0) b += MOD2;
        return {a, b};
    }
};

int main() {
    // 输入重定向加速
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string dtype;
    if (!(cin >> dtype)) return 0; // 数据类型，忽略
    string A, B;
    cin >> A >> B;
    int n = (int)A.size(), m = (int)B.size();

    vector<ll> fA = countStart(A);          // fA[1..n]
    vector<ll> cntB = countEnd(B);         // cntB[0..m]

    // prefixF[i] = sum_{j=1}^{i} fA[j]；额外留 fA[n+1]=0 以支持 x+P=n+1
    vector<ll> prefixF(n + 2, 0);
    for (int i = 1; i <= n; i++) prefixF[i] = prefixF[i - 1] + fA[i];
    prefixF[n + 1] = prefixF[n];

    // g[e] = cntB[e] + 1, e=0..m；PG[k] = sum_{e=0}^{k-1} g[e]
    vector<ll> PG(m + 2, 0);
    for (int e = 0; e <= m; e++) PG[e + 1] = PG[e] + (cntB[e] + 1);

    // 哈希：A 与 rev(B)
    string Brev(B.rbegin(), B.rend());
    // 随机 base，降低被卡风险
    unsigned long long seed = chrono::steady_clock::now().time_since_epoch().count();
    mt19937_64 rng(seed);
    ll base1 = 131 + (ll)(rng() % 1000);
    ll base2 = 13331 + (ll)(rng() % 1000);
    Hasher ha(A, base1, base2);
    Hasher hb(Brev, base1, base2);

    int Q;
    cin >> Q;
    string out;
    out.reserve((size_t)Q * 16);
    while (Q--) {
        int x, y;
        cin >> x >> y;
        int st = x - 1;          // A 起始 0-based
        int yst = y - 1;         // rev(B) 起始 0-based
        int L = m - y + 1;       // B_y 长度
        int maxlen = min(n - st, m - yst);

        // 二分 LCP
        int lo = 0, hi = maxlen;
        while (lo < hi) {
            int mid = (lo + hi + 1) >> 1;
            if (ha.get(st, st + mid - 1) == hb.get(yst, yst + mid - 1)) lo = mid;
            else hi = mid - 1;
        }
        int P = lo;

        ll ans = (PG[L] - PG[L - P]) + (prefixF[x + P] - prefixF[x]);
        out += to_string(ans);
        out += '\n';
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
