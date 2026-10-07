// 一本通 1718《益智游戏》（高手训练篇·三、图论）
//
// 题意 / 模型
// -----------
// 正权有向图。小P 必须沿最短路 A→B 走，小R 必须沿最短路 C→D 走；
// 每回合可移动一条边或原地休息一回合，因此两人的到站时刻可以任意延后。
// 两人在某时刻同处一节点即得一次奖励，每节点最多一次。求最大奖励数；
// 若 A 到不了 B 或 C 到不了 D 输出 -1。
//
// 关键结论
// --------
// 令 4 组距离（long long）：
//   dA[v] = dist(A,v)（原图）、dB[v] = dist(v,B)（反图从 B 跑）、
//   dC[v] = dist(C,v)、dD[v] = dist(v,D)（反图从 D 跑），D_AB=dA[B]，D_CD=dC[D]。
// 1) 一个节点能被两人先后共同访问 <=> v 同时在两条最短路集合里：
//      dA[v] + dB[v] == D_AB 且 dC[v] + dD[v] == D_CD   （记此点集为 U）
// 2) 两点 u,v 能被两人按同一先后顺序先后共同访问 <=> 存在一条由「公共最短路边」
//    组成的 u→v 路径。边 (u,v,w) 是公共最短路边当且仅当
//      dA[u] + w + dB[v] == D_AB 且 dC[u] + w + dD[v] == D_CD。
//    （必要性：最短路上的每段都必须是最短路，故两段长度都恰为 d(u,v)；
//      充分性：把公共边路径拼接起来仍是各自的最短路，中间空隙靠「休息」对齐即可。）
// 3) 因此答案为「公共最短路边」这张 DAG 上的最长节点链（正权 ⇒ 沿 dA 严格递增 ⇒
//    按 dA 排序后线性 DP），U = ∅ 时答案为 0；不可达时 -1。
//
// 复杂度 O((n + m) log n + m)，n ≤ 5e4、m ≤ 2e5 足够。
//
// 来源说明
// --------
// 网络检索到本题公开题解（同一模型、拓扑最长链）：
//   https://blog.csdn.net/qq_37494296/article/details/77509625
//   （《拓扑，DP noip 模拟赛 [益智游戏] 题解》，4 次 Dijkstra + 公共最短路边建新图 + 拓扑 DP）
//   https://blog.csdn.net/lq1990717/article/details/112505212 一份通题解目录（检索兜底）
// 其余要点：本题数据权值可达 5e8、路径长度和可达 1e14，故所有距离/判定必须 64 位，
// 且对「U 为空」「无公共边但存在公共点」的边界单独处理（题解代码用全局 dp 初值 1 会误报，
// 这里改为只对 U 中节点取初值 1，未出现公共点时答案自然为 0）。
// 题面来源：http://ybt.ssoier.cn:8088/problem_show.php?pid=1718
#include <cstdio>
#include <cstring>
#include <queue>
#include <vector>
#include <algorithm>
using namespace std;

typedef long long ll;
static const ll INF = (ll)4e18;

static const int MAXN = 50005;
static const int MAXM = 200005;

static int n, m;
static int head[2][MAXN], nxt[2][2 * MAXM], too[2][2 * MAXM], wei[2][2 * MAXM];
static int ec = 0;

static inline void addEdge(int u, int v, int w) {
    ++ec;
    too[0][ec] = v; wei[0][ec] = w; nxt[0][ec] = head[0][u]; head[0][u] = ec;
    too[1][ec] = u; wei[1][ec] = w; nxt[1][ec] = head[1][v]; head[1][v] = ec;
}

// 快速读入
static char buf[1 << 22];
static size_t blen = 0, bpos = 0;
static inline int readChar() {
    if (bpos == blen) { blen = fread(buf, 1, sizeof(buf), stdin); bpos = 0; if (blen == 0) return -1; }
    return buf[bpos++];
}
static inline ll readLL() {
    int c = readChar();
    while (c != -1 && (c < '0' || c > '9')) c = readChar();
    ll x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = readChar(); }
    return x;
}

typedef pair<ll, int> pli;

static void dijkstra(int src, int dir, ll *dist) {
    for (int i = 1; i <= n; ++i) dist[i] = INF;
    priority_queue<pli, vector<pli>, greater<pli> > pq;
    dist[src] = 0;
    pq.push(pli(0, src));
    while (!pq.empty()) {
        pli cur = pq.top(); pq.pop();
        ll du = cur.first; int u = cur.second;
        if (du > dist[u]) continue;
        for (int e = head[dir][u]; e; e = nxt[dir][e]) {
            int v = too[dir][e];
            ll nd = du + wei[dir][e];
            if (nd < dist[v]) { dist[v] = nd; pq.push(pli(nd, v)); }
        }
    }
}

static ll dA[MAXN], dB[MAXN], dC[MAXN], dD[MAXN];
static int dp[MAXN];

int main() {
    n = (int)readLL();
    m = (int)readLL();
    for (int i = 0; i < m; ++i) {
        int x = (int)readLL(), y = (int)readLL(), l = (int)readLL();
        addEdge(x, y, l);
    }
    int A = (int)readLL(), B = (int)readLL(), C = (int)readLL(), D = (int)readLL();

    dijkstra(A, 0, dA);   // A 正向
    dijkstra(B, 1, dB);   // 反图从 B => dist(v,B)
    dijkstra(C, 0, dC);   // C 正向
    dijkstra(D, 1, dD);   // 反图从 D => dist(v,D)

    if (dA[B] >= INF / 2 || dC[D] >= INF / 2) { printf("-1\n"); return 0; }
    const ll DAB = dA[B], DCD = dC[D];

    // U：同时在两条最短路上的节点；dp 初值 1
    vector<int> order;
    for (int v = 1; v <= n; ++v) {
        if (dA[v] < INF / 2 && dB[v] < INF / 2 && dC[v] < INF / 2 && dD[v] < INF / 2 &&
            dA[v] + dB[v] == DAB && dC[v] + dD[v] == DCD) {
            dp[v] = 1;
            order.push_back(v);
        } else {
            dp[v] = 0;
        }
    }
    // 公共最短路边沿 dA 严格递增 => 按 dA 排序即拓扑序
    sort(order.begin(), order.end(), [](int x, int y) { return dA[x] < dA[y]; });

    for (size_t i = 0; i < order.size(); ++i) {
        int u = order[i];
        if (dp[u] == 0) continue;
        for (int e = head[0][u]; e; e = nxt[0][e]) {
            int v = too[0][e], w = wei[0][e];
            if (dA[u] + (ll)w + dB[v] == DAB && dC[u] + (ll)w + dD[v] == DCD) {
                if (dp[u] + 1 > dp[v]) dp[v] = dp[u] + 1;
            }
        }
    }

    int ans = 0;
    for (int v = 1; v <= n; ++v) if (dp[v] > ans) ans = dp[v];
    printf("%d\n", ans);
    return 0;
}
