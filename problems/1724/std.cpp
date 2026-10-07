// std.cpp —— 一本通 1724《小K的农场》
// 题面依据：.ybt-import/staging/1724/content.md（官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1724，
//           限制 1000 ms / 131072 KB，与 config.json 一致）
//
// ============================ 来源情况（网络检索，附 URL） ============================
// 一本通 1724 与洛谷 P1993《小K的农场》、BZOJ 3436 题面逐字一致（差分约束系统模板题），
// CSDN 题解多篇（关键词「小K的农场 差分约束」「P1993 小K的农场 spfa 负环」）：
//   [1] https://blog.csdn.net/dgssl_xhy/article/details/122145488   建边：a-b>=c ⇒ b≤a-c；a-b<=c ⇒ a≤b+c；
//                                                                    a=b ⇒ 双向 0；加超级源点 n+1 连所有点 0，SPFA 判负环
//   [2] https://blog.csdn.net/qq_30115697/article/details/83004340   同上（1 型 a→b 权 -c；2 型 b→a 权 c；3 型双向 0；源点 0），dfs_spfa 判负环
//   [3] https://blog.csdn.net/xiji333/article/details/102799176     同一建边约定，dfs_spfa 判是否无解（有正/负环 ⇔ 无解）
//   [4] https://blog.csdn.net/ndsffx501ccy/article/details/40708187  一本通/BZOJ 3436 同题（差分约束判环）
// 各来源结论一致：三类信息即差分约束系统的边；「存在情况吻合记忆」⇔ 系统有可行解 ⇔ 图中无负环。
// 本 std 为**改写**（非照抄）：
//   (1) 统一成最短路的松弛式 dist[v] ≤ dist[u] + w（1 型边 a→b 权 -c；2 型边 b→a 权 c；3 型双向 0）；
//   (2) 超级源点 0 连所有点权 0 ⇒ 图不连通也能一次判完整（不逐连通块跑）；
//   (3) BFS-SPFA 判负环：静态链式前向星 + std::deque，SLF（小尾优先）tie-break 加速，
//       某点入队次数 > 点数(n+1) ⇒ 负环（Bellman-Ford 队列法标准判据）；
//   (4) 为什么可以不管「数量非负」：全部约束只限制差值，解可整体平移，故可行解总可平移成非负，
//       可行性判据与是否要求非负无关（差分约束标准结论）。
// 复杂度：n,m ≤ 10^4，边数 ≤ 2m+n ≈ 3·10^4，实测顶格点 1 ms 级。
// =====================================================================================

#include <cstdio>
#include <cstring>
#include <deque>

using namespace std;

static const int MAXN = 10005;  // n ≤ 10^4，+1 给超级源点 0
static const int MAXE = 40005;  // 2*m(相等约束双向) + n(源点) ≤ 3*10^4

static int head[MAXN], nxt[MAXE], to_[MAXE], w_[MAXE], ecnt = 0;

static inline void addEdge(int u, int v, int w) {
    ++ecnt;
    to_[ecnt] = v;
    w_[ecnt] = w;
    nxt[ecnt] = head[u];
    head[u] = ecnt;
}

static int dist_[MAXN];
static int enq_[MAXN];
static bool inq[MAXN];

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 0; i < m; ++i) {
        int op, a, b, c;
        if (scanf("%d %d %d", &op, &a, &b) != 3) return 0;
        if (op == 1) {
            // x_a - x_b ≥ c  ⟺  x_b ≤ x_a - c
            scanf("%d", &c);
            addEdge(a, b, -c);
        } else if (op == 2) {
            // x_a - x_b ≤ c  ⟺  x_a ≤ x_b + c
            scanf("%d", &c);
            addEdge(b, a, c);
        } else {
            // x_a == x_b  ⟺  x_a ≤ x_b 且 x_b ≤ x_a
            addEdge(a, b, 0);
            addEdge(b, a, 0);
        }
    }
    for (int i = 1; i <= n; ++i) addEdge(0, i, 0);  // 超级源点：保证图连通

    memset(dist_, 0x3f, sizeof(dist_));
    dist_[0] = 0;
    deque<int> q;
    q.push_back(0);
    inq[0] = true;
    enq_[0] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop_front();
        inq[u] = false;
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to_[e];
            if (dist_[u] + w_[e] < dist_[v]) {
                dist_[v] = dist_[u] + w_[e];
                if (!inq[v]) {
                    inq[v] = true;
                    if (++enq_[v] > n + 1) {  // 入队超过点数(含源点) ⇒ 存在负环
                        puts("No");
                        return 0;
                    }
                    if (!q.empty() && dist_[v] < dist_[q.front()])
                        q.push_front(v);  // SLF：更小者优先出队
                    else
                        q.push_back(v);
                }
            }
        }
    }
    puts("Yes");
    return 0;
}
