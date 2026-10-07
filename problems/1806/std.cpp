/*
 * 一本通 1806 「计算器」  (信息学奥赛一本通 · 高手训练篇 · 六、数学基础)
 * 原题主页: https://ybt.ssoier.cn/problem_show.php?pid=1806
 * 镜像题面: http://acgo.xiaomawang.com/problemset/explanation/85204  (「一本通 6.4 例 6」计算器)
 * 题面来源判定: 本题为经典三合一计算器题 (与「SDOI2011 计算器 / 洛谷 P2485」同源，题面输出 "Math Error")，
 *              把原第 2 问 (线性同余 x*y≡z) 换成了组合数 C_z^y mod P。
 *
 * 算法 (三问分别):
 *   type 1: 快速幂            y^z mod P                    O(log z)
 *   type 2: 扩展 BSGS (exBSGS) y^x ≡ z (mod P) 的最小非负整数解, P 可合数
 *           模板参考: 洛谷 P4195 【模板】扩展 BSGS/exBSGS  https://www.luogu.com.cn/problem/P4195
 *   type 3: 扩展卢卡斯 (exLucas) C_z^y mod P, P 可合数
 *           模板参考: 洛谷 P4720 【模板】扩展卢卡斯定理/exLucas https://www.luogu.com.cn/problem/P4720
 *           题面保证: 若 P 非质数, P = ∏ p_i^{a_i} 时 p_i^{a_i} ≤ 1e5
 *                     -> exLucas 逐质数幂求 C mod p^a, 前缀积表 O(p^a) ≤ 1e5, 再 CRT 合并。
 *                     质数 P 且 P > 1e5 时退化为 Lucas + 逐位直接乘积 (数据按题面保证 pk≤1e5, 该分支仅作兜底)。
 *   P = 1 时三个问的答案均为 0 (std 内部防御性处理; 数据中未使用 P=1)。
 *
 * 编译: g++ -O2 -std=c++17 -o std std.cpp
 */
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef __int128 lll;

/* ---------------- 基础 ---------------- */
static inline ll qpow(ll a, ll b, ll m) {
    if (m == 1) return 0;
    a %= m; if (a < 0) a += m;
    ll r = 1 % m;
    while (b > 0) {
        if (b & 1) r = (ll)((lll)r * a % m);
        a = (ll)((lll)a * a % m);
        b >>= 1;
    }
    return r;
}

static ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (!b) { x = 1; y = 0; return a; }
    ll g = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return g;
}
// 逆元, 需 gcd(a,m)=1, m>=2
static ll inv_mod(ll a, ll m) {
    ll x, y; exgcd(a % m, m, x, y);
    return ((x % m) + m) % m;
}

/* ---------------- type 1 ---------------- */
static ll solve_pow(ll y, ll z, ll P) { return qpow(y, z, P); }

/* ---------------- type 2 : exBSGS, 返回最小非负 x, 无解返回 -1 ---------------- */
static ll exbsgs(ll a, ll b, ll p) {
    a %= p; b %= p;
    if (p == 1) return 0;            // 模 1 下 a^x ≡ z 恒成立, 最小 x = 0
    if (b == 1) return 0;            // a^0 = 1
    ll cnt = 0, d = 1;
    for (ll g = __gcd(a, p); g != 1; g = __gcd(a, p)) {
        if (b % g) return -1;
        b /= g; p /= g;
        d = (ll)((lll)d * (a / g) % p);
        cnt++;
        if (b == d) return cnt;
    }
    // 此时 gcd(a,p) = 1
    ll m = (ll)ceil(sqrt((double)p));
    unordered_map<ll, ll> mp;
    mp.reserve((size_t)m * 2 + 8);
    ll cur = b;
    for (ll i = 0; i <= m; i++) {
        mp[cur] = i;                 // 必须覆盖为最大 j (ord(a) 可能 < m, 值会重复)
        cur = (ll)((lll)cur * a % p);
    }
    ll base = qpow(a, m, p);
    cur = d;
    for (ll i = 1; i <= m; i++) {
        cur = (ll)((lll)cur * base % p);
        auto it = mp.find(cur);
        if (it != mp.end()) return i * m - it->second + cnt;
    }
    return -1;
}

/* ---------------- type 3 : exLucas ---------------- */
static const ll PK_LIMIT = 4000000;  // 前缀积表规模上限

// n! 去掉全部 p 因子后 mod pk, 使用前缀积表 pre[0..pk]
static ll fac_with_table(ll n, ll p, ll pk, const vector<ll> &pre) {
    ll res = 1;
    while (n > 0) {
        res = (ll)((lll)res * qpow(pre[pk], n / pk, pk) % pk);
        res = (ll)((lll)res * pre[n % pk] % pk);
        n /= p;
    }
    return res;
}
// n! 去掉全部 p 因子后 mod pk, 无表版本 (O(pk) 每次, 兜底)
static ll fac_no_table(ll n, ll p, ll pk) {
    if (n == 0) return 1;
    ll res = 1;
    for (ll i = 1; i <= pk; i++) if (i % p) res = (ll)((lll)res * i % pk);
    res = (ll)((lll)qpow(res, n / pk, pk) * 1 % pk);
    for (ll i = 1; i <= n % pk; i++) if (i % p) res = (ll)((lll)res * i % pk);
    return (ll)((lll)res * fac_no_table(n / p, p, pk) % pk);
}
// n! 中 p 的幂次
static ll cnt_p(ll n, ll p) { ll s = 0; while (n) { n /= p; s += n; } return s; }

// C(n,m) mod p^k
static ll C_mod_pk(ll n, ll m, ll p, ll pk) {
    if (m < 0 || m > n) return 0;
    ll e = cnt_p(n, p) - cnt_p(m, p) - cnt_p(n - m, p);
    if (e < 0) return 0;
    ll pe = qpow(p, e, pk);          // e >= a 时自动为 0
    ll f1, f2, f3;
    if (pk <= PK_LIMIT) {
        vector<ll> pre(pk + 1);
        pre[0] = 1 % pk;
        for (ll i = 1; i <= pk; i++) {
            ll v = (i % p == 0) ? 1 : i;
            pre[i] = (ll)((lll)pre[i - 1] * v % pk);
        }
        f1 = fac_with_table(n, p, pk, pre);
        f2 = fac_with_table(m, p, pk, pre);
        f3 = fac_with_table(n - m, p, pk, pre);
    } else {
        f1 = fac_no_table(n, p, pk);
        f2 = fac_no_table(m, p, pk);
        f3 = fac_no_table(n - m, p, pk);
    }
    ll res = (ll)((lll)pe * f1 % pk);
    res = (ll)((lll)res * inv_mod(f2, pk) % pk);
    res = (ll)((lll)res * inv_mod(f3, pk) % pk);
    return res;
}

// C(n,m) mod p (p 为质数), Lucas + 逐位直接乘积
static ll lucas_prime(ll n, ll m, ll p) {
    if (m < 0 || m > n) return 0;
    if (p == 1) return 0;
    ll res = 1;
    while (n || m) {
        ll a = n % p, b = m % p;
        if (b > a) return 0;
        ll bb = min(b, a - b);
        ll num = 1, den = 1;
        for (ll j = 1; j <= bb; j++) {
            num = (ll)((lll)num * ((a - bb + j) % p) % p);
            den = (ll)((lll)den * (j % p) % p);
        }
        res = (ll)((lll)res * num % p);
        if (den != 1) res = (ll)((lll)res * qpow(den, p - 2, p) % p);
        n /= p; m /= p;
    }
    return res;
}

static ll solve_comb(ll y, ll z, ll P) {   // C(z,y) mod P
    ll n = z, m = y;
    if (P == 1) return 0;
    if (m < 0 || m > n) return 0;
    if (m == 0 || m == n) return 1 % P;
    // 分解 P
    ll tmp = P;
    vector<pair<ll, ll>> fac;   // (p, p^a)
    for (ll d = 2; d * d <= tmp; d++) {
        if (tmp % d == 0) {
            ll pk = 1;
            while (tmp % d == 0) { tmp /= d; pk *= d; }
            fac.push_back(make_pair(d, pk));
        }
    }
    if (tmp > 1) fac.push_back(make_pair(tmp, tmp));
    if (fac.size() == 1 && fac[0].first == P) {  // P 为质数 (注意: p^a==P 时 P 不是质数)
        if (P <= PK_LIMIT) return C_mod_pk(n, m, P, P);
        return lucas_prime(n, m, P);
    }
    // CRT 合并
    ll x = 0, M = 1;
    for (size_t i = 0; i < fac.size(); i++) {
        ll p = fac[i].first, pk = fac[i].second;
        ll r = C_mod_pk(n, m, p, pk);
        ll t = (ll)((lll)((r - x) % pk + pk) % pk * inv_mod(M % pk, pk) % pk);
        x = x + M * t;
        M *= pk;
        x %= M;
    }
    return x;
}

/* ---------------- main ---------------- */
int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int N;
    if (!(cin >> N)) return 0;
    string out;
    out.reserve((size_t)N * 12);
    while (N--) {
        ll type, y, z, P;
        cin >> type >> y >> z >> P;
        if (type == 1) {
            out += to_string(solve_pow(y, z, P));
        } else if (type == 2) {
            ll r = exbsgs(y, z, P);
            if (r < 0) out += "Math Error";
            else out += to_string(r);
        } else {
            out += to_string(solve_comb(y, z, P));
        }
        out += '\n';
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
