// 一本通 2142《树边匹配》标程
// 题意：给定 n 个节点的树，选出一个边集，使每个节点至多是其中一条边的端点，
//       求最多能选多少条边（树的（最大）匹配数）。
//
// 思路：树形 DP（树的最大匹配）。
//   记 best[u] = 以 u 为根的子树上能选出的最大边数；
//   记 dp0[u] = 「u 不与任何儿子配对」时子树 u 的最大匹配数；
//   记 dp1[u] = 「u 恰好与一个儿子配对」时子树 u 的最大匹配数。
//   令儿子集合为 ch(u)，则
//     dp0[u] = Σ_{v∈ch(u)} best[v]                       （儿子各自独立自由决定）
//     dp1[u] = dp0[u] + max_v ( dp0[v] - best[v] ) + 1
//            （选 v 与 u 配对：v 因此不能再与它的儿子配对，贡献由 best[v] 换成
//              dp0[v]，再加上边 (u,v) 本身）
//     best[u] = max(dp0[u], dp1[u])
//   叶子 dp1 = -inf（无儿子可配）；答案为 best[1]（根为 1）。
//   复杂度 O(n)。
//
// 实现细节：n 最大 2e5，链形数据的递归深度可达 2e5，为规避递归爆栈，
//   不使用递归 DFS：先做显式栈的迭代 DFS 得到前序序列，再倒序（儿子先于
//   父亲）自底向上递推 DP。邻接表用 CSR（计数排序）数组，避免 vector 开销。
//
// 参考来源（联网检索的网络题解，按题面自行改写并编译验证，非盲抄）：
//   1) https://blog.csdn.net/kejin2019/article/details/121181729
//      《【Ybtoj】【NOIP2021 模拟赛 B 组 Day8】最大匹配【树形DP】》
//      给出 f[x]=Σff[y]、ff[x]=max(f[x], max_y(f[x]-ff[y]+f[y]+1)) 的转移
//      （与本文 dp0/best 记号对应），本文据此改写并补充边界处理。
//   2) https://blog.csdn.net/winchester_/article/details/51938993
//      《vijos 1892 树上的最大匹配问题 树形dp》
//      给出 f[i][0]/f[i][1]（i 是否与父亲边相连）的树形 DP 转移。
//   3) https://blog.csdn.net/weixin_45674669/article/details/163333847
//      《【题解-信息学奥赛一本通】2142：树边匹配》
//      本题题解页：指出枚举边集（2^(n-1) 子集）会超时，正解为树形 DP。
//   三处来源结论一致，与题面一致，无冲突。

#include <cstdio>
#include <vector>
#include <algorithm>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    if (n <= 1) {                 // 只有一个节点的树：没有边可选
        printf("0\n");
        return 0;
    }

    std::vector<int> ea(n - 1), eb(n - 1), cnt(n + 2, 0);
    for (int i = 0; i < n - 1; ++i) {
        int a, b;
        scanf("%d %d", &a, &b);
        ea[i] = a;
        eb[i] = b;
        ++cnt[a];
        ++cnt[b];
    }

    // CSR 邻接表
    std::vector<int> start(n + 2, 0), cur(n + 2, 0), adj(2 * (n - 1));
    for (int i = 1; i <= n; ++i) start[i + 1] = start[i] + cnt[i];
    cur = start;
    for (int i = 0; i < n - 1; ++i) {
        adj[cur[ea[i]]++] = eb[i];
        adj[cur[eb[i]]++] = ea[i];
    }

    // 迭代 DFS（显式栈）：得到前序序列 order 与 parent
    std::vector<int> parent(n + 1, 0), order;
    std::vector<char> visited(n + 1, 0);
    order.reserve(n);
    std::vector<int> stk;
    stk.reserve(n);
    parent[1] = 0;                // 0 不是合法节点编号，作哨兵
    visited[1] = 1;
    stk.push_back(1);
    while (!stk.empty()) {
        int u = stk.back();
        stk.pop_back();
        order.push_back(u);
        for (int i = start[u]; i < start[u + 1]; ++i) {
            int v = adj[i];
            if (visited[v]) continue;   // 树上唯一已访问邻点是父亲
            visited[v] = 1;
            parent[v] = u;
            stk.push_back(v);
        }
    }

    const int NEG = -1000000000;  // -inf 哨兵
    std::vector<int> dp0(n + 1, 0), dp1(n + 1, 0), best(n + 1, 0);
    for (int idx = n - 1; idx >= 0; --idx) {   // 逆前序 = 儿子先于父亲
        int u = order[idx];
        int sumBest = 0;
        int bestDelta = NEG;      // max_{v∈ch(u)} (dp0[v] - best[v]) <= 0
        for (int i = start[u]; i < start[u + 1]; ++i) {
            int v = adj[i];
            if (v == parent[u]) continue;
            sumBest += best[v];
            int delta = dp0[v] - best[v];
            if (delta > bestDelta) bestDelta = delta;
        }
        dp0[u] = sumBest;
        dp1[u] = (bestDelta == NEG) ? NEG : sumBest + bestDelta + 1;
        best[u] = std::max(dp0[u], dp1[u]);
    }

    printf("%d\n", best[1]);
    return 0;
}
