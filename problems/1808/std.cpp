// ============================================================================
// 一本通 1808 《斐波那契数列》
// 题目：给定 a (0<=a<10^13)，求最小的 n>=0 使 F_n ≡ a (mod 10^13)，
//       不存在输出 -1。（F 为模 10^13 意义下的斐波那契数列，F_0=0,F_1=1）
//
// 来源说明：本题在博客园 / CSDN / 搜索引擎（Bing/Sogou/360/DDG 多轮检索，
//   含题面特征句精确搜索）均未检索到公开题解或同源代码，故按题目自身数学
//   结构自研本解法。参考数学依据（公开经典结论）：
//     - Pisano 周期：pi(2^k)=3*2^(k-1)(k>=3)，pi(5^k)=20*5^(k-1)，
//       pi(10^13)=lcm(12288, 4882812500)=15*10^12。
//     - Fibonacci Q-矩阵 M=[[1,1],[1,0]] 的阶 = Pisano 周期，
//       M^n=[[F_{n+1},F_n],[F_n,F_{n-1}]]。
//
// 算法（CRT 分解 10^13 = 2^13 * 5^13）：
//   (1) mod 2^13：周期 12288，直接枚举 n∈[0,12288) 求所有满足 F_n≡a 的
//       n mod 12288，得到解集 A。
//   (2) mod 5^13：周期 Q=4882812500。由 F_n=a 及 F_{n+1}=b 有
//       b(b-a)-a^2 = (-1)^n，即 (2b-a)^2 = 5a^2 + 4(-1)^n (mod 5^13)。
//       对两种奇偶性各解一个平方根（Hensel 提升，C 恒为 5 的幂次单位，
//       必为二次剩余），得候选矩阵 T=[[b,a],[a,b-a]]；再对每个候选 T 用
//       BSGS（m=ceil(sqrt(Q))≈69878）求最小 n 使 M^n=T，得到解集 B。
//   (3) 合并：n 需同时满足 n mod 12288 ∈ A 与 n mod Q ∈ B。gcd(12288,Q)=4，
//       对每对兼容 (r,s) 做 CRT 得模 P=15*10^12 下唯一类，取最小非负 n。
// ============================================================================
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstdint>
#include <vector>
#include <iostream>
#include <unordered_map>
using namespace std;
typedef long long ll;
typedef unsigned __int128 u128;

static const ll P2     = 8192LL;            // 2^13
static const ll MOD2P  = 12288LL;           // pi(2^13) = 3*2^12
static const ll P5     = 1220703125LL;      // 5^13
static const ll Q5     = 4882812500LL;      // pi(5^13) = 20*5^12
static const ll MOD10  = 10000000000000LL;  // 10^13

// ---- 模逆（extended Euclid，要求 gcd(a,m)=1）----
static ll inv_mod(ll a, ll m) {
    a %= m; if (a < 0) a += m;
    ll r0 = m, r1 = a, s0 = 0, s1 = 1;
    while (r1) {
        ll q = r0 / r1;
        ll r2 = r0 - q * r1; r0 = r1; r1 = r2;
        ll s2 = s0 - q * s1; s0 = s1; s1 = s2;
    }
    s0 %= m; if (s0 < 0) s0 += m;
    return s0;
}

// ---- 模 5^k 下的单位平方根（Hensel 提升），返回 [0,5^k) 内一根，无解 -1 ----
static ll sqrt5pow(ll c, int k) {
    ll c5 = c % 5;
    ll s;
    if (c5 == 1) s = 1; else if (c5 == 4) s = 2; else return -1;
    ll mod = 5;
    for (int e = 1; e < k; e++) {
        ll M = mod * 5;
        ll ss = s * s;                               // < 5^24 < 2^63
        ll diff = ((ss - c) % M + M) % M;
        ll delta = diff / mod;                       // in [0,5)
        ll inv2s = inv_mod((2 * (s % 5)) % 5, 5);
        ll t = ((5 - delta % 5) % 5) * inv2s % 5;
        s = s + t * mod;
        mod = M;
    }
    return s % mod;
}

// ---- 2x2 矩阵，模 P5 ----
struct Mat { ll a, b, c, d; };
static Mat mul(const Mat &x, const Mat &y) {
    Mat z;
    z.a = (x.a * y.a + x.b * y.c) % P5;
    z.b = (x.a * y.b + x.b * y.d) % P5;
    z.c = (x.c * y.a + x.d * y.c) % P5;
    z.d = (x.c * y.b + x.d * y.d) % P5;
    return z;
}
static Mat matpow(Mat base, ll e) {
    Mat r{1, 0, 0, 1};
    while (e) { if (e & 1) r = mul(r, base); base = mul(base, base); e >>= 1; }
    return r;
}
static u128 packm(const Mat &x) {
    u128 k = (u128)x.a;
    k = (k << 31) | (u128)x.b;
    k = (k << 31) | (u128)x.c;
    k = (k << 31) | (u128)x.d;
    return k;
}
struct HashU128 {
    size_t operator()(u128 x) const {
        return (size_t)(x ^ (x >> 64)) * 0x9e3779b97f4a7c15ULL;
    }
};

// ---- BSGS: 求最小 n∈[0,Q5) 使 M^n = T，不存在返回 -1 ----
static ll bsgs_one(const Mat &T) {
    ll m = (ll)sqrtl((long double)Q5);
    while (m * m < Q5) m++;
    while (m > 1 && (m - 1) * (m - 1) >= Q5) m--;
    Mat Minv{0, 1, 1, (P5 - 1) % P5};   // M^{-1} = [[0,1],[1,-1]]
    unordered_map<u128, ll, HashU128> baby;
    baby.reserve((size_t)m * 2);
    Mat cur = T;
    for (ll j = 0; j < m; j++) {
        u128 k = packm(cur);
        auto it = baby.find(k);
        if (it == baby.end()) baby.emplace(k, j);
        cur = mul(cur, Minv);
    }
    Mat M{1, 1, 1, 0};
    Mat G = matpow(M, m);
    Mat gi{1, 0, 0, 1};
    for (ll i = 0; i <= m; i++) {
        auto it = baby.find(packm(gi));
        if (it != baby.end()) {
            ll n = i * m + it->second;
            if (n < Q5) return n;
        }
        gi = mul(gi, G);
    }
    return -1;
}

int main() {
    ll a;
    if (!(cin >> a)) return 0;

    // (1) mod 2^13
    vector<ll> A;
    {
        ll am = a % P2;
        ll fprev = 1, fcur = 0;            // F_{-1}=1, F_0=0
        for (ll n = 0; n < MOD2P; n++) {
            if (fcur == am) A.push_back(n);
            ll nxt = (fcur + fprev) % P2;
            fprev = fcur; fcur = nxt;
        }
    }

    // (2) mod 5^13
    vector<ll> B;
    {
        ll a5 = a % P5;
        ll a2 = (a5 * a5) % P5;
        ll inv2 = inv_mod(2, P5);
        for (int eps = 0; eps < 2; eps++) {
            ll C = (5 * a2 % P5 + (eps == 0 ? 4 : (P5 - 4))) % P5;
            ll s = sqrt5pow(C, 13);
            if (s < 0) continue;
            for (int r = 0; r < 2; r++) {
                ll ss = (r == 0) ? s : (P5 - s) % P5;
                ll b = ((a5 + ss) % P5) * inv2 % P5;
                Mat T;
                T.a = b; T.b = a5; T.c = a5;
                T.d = ((b - a5) % P5 + P5) % P5;
                ll n = bsgs_one(T);
                if (n >= 0) B.push_back(n);
            }
        }
    }

    if (A.empty() || B.empty()) { cout << -1 << "\n"; return 0; }

    // (3) CRT 合并
    const ll g = 4;
    ll m1p = MOD2P / g, m2p = Q5 / g;                 // 3072, 1220703125
    ll inv = inv_mod(m1p % m2p, m2p);
    ll best = -1;
    for (ll r : A) for (ll s : B) {
        if (((s - r) % g + g) % g != 0) continue;
        ll diff = ((s - r) % Q5 + Q5) % Q5;           // 可被 g 整除
        ll t = (diff / g) % m2p * inv % m2p;
        ll n = r + MOD2P * t;                         // < P = 15*10^12
        if (best < 0 || n < best) best = n;
    }
    cout << best << "\n";
    return 0;
}
