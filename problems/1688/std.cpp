// 一本通 1688《最优路径》标程
// 题意：n 点 m 边无向图（边长均为 1，边带颜色 c），求 1->n 路径，
//       在边数最少的前提下颜色序列字典序最小。
// 思路（两次 BFS，经典 UVa 1599 "Ideal Path" 同题型）：
//   1) 从 n 反向 BFS 求 dist[v] = v 到 n 的最短边数；
//   2) 从 1 正向分层走：第 k 层候选点集合 = { v : dist[v] = dist[1]-k }，
//      每层在候选出边中取最小颜色 cmin，第 k 个输出 = min cmin，
//      下一层候选 = 颜色为 cmin 的出边所到的、尚未入层的点。
//   每个点最多入层一次，总复杂度 O(n + m)。
// 参考来源（思路改写，非逐行照抄）：
//   https://blog.csdn.net/weixin_33769207/article/details/93938063 （例题6-20 UVa1599 Ideal Path 两次BFS）
//   https://blog.csdn.net/shiki_05/article/details/49623617 （理想路径 Ideal Path UVa1599）
// 本题与 UVa 1599 差异：多组数据；题目未保证图连通/1 可达 n（不可达时无解，
//   本标程约定输出 "0" 与空行，见 gen-report.md 风险点）。

#include <cstdio>
#include <vector>
#include <queue>
#include <climits>

using namespace std;

const int MAXN = 100005;

int n, m;
vector<int> g[MAXN];   // 邻接点
vector<int> col[MAXN]; // 对应边颜色
int dist_[MAXN];      // 到 n 的最短边数
int inLayer[MAXN];    // 是否已加入某层（每点仅入层一次）
int outSeq[200005];

int main() {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        scanf("%d %d", &n, &m);
        for (int i = 1; i <= n; ++i) { g[i].clear(); col[i].clear(); }
        for (int i = 0; i < m; ++i) {
            int a, b, c;
            scanf("%d %d %d", &a, &b, &c);
            if (a == b) continue; // 自环对最短路无用
            g[a].push_back(b); col[a].push_back(c);
            g[b].push_back(a); col[b].push_back(c);
        }
        // ---- BFS 1: 从 n 出发求各点到 n 的最短边数 ----
        for (int i = 1; i <= n; ++i) { dist_[i] = -1; inLayer[i] = 0; }
        queue<int> q;
        dist_[n] = 0; q.push(n);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (size_t i = 0; i < g[u].size(); ++i) {
                int v = g[u][i];
                if (dist_[v] == -1) { dist_[v] = dist_[u] + 1; q.push(v); }
            }
        }
        if (dist_[1] == -1) { // 1 与 n 不连通：题面未定义，输出 0 与空行
            printf("0\n\n");
            for (int i = 1; i <= n; ++i) { vector<int>().swap(g[i]); vector<int>().swap(col[i]); }
            continue;
        }
        // ---- BFS 2: 逐层取最小颜色 ----
        // 可行层集合可能包含 dist 相同但不在任一 "最优前缀路径" 上的点：
        // 任何满足 dist[v]=D-k 的点，从 1 出发经 k 条最优边（每步沿 dist 递减的可行边）
        // 都能继续沿 dist 递减走完剩余 D-k 步到 n，因此不会把死点带入后续层。
        int D = dist_[1];
        vector<int> cur;      // 当前层节点
        cur.push_back(1);
        inLayer[1] = 1;
        int outLen = 0;
        while (outLen < D) {
            int targetDist = D - outLen - 1; // 下一层应满足的 dist 值
            int cmin = INT_MAX;
            for (size_t i = 0; i < cur.size(); ++i) {
                int u = cur[i];
                for (size_t j = 0; j < g[u].size(); ++j)
                    if (dist_[g[u][j]] == targetDist && col[u][j] < cmin)
                        cmin = col[u][j];
            }
            outSeq[outLen++] = cmin;
            vector<int> nxt;
            for (size_t i = 0; i < cur.size(); ++i) {
                int u = cur[i];
                for (size_t j = 0; j < g[u].size(); ++j) {
                    int v = g[u][j];
                    if (dist_[v] == targetDist && col[u][j] == cmin && !inLayer[v]) {
                        inLayer[v] = 1;
                        nxt.push_back(v);
                    }
                }
            }
            cur.swap(nxt);
        }
        printf("%d\n", D);
        for (int i = 0; i < D; ++i) printf("%d%c", outSeq[i], i + 1 == D ? '\n' : ' ');
        if (D == 0) printf("\n");
        // 多组数据下释放邻接表容量，避免跨组内存累积
        for (int i = 1; i <= n; ++i) { vector<int>().swap(g[i]); vector<int>().swap(col[i]); }
    }
    return 0;
}
