// 一本通 1756《过路费》标准程序 (std)
// 题意：无向连通图，n 点 m 边，边权 w。每次询问 (S,T)，求一条 S->T 的路径
//       使得路径上边权的最大值最小，输出该最小值。
//
// 算法（自研，依据经典结论「最小瓶颈路径」）：
//   1) 求最小生成树(MST)：任何一棵 MST 都是最小瓶颈生成树，即对于任意点对
//      (u,v)，MST 上 u-v 路径的最大边权 = 全图中所有 u-v 路径最大边权的最小值。
//      （证明：Kruskal 从小到大加边，第一次使 u,v 连通的那条边的权即为答案，
//       而这条边恰好进入 MST。）
//   2) 在 MST 上做倍增 LCA，同时维护「向上 2^k 步路径上的最大边权」。
//   3) 每次询问在求 LCA 的过程中合并两侧的最大边权即为答案；S==T 时为 0。
//
// 复杂度：O(m log m + (n+q) log n)。
//
// 参考/同源说明：本题为经典「最小瓶颈路径 / 瓶颈生成树」题，
//   与洛谷 P2245《星际导航》等价（点对路径上最大边权最小化），亦为
//   最小生成树 + 树上路径最值（倍增/树剖）模板。无网络检索工具可用，
//   故按上述经典结论自研实现；实现后在题面样例上验证通过。
//   来源依据：最小生成树即最小瓶颈生成树（算法导论 / OI-Wiki「最小生成树」）。

#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <utility>
using namespace std;

struct Edge {
    int u, v;
    long long w;
};

int n, m, q;
vector<Edge> edges;
vector<int> par;

int find(int x) {
    while (par[x] != x) {
        par[x] = par[par[x]];
        x = par[x];
    }
    return x;
}

int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    edges.resize(m);
    for (int i = 0; i < m; i++) {
        int a, b;
        long long w;
        scanf("%d %d %lld", &a, &b, &w);
        edges[i] = {a, b, w};
    }

    // Kruskal 求 MST
    sort(edges.begin(), edges.end(), [](const Edge &x, const Edge &y) {
        return x.w < y.w;
    });
    par.resize(n + 1);
    for (int i = 1; i <= n; i++) par[i] = i;

    vector<vector<pair<int, long long>>> adj(n + 1);
    for (const Edge &e : edges) {
        int ru = find(e.u), rv = find(e.v);
        if (ru == rv) continue;  // 自环或成环，跳过
        par[ru] = rv;
        adj[e.u].push_back({e.v, e.w});
        adj[e.v].push_back({e.u, e.w});
    }

    // 倍增预处理
    int LOG = 1;
    while ((1 << LOG) <= n) LOG++;
    if (LOG < 1) LOG = 1;
    vector<vector<int>> up(LOG, vector<int>(n + 1, 1));
    vector<vector<long long>> mx(LOG, vector<long long>(n + 1, 0));
    vector<int> depth(n + 1, 0);
    vector<char> vis(n + 1, 0);

    // 迭代 BFS/DFS 建树（避免深链递归爆栈）
    vector<int> stk;
    stk.reserve(n);
    stk.push_back(1);
    vis[1] = 1;
    up[0][1] = 1;
    mx[0][1] = 0;
    while (!stk.empty()) {
        int u = stk.back();
        stk.pop_back();
        for (auto &pr : adj[u]) {
            int v = pr.first;
            if (vis[v]) continue;
            vis[v] = 1;
            depth[v] = depth[u] + 1;
            up[0][v] = u;
            mx[0][v] = pr.second;
            stk.push_back(v);
        }
    }
    // 处理极端情况：若还有未访问点（题面保证连通，这里仅防御），指向自身
    for (int k = 1; k < LOG; k++) {
        for (int v = 1; v <= n; v++) {
            up[k][v] = up[k - 1][up[k - 1][v]];
            mx[k][v] = max(mx[k - 1][v], mx[k - 1][up[k - 1][v]]);
        }
    }

    if (scanf("%d", &q) != 1) return 0;
    string out;
    out.reserve((size_t)q * 12);
    char buf[16];
    while (q--) {
        int s, t;
        scanf("%d %d", &s, &t);
        long long ans = 0;
        if (s != t) {
            int a = s, b = t;
            if (depth[a] < depth[b]) swap(a, b);
            int diff = depth[a] - depth[b];
            for (int k = 0; k < LOG; k++) {
                if ((diff >> k) & 1) {
                    ans = max(ans, mx[k][a]);
                    a = up[k][a];
                }
            }
            if (a != b) {
                for (int k = LOG - 1; k >= 0; k--) {
                    if (up[k][a] != up[k][b]) {
                        ans = max(ans, mx[k][a]);
                        ans = max(ans, mx[k][b]);
                        a = up[k][a];
                        b = up[k][b];
                    }
                }
                ans = max(ans, mx[0][a]);
                ans = max(ans, mx[0][b]);
            }
        }
        int len = snprintf(buf, sizeof(buf), "%lld\n", ans);
        out.append(buf, len);
    }
    fwrite(out.data(), 1, out.size(), stdout);
    return 0;
}
