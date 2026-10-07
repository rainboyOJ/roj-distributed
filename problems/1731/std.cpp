// ============================================================================
// 一本通 1731《最大流》 标程
// ----------------------------------------------------------------------------
// 原题出处：BZOJ 4435 / CERC 2015 Problem J "Juice Junctions"
//   与本题目面逐字同源（n 点 m 边无向图、无重边自环、每个点度数 <= 3、每条边容量 1、
//   求所有点对 i<j 之间最大流之和；2 <= n <= 3000, 0 <= m <= floor(3n/2)）。
//
// 解法来源（联网检索；命中方式 = 题面特征句「保证所有点的度数都不超过3」+
// 「任意两点间的最大流」+「所有点对间最大流的和」精确匹配到同题）：
//   [1] https://blog.csdn.net/abcyan1235/article/details/101608585
//       《[BZOJ4435][Cerc2015]Juice Junctions》 (CSDN / abcyan1235, 2019)
//   [2] https://blog.csdn.net/ronaldo7_zyb/article/details/106618651
//       《『毒瘤算法系列12』最大流(边双连通分量·哈希)》 (CSDN / ronaldo7_zyb, 2020)
//   [3] https://blog.csdn.net/u013578420/article/details/81915440
//       《[Codeforces Gym - 101480J] Juice Junctions》 (CSDN, 2018)
//   三篇题解结论一致（互为印证）：由最大流最小割定理 + deg <= 3 得
//     flow(i,j) ∈ {0,1,2,3}，且
//       flow(i,j) >= 1  <=>  i,j 在原图中连通
//       flow(i,j) >= 2  <=>  i,j 属于同一「边双连通分量」(2-边连通)
//       flow(i,j) >= 3  <=>  对原图每条边 e，i,j 在 G-e 中仍属于同一边双连通分量
//   记 cntk = #{(i<j) : flow(i,j) >= k}，则 答案 = cnt1 + cnt2 + cnt3。
//   复杂度 O(m*(n+m)) 左右（n=3000,m=4500 时约 3e7 基本操作），3s/256MB 内轻松通过。
//
// 本实现说明（按上述解法重写，非照抄）：
//   * 参考代码用递归 Tarjan + 数组邻接表 + 双重哈希表示「删边后的分量指纹」。
//     本实现改为：
//       - 迭代式（显式栈）Tarjan 求桥 + 忽略桥的 flood-fill 求边双分量（无递归深度风险）；
//       - 不用哈希：对每组删边结果做「等价类精化」(rank refinement)，
//         即按 (上一轮 rank, 本轮边双编号) 排序重新编号，m 轮后 rank 相同
//         <=> 每一轮删边后都同分量 <=> flow >= 3。全程确定性，无哈希冲突可能；
//   * 全部数据用 std::vector 按题面上限动态开（无定长数组、无越界段错误风险）；
//   * 退化情形特判：m == 0 时不存在任何「删一条边」的检验，cnt3 = 0。
//
// 编译：g++ -O2 -std=c++17 std.cpp -o std      （无外部依赖，仅用标准库）
// 运行：./std < input.txt
// ============================================================================

#include <algorithm>
#include <cstdio>
#include <vector>

using namespace std;

static int n, m;
static vector<int> eu, ev;          // 第 i 条边的两个端点（边编号 0..m-1）
static vector<vector<int>> adj;     // 邻接表（存边编号）

// ---------------------------------------------------------------------------
// 求「删去第 banId 条边后」图的边双连通分量编号（banId < 0 表示不删边）。
// 做法：迭代式 Tarjan 标出所有桥，然后忽略桥与被删边做 flood-fill；
// 每块即一个边双连通分量（不含桥的连通块）。
// ---------------------------------------------------------------------------
static vector<int> edgeBiconnected(int banId) {
    vector<int> dfn(n + 1, 0), low(n + 1, 0), parEdge(n + 1, -1), it(n + 1, 0);
    vector<unsigned char> isBridge(m, 0);
    vector<int> path, stackEdge;    // 显式 DFS 栈 + 栈上顶点的入边编号
    path.reserve(n);
    stackEdge.reserve(n);

    int timer = 0;
    for (int s = 1; s <= n; ++s) {                 // 图可以不连通，逐连通块 DFS
        if (dfn[s]) continue;
        dfn[s] = low[s] = ++timer;
        parEdge[s] = -1;
        it[s] = 0;
        path.clear();
        stackEdge.clear();
        path.push_back(s);
        stackEdge.push_back(-1);
        while (!path.empty()) {
            int u = path.back();
            if (it[u] < (int)adj[u].size()) {
                int e = adj[u][it[u]++];
                if (e == banId) continue;                          // 该边被删除
                int v = (eu[e] == u) ? ev[e] : eu[e];
                if (!dfn[v]) {                                     // 树边
                    dfn[v] = low[v] = ++timer;
                    parEdge[v] = e;
                    it[v] = 0;
                    path.push_back(v);
                    stackEdge.push_back(e);
                } else if (e != parEdge[u] && dfn[v] < low[u]) {    // 回边（指向祖先）
                    low[u] = dfn[v];
                }
            } else {                                               // 回溯
                int pe = stackEdge.back();
                path.pop_back();
                stackEdge.pop_back();
                if (!path.empty()) {
                    int p = path.back();
                    if (low[u] > dfn[p]) isBridge[pe] = 1;          // 树边 (p,u) 是桥
                    if (low[u] < low[p]) low[p] = low[u];
                }
            }
        }
    }

    vector<int> bel(n + 1, 0);
    vector<int> stk;
    stk.reserve(n);
    int comp = 0;
    for (int s = 1; s <= n; ++s) {                 // 忽略桥/被删边，逐块 flood-fill
        if (bel[s]) continue;
        bel[s] = ++comp;
        stk.push_back(s);
        while (!stk.empty()) {
            int u = stk.back();
            stk.pop_back();
            for (int e : adj[u]) {
                if (e == banId || isBridge[e]) continue;
                int v = (eu[e] == u) ? ev[e] : eu[e];
                if (!bel[v]) {
                    bel[v] = comp;
                    stk.push_back(v);
                }
            }
        }
    }
    return bel;
}

// 统计「编号相同的点对」个数（某等价关系下的点对数）
static long long countEqualPairs(const vector<int>& id) {
    vector<int> v(id.begin() + 1, id.end());
    sort(v.begin(), v.end());
    long long res = 0;
    for (size_t i = 0; i < v.size();) {
        size_t j = i;
        while (j < v.size() && v[j] == v[i]) ++j;
        long long c = (long long)(j - i);
        res += c * (c - 1) / 2;
        i = j;
    }
    return res;
}

int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    eu.assign(m, 0);
    ev.assign(m, 0);
    adj.assign(n + 1, {});
    for (int i = 0; i < m; ++i) {
        int x, y;
        if (scanf("%d %d", &x, &y) != 2) return 0;
        eu[i] = x;
        ev[i] = y;
        adj[x].push_back(i);
        adj[y].push_back(i);
    }

    // ---- cnt1：连通分量（并查集）=> flow >= 1 的点对数 --------------------
    vector<int> fa(n + 1);
    for (int i = 1; i <= n; ++i) fa[i] = i;
    for (int i = 0; i < m; ++i) {
        int a = eu[i], b = ev[i];
        while (fa[a] != a) a = fa[a] = fa[fa[a]];          // 路径折半
        while (fa[b] != b) b = fa[b] = fa[fa[b]];
        if (a != b) fa[a] = b;
    }
    vector<int> cc(n + 1);
    for (int i = 1; i <= n; ++i) {
        int a = i;
        while (fa[a] != a) a = fa[a] = fa[fa[a]];
        cc[i] = a;
    }
    long long cnt1 = countEqualPairs(cc);

    // ---- cnt2：原图（不删边）边双连通分量 => flow >= 2 的点对数 -----------
    long long cnt2 = countEqualPairs(edgeBiconnected(-1));

    // ---- cnt3：flow >= 3 <=> 删去任一条边后仍同一边双分量 -----------------
    // 等价类精化：rank[v] 记录 v 的"历史指纹秩"。每轮按 (rank[v], bel[v]) 排序后
    // 重新赋秩；m 轮后 rank 相同的点对 <=> 每一轮删边后都处于同一分量 <=> flow = 3。
    // 注：m 轮里已包含"删桥"的情形，足以保证这些点对在原图中也 2-边连通（见证明略）。
    long long cnt3 = 0;
    if (m > 0) {
        vector<int> rank(n + 1, 0);
        vector<pair<pair<int, int>, int>> key(n);           // ((rank, bel), 顶点)
        for (int ban = 0; ban < m; ++ban) {
            vector<int> bel = edgeBiconnected(ban);
            for (int i = 1; i <= n; ++i)
                key[i - 1] = make_pair(make_pair(rank[i], bel[i]), i);
            sort(key.begin(), key.end());
            int r = 0;
            for (int i = 0; i < n; ++i) {
                if (i > 0 && key[i].first != key[i - 1].first) ++r;
                rank[key[i].second] = r;
            }
        }
        cnt3 = countEqualPairs(rank);
    }

    // ---- 答案 = cnt1 + cnt2 + cnt3 ---------------------------------------
    printf("%lld\n", cnt1 + cnt2 + cnt3);
    return 0;
}
