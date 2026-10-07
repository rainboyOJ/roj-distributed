// 一本通 1791《太空飞船》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 题面（官方）：http://ybt.ssoier.cn:8088/problem_show.php?pid=1791
//   官方页确认：题号 1791、题名「太空飞船」、时限 1000 ms、内存 262144 KB。
// 原题出处：BJOI2017 一试 spaceship（题面首段「21XX年，秋。小诚是THU…」为原题全文）。
// 解法与标程参考（按题面特征句「太空飞船（spaceship）」精确检索所得）：
//   [1] https://blog.csdn.net/liankewei123456/article/details/84667713
//       《太空飞船（spaceship）》—— 完整题面 + 来源「BJOI2017一试」+ 解法要点与标程：
//         * 化简方差式后等价于「环形分成 K 段，最小化 sum s_i^2」；
//         * K=2：双指针维护权和接近 S/2 的切点；
//         * K=3：在 K=2 的基础上二分第二个切点；
//         * n<=400：令 f[i][j] = 前 i 个点分 j 块的最小代价，
//           f[i][j] = min_k f[k][j-1] + (sum[i]-sum[k])^2，滚动 + 斜率优化；
//           环形则枚举 n 个断环起点（共 O(n^2 K)）。
//   [2] https://blog.csdn.net/weixin_39837352/article/details/118987469
//       《信息学奥赛题库- 太空飞船》—— 与官方一致的题面（含 10 个测试点数据规模表）。
// 结论：[1] 的做法与题面/样例口径一致，本标程按 [1] 的思路改写（清理命名、加边界保护、
//       最终答案用 __int128 累乘防溢出），非盲抄。
// =============================================================================
//
// 题意与公式（关键推导）：
//   设 K 段长度和为 s_1..s_K，总和 S = sum L_i 固定，s_avg = S/K。
//   题面定义「方差」为 sum_{i=1..K} (s_i - s_avg)^2（注意题面未除以 K）。
//   方差 * K^2 = K^2 * ( sum s_i^2 - S^2/K ) = K^2 * sum s_i^2 - K * S^2。
//   故只需最小化 sum s_i^2，答案 = K^2*minSumSq - K*S^2。
//   自检（样例1）：K=2，分段 [2 6][1 3 4] -> s=8,8，minSumSq=128，
//     2^2*128 - 2*16^2 = 512-512 = 0 ✓（样例输出 0）。
//   自检（样例2）：K=3，分段 [4 2][6][1 3] -> s=6,6,4，minSumSq=88，
//     3^2*88 - 3*16^2 = 792-768 = 24 ✓（样例输出 24）。
//
// 数据范围（题面）：1 <= L_i <= 1000；N <= 300000；K <= 20；10 个测试点。
//   测试点表（题面「数据规模」）：n<=400 的点 K 最大到 20；
//   n>400 的点（N=1000/100000/300000）K 仅为 2 或 3（与 [1] 的分支一致）。
// 时限 1000 ms：n<=400 走 O(n^2 K) 斜率优化；n>400 走 O(N log N) 的双指针/二分。
//
// 分支：
//   (A) n <= 400      ：枚举 n 个断环起点，斜率优化（凸包）DP，O(n^2 K)，精确。
//   (B) n > 400, K=2  ：双指针，对每个起点取权和最接近 S/2 的切点。
//   (C) n > 400, K=3  ：先定第一个切点（权和不超 S/3 的最远点），再二分第二个切点。
//   (D) K=1           ：方差恒为 0（退化保护，题面数据 K>=2）。

#include <cstdio>
#include <algorithm>

typedef long long ll;
typedef __int128 lll;

static const ll INF = (ll)4e18;

static int n, k;
static ll a[600005];   // 舱室长度（倍长，1-indexed，供断环使用）
static ll ps[600005];  // 倍长前缀和，ps[i] = a[1..i] 之和（ps[i+n] = ps[i] + S）
static ll S;           // 总长度

/* ================= (A) n <= 400：枚举断环起点 + 斜率优化 DP ================= */

static ll cur[405];                 // 旋转后的前缀和
static ll f[405], g[405];           // f[i]：前 i 个点分 t 块的最小 sum s^2
static ll hm[405], hb[405];         // 凸包直线：y = hm*x + hb
static int hsz;                     // 凸包大小

static inline ll lineVal(int i, ll x) { return hm[i] * x + hb[i]; }

// 直线按斜率严格递减的顺序加入（j 递增 => -2*cur[j] 递减）
static void hullAdd(ll m, ll b) {
    while (hsz >= 2) {
        ll m1 = hm[hsz - 2], b1 = hb[hsz - 2];
        ll m2 = hm[hsz - 1], b2 = hb[hsz - 1];
        // 若 line2 被 line1 与 line3 覆盖则弹出：x13 <= x12
        //   (b-b1)*(m1-m2) <= (b2-b1)*(m1-m)
        if ((b - b1) * (m1 - m2) <= (b2 - b1) * (m1 - m))
            hsz--;
        else
            break;
    }
    hm[hsz] = m;
    hb[hsz] = b;
    hsz++;
}

// 凸包上二分最小值（hull 上取值关于下标下凸）
static ll hullQuery(ll x) {
    int lo = 0, hi = hsz - 1;
    while (lo < hi) {
        int mid = (lo + hi) >> 1;
        if (lineVal(mid, x) <= lineVal(mid + 1, x))
            hi = mid;
        else
            lo = mid + 1;
    }
    return lineVal(lo, x);
}

static ll solveSmall() {
    ll best = INF;
    for (int d = 1; d <= n; d++) {  // 枚举断环起点
        cur[0] = 0;
        for (int i = 1; i <= n; i++) cur[i] = cur[i - 1] + a[d + i - 1];

        f[0] = 0;
        for (int i = 1; i <= n; i++) f[i] = INF;

        for (int t = 1; t <= k; t++) {
            hsz = 0;
            for (int i = 1; i <= n; i++) {
                int j = i - 1;  // 把 j = i-1 的直线加入后查询 i（保证只用到 j < i）
                if (f[j] < INF) hullAdd(-2 * cur[j], f[j] + cur[j] * cur[j]);
                g[i] = (hsz > 0) ? (hullQuery(cur[i]) + cur[i] * cur[i]) : INF;
            }
            for (int i = 0; i <= n; i++) f[i] = g[i];
        }
        if (f[n] < best) best = f[n];
    }
    return best;
}

/* ================= (B) n > 400, K = 2：双指针 ================= */

static ll solveK2() {
    ll best = INF;
    int j = 1;
    for (int i = 1; i <= n; i++) {
        // j 单调不减：权和 <= S/2 的最远右端点
        while (j <= i + n - 2 && (ps[j + 1] - ps[i - 1]) * 2 <= S) j++;
        if (j >= i) {  // 切点 j：第一段 [i..j]
            ll v = ps[j] - ps[i - 1];
            best = std::min(best, v * v + (S - v) * (S - v));
        }
        if (j + 1 >= i && j + 1 <= i + n - 1) {  // 切点 j+1（权略超 S/2 的一侧）
            ll v = ps[j + 1] - ps[i - 1];
            best = std::min(best, v * v + (S - v) * (S - v));
        }
    }
    return best;
}

/* ================= (C) n > 400, K = 3：双指针 + 二分 ================= */

static ll solveK3() {
    ll best = INF;
    int j = 1;
    for (int i = 1; i <= n; i++) {
        // 第一个切点：权和 <= S/3 的最远点 j
        while (j <= i + n - 2 && (ps[j + 1] - ps[i - 1]) * 3 <= S) j++;

        // 第二个切点：在 [j+1, i+n-1] 内找权和 <= S/3 的最远点 l；
        // 若不存在则 l 停留在 j+1（与参考实现一致，等价于取最小非空第二段）。
        int l = j + 1, r = i + n - 1;
        while (l < r) {
            int mid = (l + r + 1) >> 1;
            if ((ps[mid] - ps[j]) * 3 > S)
                r = mid - 1;
            else
                l = mid;
        }

        // 检查 l-1, l, l+1（第二段权和在 S/3 两侧的候选）
        for (int d = -1; d <= 1; d++) {
            int l2 = l + d;
            if (l2 < j + 1 || l2 > i + n - 2) continue;  // 保证三段均非空
            ll v1 = ps[j] - ps[i - 1];
            ll v2 = ps[l2] - ps[j];
            ll v3 = S - v1 - v2;
            if (v3 <= 0) continue;
            best = std::min(best, v1 * v1 + v2 * v2 + v3 * v3);
        }
    }
    return best;
}

/* ============================== 主程序 ============================== */

int main() {
    if (scanf("%d %d", &n, &k) != 2) return 0;
    for (int i = 1; i <= n; i++) {
        scanf("%lld", &a[i]);
        a[i + n] = a[i];
    }
    for (int i = 1; i <= 2 * n; i++) ps[i] = ps[i - 1] + a[i];
    S = ps[n];

    if (k <= 1) {  // 退化：只有一段，方差为 0
        printf("0\n");
        return 0;
    }
    if (k > n) return 0;  // 非法（题面保证 K <= N）

    ll minSumSq;
    if (n <= 400)
        minSumSq = solveSmall();
    else if (k == 2)
        minSumSq = solveK2();
    else
        minSumSq = solveK3();  // 题面数据：n>400 时 K 仅为 2 或 3

    lll ans = (lll)k * k * minSumSq - (lll)k * S * S;
    // 输出 __int128
    if (ans < 0) {
        putchar('-');
        ans = -ans;
    }
    char buf[64];
    int p = 0;
    if (ans == 0)
        buf[p++] = '0';
    while (ans > 0) {
        buf[p++] = char('0' + (int)(ans % 10));
        ans /= 10;
    }
    while (p > 0) putchar(buf[--p]);
    putchar('\n');
    return 0;
}
