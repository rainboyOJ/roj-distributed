// 一本通 1420《Dijkastra(II)》标程
//
// 题意：无向连通图，n 点 m 边（N≤200000, M≤400000, 0≤D≤10^9），
//       求点 1 到点 n 的最短距离，输出一个整数。
//
// 参考来源（网络 C++ 题解，已联网核对、本机编译并经样例+对拍验证后改写）：
//   1. https://blog.csdn.net/qq_59414216/article/details/119861667
//      《1420：Dijkastra(II)》—— 堆优化 Dijkstra（priority_queue + pair，邻接表），
//      long long dis[200005]，重边取 min，自环跳过（样例含自环 2 2 0）。
//   2. https://blog.csdn.net/lybc2019/article/details/128441918
//      《1420：Dijkastra(II)》—— 结构体 node{num,dist} + priority_queue 小根堆，
//      同样为堆优化 Dijkstra，long long 距离。
//   3. https://www.jianshu.com/p/be597719474a（同 2 的思路，作者 Simon 李）
//
// 要点（与来源一致）：
//   * 边权 0≤D≤10^9，路径最长可达约 2*10^5 * 10^9 = 2*10^14 > INT_MAX，
//     距离必须用 long long（本组顶格数据实际把这一卡点做进去）。
//   * 无向边双向建边；重边自动被 Dijkstra 的取 min 语义处理；
//     自环对最短路无影响，可直接跳过（与来源 1 一致）。
//   * 堆优化 Dijkstra 复杂度 O((N+M) log N)，顶格 N=2e5, M=4e5 下 < 100 ms。
//
// 题面无负权（0≤D），Dijkstra 正确性成立；图保证连通，dis[n] 一定可达。

#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>

using namespace std;

const int MAXN = 200005;
const int MAXM = 400005;          // M ≤ 400000，无向边双向建边需 2*M
const long long INF = 0x3f3f3f3f3f3f3f3fLL;

int n, m, tot, head[MAXN], nxt[2 * MAXM], to[2 * MAXM];
int w[2 * MAXM];
long long dis[MAXN];
bool vis[MAXN];

inline void add(int s, int t, int d) {
    ++tot;
    to[tot] = t;
    w[tot] = d;
    nxt[tot] = head[s];
    head[s] = tot;
}

int main() {
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= m; ++i) {
        int s, t, d;
        scanf("%d%d%d", &s, &t, &d);
        if (s == t) continue; // 自环跳过（样例含 2 2 0）
        add(s, t, d);         // 无向边：双向建边
        add(t, s, d);
    }
    memset(dis, 0x3f, sizeof(dis));
    dis[1] = 0;
    // 小根堆：pair<距离, 点号>
    priority_queue< pair<long long, int>, vector< pair<long long, int> >,
                    greater< pair<long long, int> > > q;
    q.push(make_pair(0LL, 1));
    while (!q.empty()) {
        pair<long long, int> top = q.top();
        q.pop();
        int x = top.second;
        if (vis[x]) continue; // 堆优化 Dijkstra：出堆时定稿
        vis[x] = true;
        for (int i = head[x]; i; i = nxt[i]) {
            int y = to[i];
            if (!vis[y] && dis[x] + w[i] < dis[y]) {
                dis[y] = dis[x] + w[i];
                q.push(make_pair(dis[y], y));
            }
        }
    }
    printf("%lld\n", dis[n]); // 图保证连通，dis[n] 必可达
    return 0;
}
