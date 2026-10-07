// 一本通 1717《负环》 标程
//
// 题意：给定 n 个点 m 条边的带权有向图（保证无重边、无自环），求点数最少的负环
//       所含点数；若不存在负环输出 0。
// 数据范围（题面）：2 <= n <= 300，0 <= m <= n*(n-1)，|w_i| <= 10^4。
//
// 做法：倍增 Floyd（min-plus 矩阵幂）+ 按位贪心，O(n^3 log n)。
//   记 B[i] = “至多使用 2^i 条边”时任意两点间的最短路矩阵：
//     B[0] = 邻接矩阵，并令主对角线 = 0（表示“留在原地”，从而把 <= L 转化为“恰好 L 步”）。
//     B[i] = B[i-1] (x) B[i-1]（min-plus 乘法，即一次 Floyd 的矩阵形式）。
//   一条闭迹权值为负等价于含负环；简单负环点数 L* <= n <= 300 < 511 = 2^9-1，
//   故只需 bits 0..8。按位从高到低贪心：
//     cur 表示“至多 tot 条边”的最短路矩阵（初始为 0 条边即单位矩阵），
//     若 cur (x) B[i] 的主对角线没有负数（即不存在 <= tot+2^i 条边的负权闭迹），
//     则接受 cur = cur (x) B[i]，tot += 2^i；否则跳过。
//   循环结束后再乘一次 B[0]：主对角线出现负数则答案为 tot+1，否则图中无负环输出 0。
//
// 正确性要点：
//   - “存在负权闭迹” <=> “存在负环”（闭迹删去非负子回路后必得负环），
//     且最短负环长度不超过 n，故答案为“最小的 L 使存在 <= L 条边的负权闭迹”。
//   - 主对角线可保持 <= 0，从而 B 矩阵元素始终 <= INF，且真实最短路权值
//     <= 511*10^4 < INF，用 int + INF=0x3f3f3f3f 不溢出（相加 <= 2*INF < INT_MAX）。
//
// 【来源说明】本题与经典题 BZOJ 4773《负环》题面与数据范围完全一致（同一道题）。
//   参考的公开题解（访问日期 2026-02）：
//     https://www.cnblogs.com/GXZlegend/p/6856410.html       （倍增 Floyd，n=300 原始数据）
//     https://www.cnblogs.com/hankeke/p/bzoj4773.html        （倍增邻接矩阵 + 二分思想）
//     https://www.cnblogs.com/Blue233333/p/7636520.html      （矩阵快速幂式倍增 + LCA 式贪心）
//   本代码按上述思路自行重写，并核对了 BZOJ 4773 样例（3 6 / 答案 2）与本题样例（答案 4）。

#include <cstdio>
#include <cstring>

static const int MAXN = 305;
static const int INF = 0x3f3f3f3f;
static const int BITS = 8;  // 2^8 = 256，配合按位贪心可表示 0..511 > n

int n, m;
static int B[BITS + 1][MAXN][MAXN];  // B[i]：至多 2^i 条边的最短路（min-plus 幂）
static int cur[MAXN][MAXN];
static int tmp[MAXN][MAXN];

// out = a (x) b，min-plus 乘法（Floyd 的矩阵形式）
static void mul(const int a[][MAXN], const int b[][MAXN], int out[][MAXN])
{
    for (int i = 0; i < n; ++i) {
        int *oi = out[i];
        const int *ai = a[i];
        for (int j = 0; j < n; ++j) oi[j] = INF;
        for (int k = 0; k < n; ++k) {
            const int aik = ai[k];
            const int *bk = b[k];
            for (int j = 0; j < n; ++j) {
                const int v = aik + bk[j];
                if (v < oi[j]) oi[j] = v;
            }
        }
    }
}

static bool hasNegDiag(const int a[][MAXN])
{
    for (int i = 0; i < n; ++i)
        if (a[i][i] < 0) return true;
    return false;
}

int main()
{
    if (scanf("%d %d", &n, &m) != 2) return 0;

    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) B[0][i][j] = INF;
    for (int i = 0; i < n; ++i) B[0][i][i] = 0;
    for (int e = 0; e < m; ++e) {
        int u, v, w;
        if (scanf("%d %d %d", &u, &v, &w) != 3) return 0;
        --u; --v;
        if (w < B[0][u][v]) B[0][u][v] = w;  // 题面保证无重边，此处仅作防御
    }

    for (int i = 1; i <= BITS; ++i) mul(B[i - 1], B[i - 1], B[i]);

    // cur = “至多 0 条边”的最短路 = 单位矩阵
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j) cur[i][j] = (i == j ? 0 : INF);

    int tot = 0;
    for (int i = BITS; i >= 0; --i) {
        mul(cur, B[i], tmp);
        if (!hasNegDiag(tmp)) {
            for (int r = 0; r < n; ++r)
                memcpy(cur[r], tmp[r], sizeof(int) * n);
            tot += 1 << i;
        }
    }

    mul(cur, B[0], tmp);
    printf("%d\n", hasNegDiag(tmp) ? tot + 1 : 0);
    return 0;
}
