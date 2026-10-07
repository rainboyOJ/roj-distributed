// 一本通 1813《图的计数》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 本题与 JZOJ 3085【NOIP2012模拟11.3】图的计数 同源（题面逐字一致：
// 「询问有多少个 N 个点，M 条边的有向图，从 1 号点到达 N 号点需要经过至少 N-1 条边。
//   该有向图中可以包含重边和自环。」）。
// 下列来源结论一致（均给出同一公式），本代码按公式自主改写（非盲抄）：
//  [1] https://blog.csdn.net/mr_wuyongcong/article/details/86611624
//      《jzoj3085-图的计数【组合数,数论】》——「1 到 n 的最短路长度为 n-1」；
//      链边固定 n-1 条；捷径边 C(n-1,2) 种，可加边类型 n^2 - C(n-1,2)；
//      余 m-n+1 条边隔板法；再乘 (n-2)!；组合数用逆元。
//  [2] https://blog.csdn.net/enjoy_pascal/article/details/86618651
//      《【JZOJ3085】图的计数》——题面与一本通 1813 逐字一致，结论同上（乘 (n-2)!）。
//  [3] https://blog.csdn.net/xuxiayang/article/details/86612775
//      《2019.01.23【NOIP提高组】模拟A&B组 JZOJ 3085 图的计数》——
//      「首先 n-1 条边是固定的，如果小于这个边数则无法满足要求直接输出 0」；
//      剩余边插板法 + 乘 (n-2)!，复杂度 O(M log M + N)。
//  [4] https://blog.csdn.net/weixin_30493321/article/details/95749033
//      《[数学] Jzoj P3085 图的计数》——代码给出
//      C(n^2 - C(n-1,2) - 1 + m - n + 1, m - n + 1) * (n-2)!。
// =============================================================================
//
// 结论推导（题面口径：1 -> n 的“需要经过的边数”= 最短路径长度；样例 n=2,m=2 -> 4 佐证）：
//   设 d(v) 为 1 到 v 的最短路。若 d(n) = n-1（n 个点的简单路最多 n-1 条边，故「至少 n-1」
//   在有解时即「恰好 n-1」），则最短路必经全部 n 个点，且距离 0..n-1 各恰出现一次，
//   于是顶点顺序 1 = u0 -> u1 -> ... -> u_{n-1} = n 被距离唯一确定。
//   该顺序合法 <=> (a) 每条 u_i -> u_{i+1} 至少 1 条（否则 d(u_{i+1}) 达不到 i+1）；
//                (b) 不存在 u_i -> u_j（j >= i+2，捷径边，会把 d(u_j) 压到 <= i+1）。
//   捷径边共 C(n-1,2) = (n-1)(n-2)/2 种；故允许边类型 A = n^2 - (n-1)(n-2)/2。
//   中间 n-2 个点可任意排列，乘 (n-2)!；固定顺序后，m 条边 = 链边各 >= 1 + 余下
//   k = m-n+1 条在 A 种类型中任取（可重复/重边），隔板法 = C(A + k - 1, k) = C(A+m-n, m-n+1)。
//   => ans = (n-2)! * C(A+m-n, m-n+1) mod 1e9+7。
//   样例核对：n=2,m=2 -> 0! * C(4+0, 1) = 4 ✓
//   m < n-1（n >= 2）无解 -> 0（[3] 明文；如 n=3,m=1、n=10000,m=9998）。
//   n = 1 特判：d(1,1)=0 = n-1 恒成立，1 个点的 m 条边只能全是自环 -> 唯一图 -> 1。
//
// 复杂度：O(n + m)（阶乘 + k 个因子逐项乘 + 一次快速幂求逆元），O(1) 空间；
// 顶格 n=10000, m=50000 实测 < 1 ms，题限 1000 ms / 256 MB（config.json）。

#include <cstdio>

typedef long long ll;

static const ll MOD = 1000000007LL;  // 1e9+7

// 快速幂（用于费马小定理求逆元）
static ll power(ll x, ll b) {
    ll ans = 1;
    x %= MOD;
    while (b > 0) {
        if (b & 1) ans = ans * x % MOD;
        x = x * x % MOD;
        b >>= 1;
    }
    return ans;
}

int main() {
    ll n, m;
    if (scanf("%lld %lld", &n, &m) != 2) return 0;  // 无输入安全退出

    if (n <= 1) {           // n = 1：1 个点 + m 条自环，图唯一
        printf("1\n");
        return 0;
    }
    if (m < n - 1) {        // 无解：连不成 1..n 的链
        printf("0\n");
        return 0;
    }

    // (n-2)! mod p
    ll fact = 1;
    for (ll i = 2; i <= n - 2; i++) fact = fact * i % MOD;

    ll A = n * n - (n - 1) * (n - 2) / 2;  // 允许边类型数，<= 1e8，long long 安全
    ll k = m - n + 1;                      // 余下边数（>= 0）
    ll N = A + k - 1;                      // C(N, k)；N <= 5e7+5e4 << MOD

    ll num = 1, den = 1;                   // num = N*(N-1)*...*(N-k+1)，den = k!
    for (ll i = 0; i < k; i++) {
        num = num * ((N - i) % MOD) % MOD;
        den = den * ((k - i) % MOD) % MOD;
    }
    ll ans = fact * num % MOD * power(den, MOD - 2) % MOD;
    printf("%lld\n", ans);
    return 0;
}
