// 一本通 1685《新版方格取数》标程
// 参考来源（思路与解法参考，代码已改写重实现）：
//   https://www.cnblogs.com/DK-orz/p/22896866  （信息学奥赛一本通1685：新版方格取数 - DK_orz - 博客园）
// 题意：m*n (m*n<=16) 方格，从边缘格开始取数，每次可走到相邻四方向的未取格，
//       或者（当前在边缘时）离开方格并从任一未取的边缘格重新进入；
//       第 i 次取走的数 j 得 i*j 分，求最大总得分。
// 解法：状压 DP。dp[S][p] = 已取格集合为 S、当前位于格 p 时的最大得分。
//       初始：所有边缘格 p，dp[{p}][p] = a[p]（第 1 次取，得 1*a[p]）。
//       转移（刷表）：
//         (a) 走到相邻未取格 q：dp[S|{q}][q] = max(dp[S][p] + k*a[q])，k=|S|+1 为取数序号；
//         (b) 若 p 在边缘：可“离开再进入”，即从任意未取边缘格 q 重新开始，
//             dp[S|{q}][q] = max(dp[S][p] + k*a[q])。
//       答案 = 所有 dp[S][p] 的最大值（游戏可以在任何时刻结束，也可中途无路可走）。
// 与来源代码的差异 / 修复说明：
//   1. 来源代码 dp 数组 65536*16 个 ll（8MB）开成全局没问题，但来源把 n/m 读入顺序
//      当作 “n 行 m 列”，与题面 “m 行 n 列” 相反；本题面以 m 行 n 列读入，此处已对齐题面，
//      行列交换不影响正确性（方格取数规则对行列对称）。
//   2. 溢出防护：最大总得分 <= 16*16*99999 < 2^31，但为稳妥仍用 long long；
//      乘积 (k+1)*a[q] 用 (ll) 显式转换，避免 int 中间乘积溢出（来源已如此，保留）。
//   3. 来源用 -INF=1e18 初始化并最后取 max(dp)（初始 0 也可，因为空集得 0 分），
//      此处沿用取 max 的写法，但初始答案取 0（一个数都不取也是合法结束）。
//   4. 使用 scanf/printf（stdin→stdout），风格与仓库 problems/1000/std.cpp 保持一致。
#include <cstdio>
#include <algorithm>
using namespace std;
typedef long long ll;

const ll NEG = -1; // 用 -1 标记“不可达”，因为得分为非负，-1 < 任何可达值

int m, n;            // m 行 n 列（题面原义）
int a[16];           // 展平成一维：格子 i 处于第 i/n 行、第 i%n 列
bool onEdge[16];
ll dp[1 << 16][16];  // dp[S][p]

int main() {
    if (scanf("%d %d", &m, &n) != 2) return 0;
    int total = m * n;
    for (int i = 0; i < total; i++) scanf("%d", &a[i]);

    for (int i = 0; i < total; i++) {
        int r = i / n, c = i % n;
        onEdge[i] = (r == 0 || r == m - 1 || c == 0 || c == n - 1);
    }

    int maxS = 1 << total;
    for (int S = 0; S < maxS; S++)
        for (int p = 0; p < total; p++)
            dp[S][p] = NEG;

    // 初始：第一个数必须从边缘取
    for (int p = 0; p < total; p++)
        if (onEdge[p]) dp[1 << p][p] = a[p];

    for (int S = 0; S < maxS; S++) {
        for (int p = 0; p < total; p++) {
            ll cur = dp[S][p];
            if (cur == NEG) continue;
            int k = __builtin_popcount(S); // 已取 k 个，下一个是第 k+1 个
            int r = p / n, c = p % n;
            static const int dr[4] = {0, 0, 1, -1};
            static const int dc[4] = {1, -1, 0, 0};
            // (a) 走到相邻未取格
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
                int q = nr * n + nc;
                if (S >> q & 1) continue;
                int nS = S | (1 << q);
                ll val = cur + (ll)(k + 1) * a[q];
                if (val > dp[nS][q]) dp[nS][q] = val;
            }
            // (b) 当前在边缘：可离开方格，从任意未取边缘格重新进入
            if (onEdge[p]) {
                for (int q = 0; q < total; q++) {
                    if (!onEdge[q]) continue;
                    if (S >> q & 1) continue;
                    int nS = S | (1 << q);
                    ll val = cur + (ll)(k + 1) * a[q];
                    if (val > dp[nS][q]) dp[nS][q] = val;
                }
            }
        }
    }

    ll ans = 0; // 不取任何数得 0 分
    for (int S = 0; S < maxS; S++)
        for (int p = 0; p < total; p++)
            if (dp[S][p] > ans) ans = dp[S][p];
    printf("%lld\n", ans);
    return 0;
}
