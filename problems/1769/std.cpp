// 一本通 1769《景中人》 标准程序 (std.cpp)
//
// 题意：平面上 n 个点 (x,y)（x,y 非负），用最少数量的矩形覆盖所有点；每个矩形面积 <= S，
//       且矩形的一条边必须贴着 y=0（即矩形形如 [a,b] x [0,h]，面积 = (b-a)*h）。
// 输入：多组数据。第一行 T；每组第一行 n S，随后 n 行 x y。
// 输出：每组一行，最少矩形数。
// 数据范围：T<=10, n<=100, x<=3000000, 1<=y<=S<=200000。
//
// ---------------------------------------------------------------------------
// 来源（均为网络公开题解/AC 代码，已 curl 实取正文核对；两来源算法互相独立且一致）：
//
// [S1] https://blog.csdn.net/kirikayakazuto/article/details/110672398
//      《信奥赛一本通1769：景中人ac代码》 —— 与本题题面逐字一致，给出该题的 AC 代码
//      （记忆化搜索，状态 dp[x][xx][gao]，与本文件状态定义相同）。
// [S2] https://blog.csdn.net/mys_c_k/article/details/84537802
//      《景中人 - dp》 —— 独立来源，给出同一算法的自底向上写法与关键性质说明：
//      「性质：存在一种最优解，矩形的底边存在包含关系或者相离。
//        因此考虑一个区间 dp，设 dp[i,j,k] 表示 i 到 j 的点覆盖 k 高度及以上的点的最小代价，
//        转移枚举分两半或者选 [i,j] 即可。」
// [S3] https://blog.csdn.net/ez_yww/article/details/78993247 《【XSY2693】景中人 区间DP》
//      （摘要可见：矩形横坐标关系只能"相离或包含"，不会相交 → 区间 DP）—— 与 [S2] 性质一致。
//
// 本标程以 [S2] 的自底向上版本为骨架改写（比 [S1] 的记忆化递归更易界定复杂度），
// 改写点：
//   1) [S2] 中 `getid(S/(vx[j-1]-vx[i-1]), vy)` 在商 >= 最大高度时返回 m+1，
//      随即访问 vy[m] 越界（vector 下标 m 非法，UB）。本实现改用
//      upper_bound(vy, q) 直接取「<= q 的最大高度下标」（无则 0，全则 m），语义等价且无越界。
//   2) 读入用 long long 承接 S，数组上限取 110（题面上限 100 x 安全系数），
//      dp 第三维开到 110 以容纳阈值下标 m+1 / m+2。
//   3) n=0 的退化输入直接输出 0（题面隐含 n>=1，此处仅作健壮性保护）。
//
// 算法（与 [S1][S2] 完全一致）：
//   1. 同一横坐标 x 上的点只需保留最大的 y（矩形 [a,b]x[0,h] 覆盖 (x,y) 当且仅当 a<=x<=b 且 y<=h）。
//      于是把点压缩为 nn 列，第 t 列 (vx[t-1], 高度下标 yv[t])；m = 去重后的高度个数。
//   2. 性质：存在最优解使各矩形底边（横坐标区间）两两「相离或包含」（相交的两矩形可把矮者截短，
//      被截去的点必被高者覆盖），故为区间 DP。
//   3. dp[i][j][k] = 覆盖第 i..j 列中所有高度 >= vy[k-1] 的点所需最少矩形数。转移：
//        (a) 分裂：dp[i][j][k] = min_t dp[i][t][k] + dp[t+1][j][k]；
//        (b) 用一条横跨整个 [vx[i-1], vx[j-1]] 的矩形（高度取允许的最大值 ymx = max{h : h<=S/width}）：
//            当 ymx >= max(yv[i], yv[j], k) 时 dp[i][j][k] = min(.., dp[i][j][ymx+1] + 1)。
//            要求 ymx >= yv[i], yv[j] 是因为「整跨矩形」必须能覆盖两端列（否则应由 (a) 处理）；
//            ymx >= k 时才有意义（否则 dp[i][j][ymx+1] >= dp[i][j][k]，不可能更优）。
//        k 从 m 递减枚举，保证 dp[i][j][ymx+1] 已被算过（ymx+1 > k）。
//   4. 答案 = dp[1][nn][1]。
//   复杂度：O(nn^2 * m * nn) 级别的区间 DP，nn,m<=100，T<=10，实测最坏点 < 0.1 s。
// ---------------------------------------------------------------------------

#include <bits/stdc++.h>
using namespace std;

const int MAXN = 110;              // 题面上限 100 x 安全系数
static int X[MAXN], Y[MAXN];
static int yv[MAXN];               // yv[t] = 第 t 列的最大高度在去重高度表中的 1-based 下标
static int dp[MAXN][MAXN][MAXN];   // dp[i][j][k], k 取值 1..m+2

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        int n;
        long long S;
        if (scanf("%d %lld", &n, &S) != 2) return 0;

        vector<int> vx, vy;
        vx.reserve(n); vy.reserve(n);
        for (int i = 0; i < n; i++) {
            scanf("%d %d", &X[i], &Y[i]);
            vx.push_back(X[i]);
            vy.push_back(Y[i]);
        }

        if (n <= 0) { printf("0\n"); continue; }

        sort(vx.begin(), vx.end());
        vx.erase(unique(vx.begin(), vx.end()), vx.end());
        sort(vy.begin(), vy.end());
        vy.erase(unique(vy.begin(), vy.end()), vy.end());

        int nn = (int)vx.size();     // 列数
        int m  = (int)vy.size();     // 高度档数

        for (int t = 1; t <= nn; t++) yv[t] = 0;
        for (int i = 0; i < n; i++) {
            int t  = (int)(lower_bound(vx.begin(), vx.end(), X[i]) - vx.begin()) + 1;
            int hh = (int)(lower_bound(vy.begin(), vy.end(), Y[i]) - vy.begin()) + 1;
            if (hh > yv[t]) yv[t] = hh;
        }

        // 单列基态：需要覆盖第 i 列的（最大高度）点时 1 个矩形，否则 0
        for (int i = 1; i <= nn; i++)
            for (int k = 1; k <= m; k++)
                dp[i][i][k] = (k <= yv[i]) ? 1 : 0;
        // 阈值高于最高档：无点需要覆盖
        for (int i = 1; i <= nn; i++)
            for (int j = i; j <= nn; j++)
                dp[i][j][m + 1] = dp[i][j][m + 2] = 0;

        for (int len = 2; len <= nn; len++) {
            for (int i = 1; i + len - 1 <= nn; i++) {
                int j = i + len - 1;
                long long width = (long long)vx[j - 1] - vx[i - 1];
                long long q = S / width;                     // 整跨 [i,j] 时允许的最大高度（下取整）
                // ymx = 「高度 <= q 的最大档」的 1-based 下标（无则 0，全部 <= q 则为 m）
                int ymx = (int)(upper_bound(vy.begin(), vy.end(), (int)min<long long>(q, INT_MAX)) - vy.begin());
                int need = max(max(yv[i], yv[j]), 0);
                bool cross_ok = (ymx >= need);               // 整跨矩形至少能盖住两端列
                for (int k = m; k >= 1; k--) {
                    int best = j - i + 1;                    // 上界：每列各用一个宽度 0 的矩形
                    for (int t = i; t < j; t++) {
                        int v = dp[i][t][k] + dp[t + 1][j][k];
                        if (v < best) best = v;
                    }
                    if (cross_ok && ymx >= k) {
                        int v = dp[i][j][ymx + 1] + 1;       // ymx+1 > k，本 len 已算过
                        if (v < best) best = v;
                    }
                    dp[i][j][k] = best;
                }
            }
        }

        printf("%d\n", dp[1][nn][1]);
    }
    return 0;
}
