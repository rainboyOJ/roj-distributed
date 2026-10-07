// 一本通 1768《交换》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 本题按任务书要求先联网检索 C++ 解法。题面特征句「一个{0, 1, 2 , … , n - 2}的排列 q
// 被认为是优美的排列」+ 题名「交换」精确命中下列来源（题面、样例、数据范围 30% n<=10 /
// 100% n<=50 逐字一致），代码按题面口径改写为「区间 DP + 组合数」版本（非盲抄）：
//   [1] https://www.cnblogs.com/FYH-SSGSS/p/7353901.html
//       《[题解] 交换》—— 原始题解（本轮的规范来源）。核心论述：
//       「控制交换次数为 n-1 …… 考虑倒着处理：交换 (i, i+1) 之后，前面的数下标恒 <= i，
//        后面的数恒 > i，所以最后一次交换前必须 [左边全是小数 / 右边全是大数]，
//        于是归结成两个互不干涉的子问题」；转移
//        dp[L][R] += dp[L][k] * dp[k+1][R] * C(R-L-1, k-L)，
//        并给出预处理组合数（同一篇文章内含 n<=10 的 dfs 暴力拿 30% 分）。
//   [2] https://blog.csdn.net/xin13261615514/article/details/101549410
//       《某次模拟赛 交换》—— CSDN 转载件（文末注明「转载于 cnblogs/FYH-SSGSS」），
//       题面与 [1] 逐字相同，DP 源码一致，互为交叉印证。
// 说明：来源正文的转移式行文写作 C(R-L, k-L-1)，而其代码写的是 C(R-L-1, i-L)；
// 两者不等价，经样例与手算小例（n=3/4/5，见 gen-report.md §4）核实，**代码里的
// C(R-L-1, k-L) 才是正确形式**（含义：左子区间 k-L 条边与右子区间 R-k-1 条边
// 在「本区间最后一次交换」之前的交错方案数 = C((k-L)+(R-k-1), k-L)）。
// =============================================================================
//
// 题面数据范围：第一行 n；第二行 n 个整数（p 是 {0..n-1} 的排列）。
//   30% 数据 n <= 10；100% 数据 n <= 50。限制 1000 ms / 256 MB（config.json）。
//
// 算法（区间 DP）：
//   记区间 [L,R] 的「内容」c[L..R] 为：当前该区间内各位置上站着的元素（恒为 {L..R} 的一个排列）。
//   把区间 [L,R] 内 R-L 条边各用一次、从恒等排列 [L,L+1,...,R] 变成内容 c 的方案数记作 f(L,R,c)。
//   设最后一次（区间内最后一条被使用的）边为 k（L <= k < R），它交换位置 k,k+1，
//   因此交换前的状态 A = swap(c, k)。交换 k 之后，左块 [L,k] 的元素再也不可能跑到右块
//   （右块同理），所以必须且只需 A[L..k] = {L..k}（值域对齐），此后左右两子问题完全独立。
//   剩余 R-L-1 条边中，左子区间占 k-L 条、右子区间占 R-k-1 条，它们可任意交错且互不干涉，
//   方案数 C(R-L-1, k-L)。故
//        f(L,R,c) = Σ_{k 满足 A[L..k]={L..k}} C(R-L-1, k-L) * f(L,k,A[L..k]) * f(k+1,R,A[k+1..R])
//   边界 f(L,L,c) = [c[L]==L]。答案 = f(0,n-1,p)。
//
//   关键实现细节（对来源代码的等价改写）：可以证明（gen-report.md §4.2）对任意合法（可达）
//   区间 [L,R]，其内容恒形如 c[L..R] = [x, p[L+1], p[L+2], ..., p[R-1], y]，
//   即「区间内部位置的值就是原排列 p 的值」，只有两个端点 x=c[L]、y=c[R] 可能被祖先的
//   交换"推"进来；且 {x,y} = {L..R} \ {p[L+1..R-1]}，x 由路径唯一确定（来源代码用
//   in-place swap(p[i],p[i+1]) 隐式携带该信息）。这里把端点 x 显式写进 DP 状态
//   （y 由 x 与内部值唯一确定），避免依赖原地修改与记忆化的耦合，等价且更好自证。
//   状态数 O(n^3)，每个状态枚举 O(n) 个 k，总复杂度 O(n^4) 但常数极小（n<=50 实测 <1 ms）。
//
// 取模：答案对 1e9+7 取模，组合数与 DP 值全部用 long long 存取。

#include <cstdio>
#include <cstring>

static const long long MOD = 1000000007LL;
static const int MAXN = 55;

static int n;
static int p[MAXN];
static long long Cbin[MAXN][MAXN];      // 组合数（Pascal，模 MOD）
static long long memo[MAXN][MAXN][MAXN]; // memo[L][R][cL]
static bool done[MAXN][MAXN][MAXN];

// f(L,R,cL)：区间 [L,R]，其内容左端点为 cL（右端点由内部值唯一确定）时的方案数。
static long long solve(int L, int R, int cL) {
    if (L == R) return (cL == L) ? 1 : 0;
    if (done[L][R][cL]) return memo[L][R][cL];
    done[L][R][cL] = true;

    long long res = 0;
    static bool used[MAXN];
    for (int v = L; v <= R; v++) used[v] = false;

    bool ok = (L <= cL && cL <= R);
    if (ok) used[cL] = true;
    // 内部位置 L+1..R-1 的值必须落在 [L,R] 内且互不相同（p 本身是排列，只需查值域）
    for (int j = L + 1; j <= R - 1 && ok; j++) {
        int v = p[j];
        if (v < L || v > R || used[v]) ok = false;
        else used[v] = true;
    }
    if (ok) {
        int cR = -1;                       // 剩下的那个值就是右端点
        for (int v = L; v <= R; v++) if (!used[v]) { cR = v; break; }
        // 内容查询：content(j)
        // 用显式分支代替 lambda，避免捕获开销；逻辑与 lambda 相同
        // content(j) = cL (j==L) / cR (j==R) / p[j] (otherwise)
        for (int k = L; k <= R - 1; k++) {
            // 检查交换位置 k,k+1 后 A[L..k] 的值域 == {L..k}
            bool good = true;
            for (int j = L; j <= k - 1; j++) {
                int a = (j == L) ? cL : p[j];
                if (a < L || a > k) { good = false; break; }
            }
            if (good) {
                int a = (k + 1 == R) ? cR : p[k + 1];   // A[k] = content(k+1)
                if (a < L || a > k) good = false;
            }
            if (!good) continue;

            int leftcL = (k == L) ? ((L + 1 == R) ? cR : p[L + 1]) : cL;  // A[L]
            int rightcL = (k == L) ? cL : p[k];                           // A[k+1] = content(k)
            long long sub = solve(L, k, leftcL) * solve(k + 1, R, rightcL) % MOD;
            sub = sub * Cbin[R - L - 1][k - L] % MOD;
            res = (res + sub) % MOD;
        }
    }
    memo[L][R][cL] = res;
    return res;
}

int main() {
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) scanf("%d", &p[i]);

    memset(Cbin, 0, sizeof(Cbin));
    for (int i = 0; i <= n; i++) {
        Cbin[i][0] = 1;
        for (int j = 1; j <= i; j++)
            Cbin[i][j] = (Cbin[i - 1][j - 1] + Cbin[i - 1][j]) % MOD;
    }

    printf("%lld\n", solve(0, n - 1, p[0]) % MOD);
    return 0;
}
