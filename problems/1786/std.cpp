// 一本通 1786《01背包》
// ---------------------------------------------------------------------------
// 题意：n 个物品（体积 s，价值 v），对每个容量 j = 1..m 独立地做一次 0/1 背包，
//       输出 m 个最大价值。数据范围 1<=n<=1e6, 1<=m<=1e5, 1<=s<=300, 1<=v<=1e9。
//       限制 time 7000 ms / memory 512 MB（config.json）。
//
// 来源（网络检索 + 自研补全）：
//   * 题面特征句「OIP马上就要到了，爱思考的kcz在复习01背包时想到了这样一个问题」精确检索，
//     只命中题面转载页（www.kidscoding8.com/116999.html，仅题面无解），无公开完整题解。
//   * 用「体积分组 + 组内价值降序 + 单调队列 + 二分求最优性反转时间」检索，命中同源题解
//     《WZOJ 1304 01背包加强版(完全背包单调队列优化)》
//     https://blog.csdn.net/qq_16267919/article/details/79447128
//     该文摘要即本题正解骨架：「将相同体积的物品归类并按价值排序 …… 在物品价值逐渐减小的
//     情况下，队列中元素最优性的反转 …… 二分查找确定反转时间，以确保队列单调」。
//     （正文付费墙，仅摘要可见；下面算法细节由本包自行推导并给出完整证明。）
//
// 算法（O(n log n_输入 + Σ_s m log(m/s))，s 为不同体积数 <= 300）：
//
//   记 dp[j] = 容量 <= j 时的最大价值（题面答案即 dp[1..m]）。初始 dp ≡ 0。
//   把物品按体积 s 分组；同一组内物品体积相同，故「取 k 个」一定取价值最大的 k 个。
//   设组 s 有 cnt 个物品，价值降序为 v[1..cnt]，前缀和 P[k] = v[1]+...+v[k]（k>cnt 时 P[k]=P[cnt]）。
//   按体积 s 从小到大做一次「组内多重背包」转移：
//
//        new_dp[j] = max_{ 0 <= k <= min(i, floor(m/s)) } dp[j - k*s] + P[k]
//
//   注意：把 P 在 k>cnt 处延拓为常数 P[cnt] 是**无损**的（多取的是体积 s、价值 0 的
//   幽灵物品，A[i-k] <= A[i-cnt]，永不更优），于是转移里 k 的上界只剩容量约束，
//   「最多 cnt 个」的滑动窗口约束消失，实现大为简化。
//
//   按 residue r mod s 拆开（j = r + i*s，A[i] = dp[r+i*s]，C[i] = new_dp[r+i*s]）：
//
//        C[i] = max_{ 0 <= t <= i } A[t] + P[i - t]          （t = i-k 为「源位置」）
//
//   **核心引理（二分反转时间的依据）**：对 t1 < t2，令
//        D(i) = f_{t1}(i) - f_{t2}(i) = (A[t1]-A[t2]) + (P[i-t1] - P[i-t2])
//             = 常数 + Σ_{k=u+1}^{u+d} v[k],  u = i-t2, d = t2-t1 > 0.
//   由于组内价值降序（v 非增），Σ_{k=u+1}^{u+d} v[k] 关于 u 单调不增，
//   故 D(i) 关于 i 单调不增：**t1 与 t2 的优劣至多反转一次，且只会从「t1 更优」翻到「t2 更优」**。
//   等价说法：矩阵 M[i][t] = A[t]+P[i-t] 对行最大值是**全单调**的，因此
//      (a) argmax_t 关于 i 单调不减（可用分治优化，本实现不用）；
//      (b) 可用「单调队列 + 二分求反转时间」在线维护上包络。
//
//   本实现采用 (b)：队列存候选源位置 t（递增）与 sigma[t]（t 成为最优的时刻，递增）。
//   插入候选 i 时与队尾 t_last 比较，二分出首个满足 f_i(i') > f_{t_last}(i') 的 i' = tau
//   （D 单调 ⇒ 可二分）；若 tau <= sigma[t_last] 则 t_last 永远不会成为最优，弹尾；
//   若在整个 [i, I] 上都不反转则候选 i 恒劣于队尾，直接丢弃。取答案时把 sigma[队首+1] <= i
//   的队首弹出，队首即为当前最优源位置。每元素入队/出队各一次，每次插入一次二分，
//   单 residue 复杂度 O(I log I)，全题 Σ_s m log(m/s)（s<=300）。
//
//   样例验证（n=4,m=9, 物品 (2,8)(1,1)(3,4)(5,100)）：
//     本程序输出 "1 8 9 9 100 101 108 109 109"，与题面输出样例逐字一致。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <vector>

using namespace std;

// 题面 s <= 300；安全系数 ~13 倍开桶，避免越界（若 s 超过此值，程序会跳过该物品并报警）
static const int MAXS = 4096;

static vector<char> g_in;

static inline int readInt(size_t &p, size_t n) {
    while (p < n && (g_in[p] < '0' || g_in[p] > '9')) ++p;
    int x = 0;
    while (p < n && g_in[p] >= '0' && g_in[p] <= '9') { x = x * 10 + (g_in[p] - '0'); ++p; }
    return x;
}

int main() {
    // ---- 读入全部输入（n 可达 1e6 行）----
    {
        const size_t CH = 1 << 20;
        char tmp[CH];
        size_t r;
        g_in.reserve(1 << 25);
        while ((r = fread(tmp, 1, CH, stdin)) > 0) g_in.insert(g_in.end(), tmp, tmp + r);
        g_in.push_back('\0');
    }
    size_t p = 0, tot = g_in.size();

    int n = readInt(p, tot);
    int m = readInt(p, tot);
    if (n < 0) n = 0;
    if (m < 0) m = 0;

    vector<vector<int> > vals(MAXS);
    bool overflow = false;
    for (int i = 0; i < n; ++i) {
        int s = readInt(p, tot);
        int v = readInt(p, tot);
        if (s <= 0) continue;
        if (s > m) continue;                 // 体积超过任何容量：任何方案都用不到
        if (s >= MAXS) { overflow = true; continue; }
        vals[s].push_back(v);
    }
    if (overflow) fprintf(stderr, "[std] WARNING: some s >= MAXS(%d) skipped\n", MAXS);

    // dp[j] = 容量 <= j 的最大价值（j = 0..m）
    vector<long long> dp((size_t)m + 1, 0);

    vector<long long> A((size_t)m + 2), C((size_t)m + 2);
    vector<long long> P((size_t)m + 2);
    vector<int> dqt((size_t)m + 2), dqsig((size_t)m + 2);

    for (int s = 1; s <= m && s < MAXS; ++s) {
        if (vals[s].empty()) continue;
        vector<int> &w = vals[s];
        sort(w.begin(), w.end(), greater<int>());
        int cnt = (int)w.size();
        int K = m / s;                       // k 的上界（k*s <= m）

        // P[k] = 组内最大 k 个价值之和（k > cnt 时延拓为 P[cnt]）
        P[0] = 0;
        for (int k = 1; k <= K; ++k)
            P[k] = P[k - 1] + (k <= cnt ? (long long)w[k - 1] : 0LL);

        for (int r = 0; r < s; ++r) {
            if (r > m) break;
            int I = (m - r) / s;             // i = 0..I
            for (int i = 0; i <= I; ++i) A[i] = dp[(size_t)r + (size_t)i * s];

            int head = 0, tail = -1;
            for (int i = 0; i <= I; ++i) {
                bool ins = false;
                int sig = 0;
                while (head <= tail) {
                    int tl = dqt[tail];
                    int d = i - tl;                 // d > 0
                    int U = I - i;                  // u = i'-i 的上界
                    long long base = A[tl] - A[i];
                    // G(u) = base + P[u+d] - P[u] 关于 u 单调不增
                    if (base + P[U + d] - P[U] >= 0) { ins = false; break; }  // 永不反超 -> 丢弃 i
                    int lo = 0, hi = U;
                    while (lo < hi) {               // 首个 G(u) < 0 的 u
                        int mid = (lo + hi) >> 1;
                        if (base + P[mid + d] - P[mid] < 0) hi = mid; else lo = mid + 1;
                    }
                    int tau = i + lo;
                    if (tau <= dqsig[tail]) { --tail; continue; }   // 队尾永不最优
                    sig = tau; ins = true; break;
                }
                if (head > tail) { sig = i; ins = true; }           // 队列被弹空 -> i 立即最优
                if (ins) { ++tail; dqt[tail] = i; dqsig[tail] = sig; }
                while (tail - head + 1 >= 2 && dqsig[head + 1] <= i) ++head;  // 队首被反超
                int t = dqt[head];
                C[i] = A[t] + P[i - t];
            }
            for (int i = 0; i <= I; ++i) dp[(size_t)r + (size_t)i * s] = C[i];
        }
    }

    // ---- 输出 m 个数：容量 1..m 的最大价值 ----
    {
        const int CH = 1 << 16;
        char obuf[CH];
        int opos = 0;
        char num[32];
        for (int j = 1; j <= m; ++j) {
            long long x = dp[j];
            int len = 0;
            if (x == 0) num[len++] = '0';
            while (x > 0) { num[len++] = char('0' + (int)(x % 10)); x /= 10; }
            if (j > 1) obuf[opos++] = ' ';
            while (len > 0) obuf[opos++] = num[--len];
            if (opos > CH - 40) { fwrite(obuf, 1, opos, stdout); opos = 0; }
        }
        obuf[opos++] = '\n';
        fwrite(obuf, 1, opos, stdout);
    }
    return 0;
}
