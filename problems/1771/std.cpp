/*
 * std.cpp  --  一本通 1771 《仓库选址》
 *              (同源经典题: 小奇的仓库 / warehouse, CSP-S 模拟测试, 换根 DP)
 *
 * 来源 / 依据:
 *   题面: .ybt-import/staging/1771/content.md  (一本通·高手训练 动态规划)
 *   参考题解与代码: https://www.cnblogs.com/Bn_ff/p/13225513.html
 *       (博客园 "【题解】test0628 仓库选址 - 换根 dp - 二进制运算", 题头标注 ybt 1771)
 *   同源题确认: 小奇的仓库(warehouse), 见 https://www.cnblogs.com/My-flurry/p/11421752.html
 *       "喵星系 n 个星球构成树, 花费 dis(a,b) xor M, 求每点到其余所有点花费之和"
 *
 * 思路:
 *   要求 ans[i] = sum_j ( dis(i,j) xor M ).  由于 M <= 15, 异或只影响二进制低 4 位,
 *   即 (dis xor M) = dis - (dis mod 16) + ((dis mod 16) xor M).
 *   于是:
 *     1) 一次换根 DP 求出 sumdis[i] = sum_j dis(i,j)  (含 j=i 的 0 贡献);
 *     2) 同时维护 g[i][r] = 满足 dis(i,j) mod 16 == r 的 j 的个数 (含 i 自身);
 *     3) ans[i] = sumdis[i] + sum_r ( (r xor M) - r ) * ( g[i][r] - (r==0 ? 1 : 0) ),
 *        其中 (r==0 ? 1 : 0) 扣掉 i 自己.
 *   复杂度 O(16n), 空间 O(16n).
 *
 *   说明: 原题解用递归 DFS; 本实现改为迭代 DFS (显式栈 + 先序/逆序), 以免链状数据爆栈,
 *         结果与题解等价。
 */

#include <cstdio>
#include <vector>
#include <array>
#include <utility>
using namespace std;

int main() {
    int n;
    long long M;
    if (scanf("%d %lld", &n, &M) != 2) return 0;

    vector<vector<pair<int, long long>>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int a, b;
        long long c;
        scanf("%d %d %lld", &a, &b, &c);
        adj[a].push_back({b, c});
        adj[b].push_back({a, c});
    }

    /* ---------- 迭代先序遍历, 得到 parent / 到父亲的边权 / 先序 order ---------- */
    vector<int> parent(n + 1, 0), order;
    vector<long long> pedge(n + 1, 0);
    vector<char> vis(n + 1, 0);
    order.reserve(n);
    vector<int> st;
    st.push_back(1);
    vis[1] = 1;
    while (!st.empty()) {
        int x = st.back();
        st.pop_back();
        order.push_back(x);
        for (auto &pr : adj[x]) {
            int y = pr.first;
            if (!vis[y]) {
                vis[y] = 1;
                parent[y] = x;
                pedge[y] = pr.second;
                st.push_back(y);
            }
        }
    }

    /* ---------- 子树 DP: g[i][r] 为子树内点数, dp[i] 为子树内距离和 ---------- */
    vector<array<long long, 16>> g(n + 1);
    vector<long long> dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        g[i].fill(0);
        g[i][0] = 1; /* 自己, 距离 0 */
    }
    for (int idx = (int)order.size() - 1; idx >= 1; --idx) {
        int x = order[idx];
        int p = parent[x];
        long long e = pedge[x];
        int ee = (int)(e % 16);
        long long sz = 0;
        for (int r = 0; r < 16; ++r) sz += g[x][r];
        dp[p] += dp[x] + sz * e;
        for (int r = 0; r < 16; ++r) g[p][(r + ee) % 16] += g[x][r];
    }

    /* ---------- 换根 DP: 由父节点信息推出子节点的全局 dp / g ---------- */
    for (int idx = 1; idx < (int)order.size(); ++idx) {
        int x = order[idx];
        int p = parent[x];
        long long e = pedge[x];
        int ee = (int)(e % 16);
        array<long long, 16> tmp;
        tmp.fill(0);
        long long sz = 0;
        for (int r = 0; r < 16; ++r) sz += g[x][r];
        for (int j = 0; j < 16; ++j) {
            int sub = ((j - ee) % 16 + 16) % 16; /* 子树的贡献在 g[p] 中落在 j-ee */
            long long rest = g[p][j] - g[x][sub];
            tmp[(j + ee) % 16] += rest;
        }
        dp[x] = dp[p] + (long long)(n - 2 * sz) * e;
        for (int r = 0; r < 16; ++r) g[x][r] += tmp[r];
    }

    /* ---------- 统计答案 ---------- */
    for (int i = 1; i <= n; ++i) {
        long long ans = dp[i];
        for (int r = 0; r < 16; ++r) {
            long long cnt = g[i][r] - (r == 0 ? 1 : 0);
            ans += ((long long)(r ^ (int)M) - r) * cnt;
        }
        printf("%lld\n", ans);
    }
    return 0;
}
