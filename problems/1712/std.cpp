// 一本通 1712《汉堡店》标程
// ---------------------------------------------------------------------------
// 来源说明：本题（一本通·高手训练 图论）在网络（CSDN 站内搜索「一本通 1712 汉堡店」、
//   「一本通 高手训练 汉堡店」、Bing）未检索到公开题解/AC 代码，故为自研，
//   依据题面推导 + 同型经典题「最小生成树强制包含某条边（删边最小生成树）」改写：
//     CSDN《删边最小生成树》 https://blog.csdn.net/qq_35392050/article/details/52863169
//     经典结论：设 T0 为原图 MST，e=(u,v) 为任意一条边，
//       含 e 的最小生成树权值 = W(T0)              ，若 e ∈ T0；
//                              = W(T0) - maxEdge(u,v in T0) + w(e)，若 e ∉ T0。
//       （加 e 成环，删去环上最重边即为最优，即 MST 的「替换」性质。）
// ---------------------------------------------------------------------------
// 题意与推导：
//   完全图中每对 (i,j) 的边权 = 欧氏距离。选一棵生成树 T（N-1 条边），再选 T 中
//   一条边 (a,b) 把两家店吃光，愉悦度 = A / B，其中
//     A = P_a + P_b，
//     B = 新图中除 (a,b) 外所有道路（即 T 的其余 N-2 条边）的权值之和 = W(T) - w(a,b)。
//   求 A/B 的最大值。
//   对固定的点对 (a,b)：A 固定，要使 A/B 最大即要 B 最小，也就是
//     B_min(a,b) = (含边 (a,b) 的最小生成树权值) - w(a,b)。
//   由上面的经典替换结论，取 T0 = 全图 MST（权值 W），则对任意点对 (u,v)：
//     B_min(u,v) = W - maxEdgeOnTreePath(u,v)。
//   （u,v 在 T0 中相邻时 maxEdge = w(u,v)，B = W - w(u,v)，与定义一致。）
//   于是答案 = max_{u<v} (P_u + P_v) / (W - maxEdgeOnTreePath(u,v))。
//   复杂度：Kruskal O(N^2 log N)，从每个点 DFS 求树路径最大边 O(N^2)，总 O(N^2 log N)，
//   N ≤ 1000 时约 5×10^5 条边，远低于 1000ms / 256MB 限制。
// ---------------------------------------------------------------------------
// 数据范围（题面）：2 < N ≤ 1000，0 ≤ X,Y ≤ 1000，0 < P < 10000，输出保留两位小数。
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <vector>

using namespace std;

struct Edge {
    int u, v;
    double w;
    bool operator<(const Edge &o) const { return w < o.w; }
};

static int par[1024];

static int find(int x) {
    while (par[x] != x) {
        par[x] = par[par[x]];
        x = par[x];
    }
    return x;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<double> X(n), Y(n), P(n);
    for (int i = 0; i < n; ++i) {
        long long x, y, p;
        scanf("%lld %lld %lld", &x, &y, &p);
        X[i] = (double)x;
        Y[i] = (double)y;
        P[i] = (double)p;
    }

    // 完全图边表
    vector<Edge> es;
    es.reserve((size_t)n * (n - 1) / 2);
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j) {
            double dx = X[i] - X[j], dy = Y[i] - Y[j];
            es.push_back(Edge{i, j, sqrt(dx * dx + dy * dy)});
        }
    sort(es.begin(), es.end());

    // Kruskal 求 MST，同时建树（邻接表）
    vector<vector<pair<int, double>>> tree(n);
    for (int i = 0; i < n; ++i) par[i] = i;
    double W = 0.0;
    int used = 0;
    for (size_t k = 0; k < es.size() && used < n - 1; ++k) {
        int a = find(es[k].u), b = find(es[k].v);
        if (a == b) continue;
        par[a] = b;
        W += es[k].w;
        ++used;
        tree[es[k].u].push_back(make_pair(es[k].v, es[k].w));
        tree[es[k].v].push_back(make_pair(es[k].u, es[k].w));
    }

    // 从每个点出发 DFS，求 MST 树上路径最大边；对每个点对更新答案。
    double ans = 0.0;
    vector<int> stNode(n), stParent(n);
    vector<double> stMax(n);
    for (int s = 0; s < n; ++s) {
        int top = 0;
        stNode[top] = s;
        stParent[top] = -1;
        stMax[top] = 0.0;
        ++top;
        while (top) {
            --top;
            int u = stNode[top], pu = stParent[top];
            double mx = stMax[top];
            if (u > s) {
                double B = W - mx;  // 除 (s,u) 外新图其余道路权值和的最小值
                if (B > 0.0) {      // B=0 仅当存在零权边且 N=2，题面排除；保守跳过
                    double r = (P[s] + P[u]) / B;
                    if (r > ans) ans = r;
                }
            }
            for (size_t t = 0; t < tree[u].size(); ++t) {
                int v = tree[u][t].first;
                if (v == pu) continue;
                stNode[top] = v;
                stParent[top] = u;
                stMax[top] = tree[u][t].second > mx ? tree[u][t].second : mx;
                ++top;
            }
        }
    }

    printf("%.2f\n", ans);
    return 0;
}
