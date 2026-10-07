// 最小花费 —— 最小生成树（Prim，O(n^2)）
//
// 建模：设前缀和 S_0=0, S_k = x_1 xor x_2 xor ... xor x_k。
// 询问区间 [i,j] 的奇偶性 = S_{i-1} xor S_j，相当于在图上的节点 (i-1) 与 j
// 之间连一条代价 c[i,j] 的边。要确定所有 x_i（等价于确定所有 S_i），
// 必须让节点 0..n 全部与 0 连通，最小代价即为该 n+1 个点的最小生成树。
//
// 于是问题化为：完全图 K_{n+1}，节点 a<b 之间的边权为 c[a+1][b]。
// 采用朴素 Prim（稠密图 O(n^2)）。
#include <cstdio>
#include <vector>
#include <cstring>
using namespace std;

typedef long long ll;

static const ll INF = (ll)4e18;

// 快速读入
static char buf[1 << 25];
static size_t bufLen = 0, bufPos = 0;

static inline int readChar() {
    if (bufPos == bufLen) {
        bufLen = fread(buf, 1, sizeof(buf), stdin);
        bufPos = 0;
        if (bufLen == 0) return -1;
    }
    return buf[bufPos++];
}

static inline ll readLL() {
    int c = readChar();
    while (c != -1 && (c < '0' || c > '9')) c = readChar();
    ll x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = readChar();
    }
    return x;
}

int main() {
    int n = (int)readLL();

    // 邻接矩阵（下三角与对角线不用），w[a*(n+1)+b] (a<b)
    int V = n + 1;
    vector<int> w((size_t)V * V, 0);
    for (int i = 1; i <= n; ++i) {
        int a = i - 1;
        for (int j = i; j <= n; ++j) {
            w[(size_t)a * V + j] = (int)readLL();
        }
    }

    vector<ll> dist(V, INF);
    vector<char> used(V, 0);
    dist[0] = 0;
    ll ans = 0;
    for (int it = 0; it < V; ++it) {
        int v = -1;
        for (int u = 0; u < V; ++u)
            if (!used[u] && (v == -1 || dist[u] < dist[v])) v = u;
        used[v] = 1;
        ans += dist[v];
        // 更新：节点 v 与其他未使用点 u 的边权（注意无向边权对称取值）
        for (int u = 0; u < V; ++u) {
            if (used[u] || u == v) continue;
            int weight = (u < v) ? w[(size_t)u * V + v] : w[(size_t)v * V + u];
            if ((ll)weight < dist[u]) dist[u] = weight;
        }
    }

    printf("%lld\n", ans);
    return 0;
}
