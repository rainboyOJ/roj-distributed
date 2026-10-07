// 一本通 1419《SPFA(II)》标程
// 题意：给定有向连通图，求 1 到 n 的最短路。
// 数据范围：N≤20000, M≤40000, -1e9≤D≤1e9，保证无负环且 1 可达 n。
// 参考来源：https://blog.csdn.net/lybc2019/article/details/128441900
//
// 注意：答案可达 -2e13 量级（路径含约 20000 条 -1e9 的边），必须用 long long，
// 且 INF 需远大于该量级。样例含自环与负权边，SPFA 与 Bellman-Ford 均可。
// 这里采用 SPFA（队列优化 Bellman-Ford）。

#include <bits/stdc++.h>
using namespace std;

static const long long INF = 4e18;

int n, m;
vector<vector<pair<int, long long>>> g;  // g[u] = {(v, w)}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    g.assign(n + 1, {});
    for (int i = 0; i < m; i++) {
        int s, t;
        long long d;
        cin >> s >> t >> d;
        g[s].push_back({t, d});
    }

    vector<long long> dist(n + 1, INF);
    vector<bool> inq(n + 1, false);
    deque<int> q;

    dist[1] = 0;
    q.push_back(1);
    inq[1] = true;

    while (!q.empty()) {
        int u = q.front();
        q.pop_front();
        inq[u] = false;
        for (auto &e : g[u]) {
            int v = e.first;
            long long w = e.second;
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                if (!inq[v]) {
                    inq[v] = true;
                    q.push_back(v);
                }
            }
        }
    }

    cout << dist[n] << '\n';
    return 0;
}
