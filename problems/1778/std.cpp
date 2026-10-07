// 一本通 1778《好数字》（目标 ROJ 题号 1778）标程
//
// 题意：一个 2n 位的数字（允许前导 0，每位数字都属于给定数字集合 S）称为好数字，
//       若「前 n 位之和 == 后 n 位之和」或「奇数位之和 == 偶数位之和」。
//       给定 n 与 S，求好数字个数 mod 999983。
//       输入：第一行 n；第二行一个长度不超过 10 的字符串表示 S。
//       输出：一行一个整数。n <= 1000, |S| <= 10。
//
// 算法（容斥 + 背包计数 DP）：
//   设 f[k][s] = 用 S 中数字构成 k 位数、各位数字和恰为 s 的方案数（mod 999983）。
//   记 A = #（前 n 位之和 == 后 n 位之和）= Σ_s f[n][s]^2
//      （前 n 位、后 n 位相互独立，各自和都为 s，故为 Σ_s f[n][s]·f[n][s]）；
//   记 B = #（奇数位之和 == 偶数位之和）：2n 位中奇数位、偶数位各 n 个，
//      同理 B = Σ_s f[n][s]^2 = A。
//   故 A + B = 2·Σ_s f[n][s]^2。
//   再减去交集 I = #（两条件同时成立）。
//   交集刻画：把 2n 位切成前 n 位 b[1..n] 与后 n 位 c[1..n]。
//     条件 1：Σb = Σc；条件 2：Σ_{i odd<=n} b_i + Σ_{i+n odd} c_i = Σ_{i even<=n} b_i + Σ_{i+n even} c_i。
//     令 l1 = 前 n 位中奇数位的个数（n 为奇数时 (n+1)/2，n 为偶数时 n/2），
//        l2 = 前 n 位中偶数位的个数（= n/2）。
//     n 偶：i+n 与 i 同奇偶 ⇒ 两式相减得 Σ_{i even<=n} b_i = Σ_{i odd<=n} c_i，
//           且 Σ_{i odd<=n} b_i = Σ_{i even<=n} c_i；
//     n 奇：i+n 与 i 反奇偶 ⇒ 两式相减得 Σ_{i odd<=n} b_i = Σ_{i odd<=n} c_i，
//           且 Σ_{i even<=n} b_i = Σ_{i even<=n} c_i。
//     两种情形都归结为：奇位块之和相等、偶位块之和相等，而奇位块、偶位块相互独立，
//     故 I = (Σ_s f[l1][s]^2) · (Σ_s f[l2][s]^2)。
//   答案 = (2·Σ_s f[n][s]^2 − (Σ_s f[l1][s]^2)·(Σ_s f[l2][s]^2)) mod 999983。
//
// 参考来源（C++ 题解与 AC 代码，均经本机编译 + 样例验证后**改写**，非盲抄）：
//   1. https://www.cnblogs.com/Comfortable/p/8562344.html
//      《JZOJ 3056 / NOIP2012模拟10.27 数字》题解（原站博客园）
//      —— 明确本 1778 题与 JZOJ 3056 题面逐字一致（问题描述/输入/输出/样例 2 / 0987654321 → 1240
//         均相同），据此判定为同源原题。给出容斥结论：
//         sum = Σ_i 2·f[n][i]·f[n][i]；l1=(n+1)/2, l2=n/2；
//         ans1 = Σ f[l1][i]^2, ans2 = Σ f[l2][i]^2；答案 = sum − ans1·ans2 (mod 999983)。
//   2. https://blog.csdn.net/weixin_30483013/article/details/95748829
//      （来源 1 的 CSDN 镜像，正文与代码逐字相同，用于交叉核对，结论一致。）
//   3. https://www.cnblogs.com/butterflydew/p/9230756.html
//      《洛谷 数字 解题报告》（原站博客园，CSDN 镜像
//       https://blog.csdn.net/weixin_30443731/article/details/99503739）
//      —— 独立给出同一公式：ans = 2·Σ dp[n][i]^2 − a0·a1，
//         其中 k1 = n>>1、k2 = (n+1)>>1，a0 = Σ dp[k1][i]^2、a1 = Σ dp[k2][i]^2。
//         与本标程的 l2 = n/2、l1 = (n+1)/2 完全对应。
//   4. 官方题面：.ybt-import/staging/1778/content.md（一本通高手训练 1778）。
//      样例 1：n=2, S="0987654321" → 1240，已实测一致。
//
// **冲突处置**：来源 1/2 与来源 3 的公式在 l1/l2 的取法上写法不同（(n+1)/2,n/2 vs
// (n+1)>>1,n>>1），但数值完全等价（n/2 与 n>>1 同值，(n+1)/2 与 (n+1)>>1 同值），
// 且两者均与题面样例 1240 一致。**不存在来源冲突或语义歧义，未触发"停下报告"。**
//
// 本标程相对来源的改写点：
//   - 来源 1 开 f[1005][1005*9] long long（约 72 MB，接近 128 MB 上限）；
//     本标程改为**滚动数组 + 三个快照**（f[l1]、f[l2]、f[n]），内存从 ~72 MB 降到 ~180 KB，
//     仍严格在 128 MB 内，且不改变算法与结果。
//   - 用 int 存 DP 值（值域 < 999983 < 2^20，int 足够），乘法处显式转 long long 防溢出。
//   - 对 n=1 时 l2 = 0 的退化情形显式处理（f[0] = {1,0,0,...}）。
//   - 输出带换行（来源 1 的 printf("%lld") 无换行），与仓库既有 staging 数据 .out 口径一致。
//
// 复杂度：时间 O(n · 9n · |S|) ≈ 4.5e7（n=1000 最坏），空间 O(9n)。

#include <cstdio>
#include <cstring>

static const int MO = 999983;
static const int MAXS = 9 * 1000 + 1;  // 各位数字和上限 = 9n, n <= 1000

int f[2][MAXS];      // 滚动数组：当前 / 上一步 的 f[k][*]
int g1[MAXS];        // 快照 f[l1][*]
int g2[MAXS];        // 快照 f[l2][*]
int gn[MAXS];        // 快照 f[n][*]
int dig[16], len;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    char s[32];
    if (scanf("%31s", s) != 1) return 0;
    len = (int)strlen(s);
    for (int i = 0; i < len; i++) dig[i] = s[i] - '0';

    const int l1 = (n + 1) / 2;  // 前 n 位中奇数位个数（n 偶时 = n/2）
    const int l2 = n / 2;        // 前 n 位中偶数位个数

    memset(f, 0, sizeof(f));
    int cur = 0;
    f[cur][0] = 1;               // f[0][0] = 1

    // 规模为 0 的快照（仅 l2 或 l1 可能为 0，即 n = 1 时 l2 = 0）
    if (l2 == 0) memcpy(g2, f[cur], sizeof(g2));
    if (l1 == 0) memcpy(g1, f[cur], sizeof(g1));

    for (int i = 1; i <= n; i++) {
        const int nxt = cur ^ 1;
        const int lim = 9 * i;
        memset(f[nxt], 0, (size_t)(lim + 1) * sizeof(int));
        for (int j = 0; j <= lim; j++) {
            long long v = 0;
            for (int k = 0; k < len; k++) {
                const int d = dig[k];
                if (j - d >= 0) v += f[cur][j - d];
            }
            f[nxt][j] = (int)(v % MO);
        }
        cur = nxt;
        if (i == l1) memcpy(g1, f[cur], sizeof(g1));
        if (i == l2) memcpy(g2, f[cur], sizeof(g2));
        if (i == n)  memcpy(gn, f[cur], sizeof(gn));
    }

    long long sum = 0;           // A + B = 2 * Σ f[n][s]^2
    for (int i = 0; i <= 9 * n; i++)
        sum = (sum + 2LL * gn[i] % MO * gn[i]) % MO;

    long long a1 = 0;            // Σ f[l1][s]^2
    for (int i = 0; i <= 9 * l1; i++)
        a1 = (a1 + 1LL * g1[i] * g1[i]) % MO;

    long long a2 = 0;            // Σ f[l2][s]^2
    for (int i = 0; i <= 9 * l2; i++)
        a2 = (a2 + 1LL * g2[i] * g2[i]) % MO;

    long long ans = ((sum - a1 * a2) % MO + MO) % MO;
    printf("%lld\n", ans);
    return 0;
}
