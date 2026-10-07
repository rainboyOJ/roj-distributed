// 一本通 1725《账本核算》标程（C++17，stdin -> stdout）
//
// ======================= 参考来源（联网检索，任务书要求） =======================
// 检索路径：CSDN 站内搜索 API「一本通 1725 账本核算」/「账本核算」直接命中同题题解；
// 另以题面特征句「小D接到一个任务，为税务部门调查一位商人的账本」交叉确认同题。
//   [1] https://blog.csdn.net/hongkongreporter/article/details/102537786
//       《20191012 练习：差分约束系统》—— 其 T2 即「1725：账本核算」。给出建模：
//       记前缀和 s[i]=A1+...+Ai，则「x..y 的总收入 = w」即 s[y]-s[x-1]=w，
//       拆成两条三角不等式 s[y] <= s[x-1]+w 与 s[x-1] <= s[y]-w（有向边 x-1->y 权 w、
//       y->x-1 权 -w）；为保证连通性加虚点（该博客用 n+1）向所有点连 0 权边，
//       判负环：有负环 false，否则 true。样例 2 组输出 true/false。
//   [2] https://blog.csdn.net/ygmjsjdboy/article/details/102557101
//       《【差分约束】账本核算》—— 同题，同一建模（s_i - s_{j-1} = c 拆两条三角不等式），
//       用 dfs 版 SPFA 判负环。
//   [3] 官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1725（本轮实抓）
//       标题「1725：账本核算」，限制 1000 ms / 165888 KB，题面与本包 content.md 一致。
// 同型经典题（非本题来源，仅作建模佐证）：HNOI2005《狡猾的商人》(Luogu P2294)——
// 题意完全相同（给出若干区间和，判断是否存在合法序列），主流解法同为前缀和差分约束。
// ============================================================================
//
// 题面数据范围（content.md）：T < 100；n, m < 100；1 <= x <= y <= n；w 题面未给上界。
// 限制：1000 ms / 162 MB（config.json；官方页 165888 KB）。
// 因 w 无上界，本标程全程用 long long（前缀和可累积到 n*|w|，须防溢出）。
//
// 算法（与来源 [1][2] 同一图模型，但把随机化的 SPFA 换成确定性 Bellman-Ford）：
//   1) 结点 0..n 表示前缀和 s[0..n]，另设虚点 n+1 向每个结点连 0 权边（保证全图可达）；
//   2) 每条信息 x y w 建两条边：(x-1) -> y 权 w，(y) -> (x-1) 权 -w；
//   3) 全图以 0 为初值（等价于虚点 0 权边松弛一轮）跑 Bellman-Ford：
//      若第 (n+2) 轮仍能松弛 => 存在负环 => 不等式组无解 => 账本是假的，输出 false；
//      否则输出 true。
//   正确性：约束系统有解 <=> 差分约束图无负环（最短路的三角不等式可构造一组解）；
//   且 w 为整数时最短路距离为整数，故「实数可解」与「整数账本可解」等价。
//
// 规模：n+2 <= 101 个点，2m + (n+1) <= 300 条边，每组 O(V*E) < 3*10^4 次松弛，
// T <= 99 组总计 < 3*10^6，远低于 1000 ms；内存常数级（远低于 162 MB）。

#include <cstdio>
#include <vector>

using namespace std;

typedef long long ll;

struct Edge {
    int u, v;
    ll w;
};

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;

    while (T-- > 0) {
        int n, m;
        if (scanf("%d %d", &n, &m) != 2) return 0;

        const int S = n + 1;   // 虚点
        const int V = n + 2;   // 结点 0..n 前缀和 + 虚点

        vector<Edge> edges;
        edges.reserve(2 * m + n + 1);

        for (int i = 0; i < m; ++i) {
            int x, y;
            ll w = 0;
            if (scanf("%d %d %lld", &x, &y, &w) != 3) break; // 输入截断时不留未初始化值
            int a = x - 1, b = y;          // s[b] - s[a] = w
            edges.push_back(Edge{a, b, w});
            edges.push_back(Edge{b, a, -w});
        }
        for (int i = 0; i <= n; ++i) edges.push_back(Edge{S, i, 0});

        // 全 0 初值 == 虚点 0 权入边先松弛一轮；此后负环 <=> 每轮都还能松弛。
        vector<ll> dist(V, 0);
        bool negativeCycle = false;
        for (int it = 0; it < V; ++it) {
            bool changed = false;
            for (size_t k = 0; k < edges.size(); ++k) {
                const Edge &e = edges[k];
                if (dist[e.u] + e.w < dist[e.v]) {
                    dist[e.v] = dist[e.u] + e.w;
                    changed = true;
                }
            }
            if (!changed) break;                  // 收敛 => 无负环
            if (it == V - 1) negativeCycle = true; // 第 V 轮仍松弛 => 负环
        }

        puts(negativeCycle ? "false" : "true");
    }
    return 0;
}
