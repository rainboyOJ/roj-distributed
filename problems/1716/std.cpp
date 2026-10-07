// 一本通 1716《次短路计数》  std.cpp
// ---------------------------------------------------------------------------
// 来源说明：
//   本题题面与 POJ 3463 "Sightseeing" 完全一致（输入样例/输出样例逐字相同），
//   怀疑 ybt 1716 即 POJ 3463 的改编收录。通过网络检索到多篇公开题解，
//   按其算法思路自行重写为 C++17 标程（未逐行复制）：
//     [1] https://blog.csdn.net/qq_41157137/article/details/88943544
//         POJ-3463：Sightseeing【次短路的数量】
//     [2] https://blog.csdn.net/icefox_zhx/article/details/78529456
//         poj3463（最短路计数+次短路计数）
//     [3] https://blog.csdn.net/gyh0730/article/details/82918773
//         POJ-3463 Sightseeing（最短路和次短路计数）
//     [4] https://vjudge.net/problem/POJ-3463
//   参考题解一致结论：求出 dist[t][0] / cnt[t][0]（最短路距离/条数）与
//   dist[t][1] / cnt[t][1]（次短路距离/条数），
//   答案 = cnt[t][0] + ( dist[t][1] == dist[t][0] + 1 ? cnt[t][1] : 0 )。
//   注意：题面【输出】要求“每组数据输出一个整数”，故只输出这一个和；
//   与 POJ 3463 输出格式一致，样例 3/2 已核对（详见 gen-report.md）。
//   “路线不同”按题面定义为“边集不同”，故平行边（x,y,w 相同但为两条边）
//   视为不同的边、产生不同的路线（题面样例2 答案=2 即由平行边 5->2 7 产生）。
// ---------------------------------------------------------------------------
// 算法：Dijkstra 扩展为「每个点两个状态：最短路状态 k=0 / 严格次短路状态 k=1」，
//   松弛时按 nd < dist0 / == dist0 / < dist1 / == dist1 四类分别更新距离与计数，
//   每个状态出堆一次（按距离升序保证最终值确定，平行边各自计数）。
//   复杂度 O((m log m) * T)，n<=1000, m<=10000。
// 输入：多组数据，第一行 T；每组 n m，随后 m 行 x y w（有向边 x->y 权 w），
//       最后一行 s t。
// 输出：每组一个整数 = 最短路方案数 +（次短路恰好多 1 单位时才加其次短路方案数），
//       保证所有数据答案 <= 1e9。
// 说明：dist[t][1] 表示“严格次短路”距离；当 dist[t][1] < dist[t][0] + 1 时，
//   “恰好多一个单位距离”的路线不存在，只计最短路部分。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>

using namespace std;

static const int INF = 0x3f3f3f3f;
static const int MAXN = 1005;

struct Edge {
    int to, w;
};

struct Node {
    int u, d, k;  // k = 0 最短路状态, k = 1 次短路状态
    bool operator<(const Node &o) const { return d > o.d; }  // 小根堆
};

int n, m, s, t;
vector<Edge> g[MAXN];
int dist[MAXN][2];
long long cnt[MAXN][2];
bool done[MAXN][2];

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        scanf("%d %d", &n, &m);
        for (int i = 1; i <= n; ++i) g[i].clear();
        for (int i = 0; i < m; ++i) {
            int x, y, w;
            scanf("%d %d %d", &x, &y, &w);
            g[x].push_back(Edge{y, w});
        }
        scanf("%d %d", &s, &t);
        for (int i = 1; i <= n; ++i) {
            dist[i][0] = dist[i][1] = INF;
            cnt[i][0] = cnt[i][1] = 0;
            done[i][0] = done[i][1] = false;
        }
        priority_queue<Node> pq;
        dist[s][0] = 0;
        cnt[s][0] = 1;
        pq.push(Node{s, 0, 0});
        while (!pq.empty()) {
            Node cur = pq.top();
            pq.pop();
            int u = cur.u, d = cur.d, k = cur.k;
            if (done[u][k] || d != dist[u][k]) continue;  // 跳过陈旧状态
            done[u][k] = true;
            for (size_t i = 0; i < g[u].size(); ++i) {
                int v = g[u][i].to, nd = d + g[u][i].w;
                if (nd < dist[v][0]) {
                    // 原最短路被顶成次短路
                    if (dist[v][0] < dist[v][1]) {
                        dist[v][1] = dist[v][0];
                        cnt[v][1] = cnt[v][0];
                        pq.push(Node{v, dist[v][1], 1});
                    }
                    dist[v][0] = nd;
                    cnt[v][0] = cnt[u][k];
                    pq.push(Node{v, nd, 0});
                } else if (nd == dist[v][0]) {
                    cnt[v][0] += cnt[u][k];
                } else if (nd < dist[v][1]) {
                    dist[v][1] = nd;
                    cnt[v][1] = cnt[u][k];
                    pq.push(Node{v, nd, 1});
                } else if (nd == dist[v][1]) {
                    cnt[v][1] += cnt[u][k];
                }
            }
        }
        long long ans = cnt[t][0];
        if (dist[t][1] == dist[t][0] + 1) ans += cnt[t][1];
        printf("%lld\n", ans);
    }
    return 0;
}
