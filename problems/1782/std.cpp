// 一本通 1782《分层图》标程
//
// 题意：DAG 分 m 层，第 1 层只有源点 s，第 m 层只有汇点 t，中间每层 k 个点。
//       可以任选若干相邻层 i,i+1（1<i<m-1）之间的边"取反"：把边 (i,k1)->(i+1,k2)
//       变成 (i,k2)->(i+1,k1)，即把该两层之间的 k×k 邻接矩阵转置。
//       问有多少种取反方案，使得 s->t 的路径条数为偶数，答案 mod 998244353。
//
// 算法（状压 DP，利用 k<=10 与"只关心奇偶性"两个特征）：
//   记第 i 层各点"从源点到它的路径条数 mod 2"组成的 k 位向量为 v_i。
//   设第 i、i+1 层间邻接矩阵为 M（行=第 i 层点，列=第 i+1 层点），
//   则 v_{i+1} = v_i * M（不取反）或 v_i * M^T（取反），运算在 GF(2) 上。
//   于是只需以 v_i ∈ {0,1}^k（至多 2^k 个状态）为 DP 状态：
//     f[v] = 走到第 i 层、且该层奇偶向量恰为 v 的"取反方案前缀数"（mod 998244353）。
//   转移：对每个状态 v，分别按 M 与 M^T 推到下一层（两个方案都计数）。
//   第 1 层（源点）无取反、第 m-1 层到汇点也无取反，单独处理。
//   最终 s->t 路径数 mod 2 = Σ_j (v_{m-1})_j * w_j（w_j = 汇点边指示），
//   答案 = Σ_{v: popcount(v & w) 为偶} f[v]。
//
//   加速：X[s] = XOR_{j∈s} (M 第 j 行掩码)，Y[s] = XOR_{j∈s} (M^T 第 j 行掩码)
//   = XOR_{j∈s} (M 第 j 列掩码)，用 lowbit 递推 O(2^k) 预计算，
//   则 v*M = X[v]、v*M^T = Y[v]。
//   总复杂度 O(m * 2^k)，m<=10^4, k<=10 时约 10^7 次运算。
//
// 来源（已联网检索，题面特征句精确命中；代码按题面自行改写并编译验证）：
//   * 本题与 JZOJ 5398 /【NOIP2017提高A组模拟10.7】Adore 同题（题面逐句一致，
//     含"取反第 i(1<i<m-1) 层和第 i+1 层之间的连边""答案对 998244353 取模"
//     "4<=m<=10^4, k<=10"）：
//     - https://blog.csdn.net/huangjingyuan107/article/details/78171654
//       （"JZOJ 5398. 【NOIP2017提高A组模拟10.7】Adore"：题解明确
//        "①k<=10，②奇偶性 → 状压 DP；设 f[i][j] 表示做到第 i 层、此层状态
//        （从源点走到的方案数奇偶性）为 j 的方案数"，转移 a0/a1 即本标程的
//        X/Y 两条转移，答案 f[末层][0]）
//     - https://blog.csdn.net/weixin_30672019/article/details/99498520
//       （"Adore 解题报告"，题面与本题逐句一致，同样的状压奇偶 DP）
//   两来源结论一致，与题面样例一致，无冲突。
#include <cstdio>
#include <cstring>

static const int MOD = 998244353;
static const int MAXK = 10;              // 题面 k<=10
static const int MAXS = 1 << (MAXK + 2); // 安全系数：允许 k 到 12 仍不越界

// ---------------- 快速读入 ----------------
static char ibuf[1 << 20];
static int ipos = 0, ilen = 0;

static inline int gc()
{
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen <= 0)
            return -1;
    }
    return ibuf[ipos++];
}

static int readInt()
{
    int c = gc();
    while (c != -1 && (c < '0' || c > '9') && c != '-')
        c = gc();
    int sgn = 1;
    if (c == '-') { sgn = -1; c = gc(); }
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x * sgn;
}

static int m, k;
static int dp[MAXS], ndp[MAXS];
static int rowMask[MAXK], rowMaskT[MAXK]; // M 的行掩码 / M^T 的行掩码(即 M 的列掩码)
static int X[MAXS], Y[MAXS];

int main()
{
    m = readInt();
    k = readInt();
    if (m <= 0 || k <= 0 || k > MAXK)   // 按题面范围 4<=m<=10^4, k<=10
        return 0;
    int N = 1 << k;

    // 第 1 行：源点到第 2 层各点的边 -> 第 2 层的奇偶向量
    int u = 0;
    for (int t = 0; t < k; t++)
        if (readInt())
            u |= (1 << t);

    memset(dp, 0, sizeof(dp));
    dp[u] = 1;

    // 第 2..m-2 行：中间层之间的 k×k 邻接矩阵，可取反
    for (int i = 2; i <= m - 2; i++) {
        memset(rowMask, 0, sizeof(rowMask));
        memset(rowMaskT, 0, sizeof(rowMaskT));
        for (int j = 0; j < k; j++)
            for (int t = 0; t < k; t++)
                if (readInt()) {
                    rowMask[j] |= (1 << t);    // (i,j) -> (i+1,t)
                    rowMaskT[t] |= (1 << j);   // 取反后 (i,t) -> (i+1,j)
                }

        X[0] = Y[0] = 0;
        for (int s = 1; s < N; s++) {
            int low = s & (-s);
            int idx = __builtin_ctz(s);
            X[s] = X[s ^ low] ^ rowMask[idx];
            Y[s] = Y[s ^ low] ^ rowMaskT[idx];
        }

        memset(ndp, 0, sizeof(int) * N);
        for (int s = 0; s < N; s++) {
            int v = dp[s];
            if (!v)
                continue;
            int a = X[s], b = Y[s];       // 不取反 / 取反
            ndp[a] += v; if (ndp[a] >= MOD) ndp[a] -= MOD;
            ndp[b] += v; if (ndp[b] >= MOD) ndp[b] -= MOD;
        }
        memcpy(dp, ndp, sizeof(int) * N);
    }

    // 最后一行：第 m-1 层各点到汇点的边
    int w = 0;
    for (int t = 0; t < k; t++)
        if (readInt())
            w |= (1 << t);

    long long ans = 0;
    for (int s = 0; s < N; s++)
        if ((__builtin_popcount(s & w) & 1) == 0)
            ans += dp[s];
    printf("%lld\n", ans % MOD);
    return 0;
}
