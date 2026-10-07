// 一本通 1789《分班》 标准程序（std）
// ---------------------------------------------------------------------------
// 题目来源 / 依据：
//   1. 题面与数据规模：一本通官方 OJ 页面 http://ybt.ssoier.cn:8088/problem_show.php?pid=1789
//      （已核对：题名「分班」，时限 1000ms / 262144KB，样例 1 / 10 3 1 4 / ... / 输出 186 3 4 完全一致）。
//   2. 本题同源原题：BSOJ 3425 【模拟试题】分班（DP + 单调队列）。
//      题解（含本题完整 Input/Output/Hint 与 AC 代码）：
//        https://blog.csdn.net/qq_30303087/article/details/53079228
//        《BSOJ 3425：分班 DP+单调队列》
//      该文题面与本题逐字一致（"求的是 sigma((xi-ave)^2)*G[g[i]] ..."），
//      故判定为一本通 1789 的同源原题，std 按其 DP 方程 + 单调队列优化改写，
//      并修正/加固了原文代码中的若干隐患（见下）。
//
// 题意：
//   M 个学生（顺序给定），分成**至多 N 个班**；每个班人数 ∈ [A,B]；同班学生必须连续。
//   记 Average = floor(sum(X)/M)，W[i] = (X[i]-Average)^2。
//   第 j 个班（j=1..k，按顺序对应教室 j）的评价代价 = G[j] * sum_{i in 班 j} W[i]。
//   求三元组 (sigma, class, last) 按字典序最小：
//     sigma = 最小评价指数；
//     class = 在 sigma 最小前提下的**最小**班数；
//     last  = 在 sigma、class 都最小的前提下，**最后一个班人数的最小值**。
//
// 算法（O(N*M)，单调队列优化 DP）：
//   sum[i] = W[1..i] 前缀和。
//   f[j][i] = 前 i 个学生恰好分成 j 个班（每班人数 ∈[A,B]）的最小评价指数：
//       f[j][i] = min_{ i-B <= k <= i-A } { f[j-1][k] + G[j]*(sum[i]-sum[k]) }
//             = G[j]*sum[i] + min_{ k } { f[j-1][k] - G[j]*sum[k] }
//   固定 j 时，括号内只与 k 有关，窗口 [i-B, i-A] 随 i 滑动，
//   故用单调队列维护 min{ f[j-1][k] - G[j]*sum[k] }，均摊 O(1) 转移。
//   f[0][0] = 0，其余 INF。
//
//   答案的字典序处理：
//     - j 从小到大枚举，用**严格** `<` 更新最优，即取「最小 sigma 下的最小班数」；
//     - 同一 j 内，单调队列在相等时弹出队尾（`val <= back`），
//       故队首保留的是**取到最小值的最大 k**，last = M-k 即「最后班人数最小值」。
//
// 原文代码的加固点（均为等价改写 / 消除未定义行为，不改变答案）：
//   - INF 用 4e18（原文 1e18 亦可，但答案上界 ~1e17，4e18 更远离溢出且仍是安全哨兵）；
//   - stu 初值置 -1，仅在 f[m][j] 有限时才用于 last（原文 stu 未初始化，
//     若前若干 j 均无解会读到垃圾值）；
//   - 数组按题面上限 × 安全系数开（M ≤ 10000 → 11000，N ≤ 200 → 256），
//     防止越界；时间/内存均远小于限制。
//
// 复杂度：每组数据 O(N*M) 时间、O(N*M) 空间（long long）；
//         最坏 M=10000,N=200,case=10 → 约 2e7 次转移，1s 内绰绰有余。
// ---------------------------------------------------------------------------

#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>

typedef long long ll;

static const int MAXM = 11000;   // 题面上限 M<=10000，安全系数 1.1
static const int MAXN = 256;     // 题面上限 N<=200，安全系数 1.28
static const ll INF = (ll)4e18;  // 答案上界约 1e17，4e18 作安全哨兵

static ll x[MAXM];
static ll G[MAXN];
static ll psum[MAXM];                 // psum[i] = sum_{t<=i} (x[t]-avg)^2
static std::vector<std::vector<ll> > f;  // f[j][i]
static int q[MAXM];                   // 单调队列（存下标 k）

int main() {
    int ncase;
    if (scanf("%d", &ncase) != 1) return 0;

    f.assign(MAXN + 1, std::vector<ll>(MAXM + 1, INF));

    while (ncase--) {
        int M, N, A, B;
        if (scanf("%d %d %d %d", &M, &N, &A, &B) != 4) break;
        ll s = 0;
        for (int i = 1; i <= M; ++i) { scanf("%lld", &x[i]); s += x[i]; }
        for (int j = 1; j <= N; ++j) scanf("%lld", &G[j]);
        ll avg = s / M;   // 先求和再整除（向下取整）

        psum[0] = 0;
        for (int i = 1; i <= M; ++i) {
            ll d = x[i] - avg;
            psum[i] = psum[i - 1] + d * d;
        }

        // 复位（本题多组数据，只清用到的那一块，避免每组 O(N*M) 的 memset 常数）
        for (int j = 0; j <= N; ++j)
            std::fill(f[j].begin(), f[j].begin() + (M + 1), INF);
        f[0][0] = 0;

        ll best = INF;
        int bestClass = -1, bestLast = -1;

        for (int j = 1; j <= N; ++j) {
            int head = 0, tail = -1;   // 空队列
            int stu = -1;              // 本 j 下 f[M][j] 取到最小值时的最大 k
            const ll gj = G[j];
            for (int i = 1; i <= M; ++i) {
                int p = i - A;         // 新进入窗口的左端点
                if (p >= 0 && f[j - 1][p] < INF) {
                    ll val = f[j - 1][p] - gj * psum[p];
                    // 相等时也弹出队尾 → 队首保留「取到最小值的最大下标 k」
                    while (head <= tail &&
                           val <= f[j - 1][q[tail]] - gj * psum[q[tail]]) --tail;
                    q[++tail] = p;
                }
                while (head <= tail && q[head] < i - B) ++head;  // 滑出窗口
                if (head > tail) continue;                        // f[j][i] 无解
                int k = q[head];
                f[j][i] = f[j - 1][k] + gj * (psum[i] - psum[k]);
                if (i == M) stu = k;
            }
            if (f[j][M] < best) {          // 严格小于 → sigma 相同则保留更小的班数
                best = f[j][M];
                bestClass = j;
                bestLast = M - stu;        // stu 必已赋值（f[j][M] 有限 ⇒ 队非空）
            }
        }

        printf("%lld %d %d\n", best, bestClass, bestLast);
    }
    return 0;
}
