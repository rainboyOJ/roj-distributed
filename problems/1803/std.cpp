// 一本通 1803《列数字》标程
//
// 题意（见 content.md）：给 1..N 的一个置换 f。把 1..N 排成一行，反复在其下写出
// 每个数的像，直到序列再次变回 1,2,...,N，记录写出的总排数。
// 记置换的阶（最小正整数 k 使 f^k = id）为 ord，则总排数 = ord + 1。
// 于是"所有可能的排数"的个数 = 所有可能的 ord 的个数。
//
// 结论：一个置换的阶 = 其各轮换长度的 lcm，而轮换长度恰好构成 N 的一个分拆。
//   所以答案 = #{ 分拆 λ ⊢ N 的 lcm(λ) 的全体不同取值 }。
//   又因为 lcm 只由各素数的最大幂次决定，一个可达的 lcm 与"每个素数取至多一个
//   幂 p^a，且这些幂之和 ≤ N（剩余部分用 1 填满）"的选取一一对应
//   （不同选取给出不同乘积，故不同 lcm）。因此答案 = 满足
//       Σ 选取的素数幂 ≤ N
//   的选取方案数（含空集，空集对应恒等置换、ord = 1、排数 = 2）。
//
// 算法：按素数分组的有界背包计数。dp[j] = 已处理若干素数后、所选素数幂之和
// 恰为 j 的方案数。对每个素数 p 枚举其幂 p^a ≤ N，转移
//   nd[j + p^a] += dp[j]（对每个素数至多选一个幂），同时保留 dp[j]（不选该素数）。
//   答案 = Σ_{j=0..N} dp[j]。
// 复杂度：O(N · Σ_p (素数 p 的幂个数))，N ≤ 1000 时为百万量级，远低于 1s。
// 数值范围：N = 1000 时答案 3018714402027 < 2^63，用 long long 即可，无需高精度。
//
// 题源认定与检索记录（重要，供人工复核）：
//   本题题面逐字对应 SCOI2009「游戏」（洛谷 P4161）——
//   "windy学会了一种游戏。对于 1 到 N 这 N 个数字，都有唯一且互不相同的
//    1 到 N 的数字与之对应……" 为原题原文，数据范围 N ≤ 1000 亦一致。
//   本次会话中尝试检索题解（Bing 精确短语 / CSDN / 博客园 / 洛谷 P4161 /
//   百度 / 搜狗 / DuckDuckGo）均因目标站点在本环境不可达（302/反爬/超时）
//   而未取到可用博客 URL，故未引用具体文章链接。标程按上述标准解法自研实现，
//   并已用「暴力枚举 N 的分拆求不同 lcm 的个数」在 N=1..12 上逐点验证一致，
//   且题面样例 N=10 → 16 通过（见 gen-report.md）。
#include <cstdio>
#include <vector>

typedef long long ll;

int main()
{
    int n;
    if (scanf("%d", &n) != 1)
        return 0;

    // 线性筛出 [2, n] 内的素数
    std::vector<int> primes;
    for (int x = 2; x <= n; x++) {
        bool isp = true;
        for (int d = 2; (ll)d * d <= x; d++)
            if (x % d == 0) { isp = false; break; }
        if (isp) primes.push_back(x);
    }

    // dp[j]：所选素数幂之和恰为 j 的方案数（每个素数至多取一个幂）
    std::vector<ll> dp(n + 1, 0);
    dp[0] = 1; // 空集：和为 0 的一种方案

    for (size_t pi = 0; pi < primes.size(); pi++) {
        int p = primes[pi];
        std::vector<int> pw;            // 该素数的所有幂 p^a <= n
        for (ll q = p; q <= n; q *= p)
            pw.push_back((int)q);

        std::vector<ll> nd = dp;        // 不选该素数
        for (int j = 0; j <= n; j++) {
            if (dp[j] == 0) continue;
            for (size_t t = 0; t < pw.size(); t++)
                if (j + pw[t] <= n)
                    nd[j + pw[t]] += dp[j];   // 选该素数的一个幂
        }
        dp.swap(nd);
    }

    ll ans = 0;
    for (int j = 0; j <= n; j++)
        ans += dp[j];   // 和 ≤ n 的所有方案
    printf("%lld\n", ans);
    return 0;
}
