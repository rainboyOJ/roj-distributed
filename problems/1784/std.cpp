// 一本通 1784《山谷》
//
// 来源说明（网络检索结论）
// ------------------------
// 按题面特征句做了精确检索，未找到任何公开题解/标程，故本题为**自研**实现：
//   * CSDN 站内搜索 API（https://so.csdn.net/api/v3/search）：
//       "一本通 1784 山谷"        -> total=4，全部无关（命中的是洛谷 P1784 数独）
//       "山谷 998244353 排列 矩阵 八连通" -> total=0
//       "山谷 八连通 排列 方案数"  -> total=0
//       "一本通 高手训练 动态规划 1784" -> 命中洛谷 P1784 数独等无关内容
//   * Bing（https://www.bing.com/search?q=...&format=rss）"一本通 1784 山谷" -> 无关结果
//   * 百度（https://www.baidu.com/s?wd=一本通 1784 山谷）-> 反爬空页
//   题面来自 .ybt-import/staging/1784/content.md（信息学奥赛一本通·高手训练篇 五、动态规划）。
//   故本标程不引用任何第三方代码，算法与推导全部为本文档内自证（下方给出完整推导）。
//
// 题意
// ----
// n*m 的格子填 1..nm 的一个排列；一个格子是"山谷"当且仅当它填的数严格小于所有与它
// 八连通的格子中的数。给定 '.'/'X' 矩阵，求"山谷集合恰好等于 X 所标格子"的排列数，
// 对 998244353 取模。多组数据（读到 EOF），每组一行答案。1<=n<=4, 1<=m<=7, 组数<=5。
//
// 推导（记 N = n*m，X 为山谷集合，V(p) 为排列 p 的山谷集合）
// ------------------------------------------------------------------
// 1) 排列 <-> 格子的一个全序（第 i 个位置放数 i）。于是
//      v 是山谷  <=>  v 在"它自己与所有邻居"中排最前。
// 2) 恰好等于 X：设 g(T) = #排列 使 T 中每个格子都是山谷（其余不约束），则
//      ans = sum_{T ⊇ X} (-1)^{|T|-|X|} g(T)。
//    T 内含相邻两格时约束互相矛盾（各要求自己在前），故 g(T)=0，只需枚举**独立集** T ⊇ X。
//    X 非独立 / X 为空时答案直接为 0（N>=2 时全局最小元必是山谷；1x1 无邻居时该格恒为山谷）。
// 3) 求 g(T)（T 独立，|T|=k，N-k 个非 T 格子）：这是"每个 t∈T 排在其所有邻居之前"的
//    偏序线性扩张计数。固定 T 的内部相对顺序 σ=(t_1..t_k)，再插入 N-k 个非 T 格子：
//      * 设 h(u)=σ 中 u 的最后一个邻居的下标（u 无 T-邻居则无约束），u 必须排在 t_{h(u)} 之后；
//      * 先按 h 递减插入"有约束"的格子：插第 j 个时，序列里所有已插入元素都在 t_{h(u_j)} 之后，
//        故可用位置数 = (k-h(u_j)) + (j-1) + 1 = k-h(u_j)+j；
//      * 再插入 F = #{u∉T : u 无 T-邻居} 个无约束格子：插第 i 个时可用位置数 = (N-F)+i，
//        连乘得 N!/(N-F)!。
//      按 h 分组（组 h 有 b_h 个），并用 C(Y)=#{u∉T : N(u)∩T ⊆ Y}（Y 为 T 的前缀集合）：
//        B_{>h} = #{u: h(u)>h} = (N-k) - C_h,  b_h = C_h - C_{h-1}
//      组 h 的连乘 = (k-h+B_{>h}+b_h)! / (k-h+B_{>h})! = (N-h-C_{h-1})!/(N-h-C_h)!。
//      于是
//        g(T) = (N!/(N-F)!) * sum_{σ} prod_{h=1..k} (N-h-C_{h-1})!/(N-h-C_h)!。
//    （已用若干小例子手工核对：1x3 的 {1,3} 得 2；1x3 的 {1} 得 3；1x4 的 {1,3} 得 5；
//      2x2 的 {角} 得 6，与题面两例 2 / 6 一致。）
// 4) 上式对 σ 的求和可用"子集 DP"完成：dp[Y] = 把 Y 作为前缀的所有顺序的乘积和，
//    由 Y 转移到 Y∪{s} 时乘 (N-|Y|-1-C(Y))!/(N-|Y|-1-C(Y∪{s}))!。最后 g(T)=dp[T]*(N!/(N-F)!)。
//    C(·) 用 cnt[mask]（mask=N(u)∩T 的压缩下标）+ 子集和（zeta）变换在 O(2^k*k) 内求出。
// 5) 枚举 T：DFS 只在"不与 X 相邻、也不与已选格子相邻"的候选格里选择，独立集规模 <= 8
//    （4x7 国王图最大独立集 = ceil(4/2)*ceil(7/2) = 8），4x7 全图独立集仅 16334 个、
//    含某固定格的仅 4749 个，总复杂度 ~ (独立集个数) * 2^k * k，最坏点毫秒级。
//
// 复杂度：每组数据 O(#独立集 T ⊇ X * (2^{|T|}*|T| + N*2^{|T|}))，N<=28，|T|<=8。

#include <cstdio>
#include <cstring>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;
static const ll MOD = 998244353;
static const int SAFE_N = 64;           // 安全系数：阶乘表开到 64

static ll fact[SAFE_N], invfact[SAFE_N];

static ll pw(ll b, ll e) { ll r = 1; b %= MOD; while (e) { if (e & 1) r = r * b % MOD; b = b * b % MOD; e >>= 1; } return r; }

static void init_fact() {
    fact[0] = 1;
    for (int i = 1; i < SAFE_N; i++) fact[i] = fact[i - 1] * i % MOD;
    invfact[SAFE_N - 1] = pw(fact[SAFE_N - 1], MOD - 2);
    for (int i = SAFE_N - 1; i > 0; i--) invfact[i - 1] = invfact[i] * i % MOD;
}

// 计算 g(T)：T 为独立集（bitmask，位=格子编号）
static ll gval(unsigned T, int N, const vector<unsigned> &adj) {
    vector<int> idx(N, -1);
    int k = 0;
    for (int v = 0; v < N; v++) if (T >> v & 1) idx[v] = k++;
    int sz = 1 << k;
    vector<int> C(sz, 0);
    for (int u = 0; u < N; u++) {
        if (T >> u & 1) continue;
        unsigned nb = adj[u] & T, m = 0;
        while (nb) { int b = __builtin_ctz(nb); nb &= nb - 1; m |= 1u << idx[b]; }
        C[m]++;
    }
    // 子集和（zeta）变换：C[Y] = #{u ∉ T : N(u)∩T ⊆ Y}
    for (int b = 0; b < k; b++)
        for (int Y = 0; Y < sz; Y++)
            if (Y >> b & 1) C[Y] += C[Y ^ (1 << b)];
    int F = C[0];                        // 无 T-邻居的格子数
    vector<ll> dp(sz, 0);
    dp[0] = 1;
    for (int Y = 0; Y < sz; Y++) {
        if (!dp[Y]) continue;
        int h = __builtin_popcount((unsigned)Y);
        int a = N - h - 1 - C[Y];        // >= k-h-1 >= 0
        for (int s = 0; s < k; s++) {
            if (Y >> s & 1) continue;
            int Y2 = Y | (1 << s);
            int b = N - h - 1 - C[Y2];
            dp[Y2] = (dp[Y2] + dp[Y] * fact[a] % MOD * invfact[b]) % MOD;
        }
    }
    return dp[sz - 1] * fact[N] % MOD * invfact[N - F] % MOD;
}

int main() {
    init_fact();
    int n, m;
    char buf[64];
    while (scanf("%d %d", &n, &m) == 2) {
        int N = n * m;
        unsigned X = 0;
        for (int i = 0; i < n; i++) {
            if (scanf("%63s", buf) != 1) return 0;
            for (int j = 0; j < m; j++) if (buf[j] == 'X') X |= 1u << (i * m + j);
        }
        vector<unsigned> adj(N, 0);
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            int v = i * m + j;
            for (int di = -1; di <= 1; di++) for (int dj = -1; dj <= 1; dj++) {
                if (!di && !dj) continue;
                int x = i + di, y = j + dj;
                if (x < 0 || x >= n || y < 0 || y >= m) continue;
                adj[v] |= 1u << (x * m + y);
            }
        }
        bool ok = (X != 0);
        for (int v = 0; v < N && ok; v++)
            if ((X >> v & 1) && (adj[v] & X)) ok = false;   // X 内相邻 -> 无解
        if (!ok) { printf("0\n"); continue; }

        // 候选格：不属于 X 且不与 X 相邻（保证 X ∪ Y 仍是独立集）
        unsigned candMask = 0;
        for (int v = 0; v < N; v++)
            if (!(X >> v & 1) && !(adj[v] & X)) candMask |= 1u << v;
        vector<int> cand;
        for (int v = 0; v < N; v++) if (candMask >> v & 1) cand.push_back(v);

        ll ans = 0;
        // 枚举独立集 Y ⊆ cand，T = X ∪ Y，贡献 (-1)^{|Y|} g(T)
        // 迭代式枚举（避免深递归）：栈帧 (pos, chosenY, forbidden)
        struct Frame { int pos; unsigned chosen, forb; };
        vector<Frame> st;
        st.push_back({0, 0u, 0u});
        while (!st.empty()) {
            Frame f = st.back(); st.pop_back();
            if (f.pos == (int)cand.size()) {
                unsigned T = X | f.chosen;
                ll g = gval(T, N, adj);
                int ycnt = __builtin_popcount(f.chosen);
                if (ycnt & 1) ans = (ans - g + MOD) % MOD; else ans = (ans + g) % MOD;
                continue;
            }
            // 不选 cand[f.pos]
            st.push_back({f.pos + 1, f.chosen, f.forb});
            // 选 cand[f.pos]
            int c = cand[f.pos];
            if (!(f.forb >> c & 1))
                st.push_back({f.pos + 1, f.chosen | (1u << c),
                              f.forb | (adj[c] & candMask)});
        }
        printf("%lld\n", ans % MOD);
    }
    return 0;
}
