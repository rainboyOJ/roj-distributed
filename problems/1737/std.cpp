// 一本通 1737《邮递员》标程（C++17）
// 自研（POI/BZOJ1515 同源模型）：
//   片段 v1..vk 强制弧 (v1,v2),...,(v_{k-1},v_k) 在欧拉回路中连续出现。
//   把被片段粘合的弧链收缩为「超弧」，问题变为收缩多重图上是否存在欧拉回路
//   （回路从 1 出发回到 1；收缩模型等价于允许片段跨越首尾的环状语义）。
//   判定：① 片段弧须存在且片段内不重复用弧；② 后继/前驱粘合约束无冲突；
//   ③ 收缩图每点入度=出度；④ 非零度点弱连通。全满足输出 TAK，否则 NIE。
#include <cstdio>
#include <vector>
#include <unordered_map>
#include <queue>
using namespace std;

typedef long long ll;

struct Edge { int u, v; };

int main() {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    vector<Edge> edges(m);
    unordered_map<ll, int> idOf;   // (u,v) -> edge id
    idOf.reserve((size_t)m * 2 + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        scanf("%d %d", &a, &b);
        edges[i] = {a, b};
        idOf[((ll)a << 20) | (ll)b] = i;    // n ≤ 50000 < 2^20
    }
    vector<int> nxtE(m, -1), prvE(m, -1);
    vector<char> inFrag(m, 0);
    bool bad = false;

    int t;
    scanf("%d", &t);
    for (int f = 0; f < t && !bad; f++) {
        int k;
        scanf("%d", &k);
        vector<int> vs(k);
        for (int i = 0; i < k; i++) scanf("%d", &vs[i]);
        if (k < 2) continue;
        vector<int> es(k - 1, -1);
        for (int i = 0; i + 1 < k; i++) {
            ll key = ((ll)vs[i] << 20) | (ll)vs[i + 1];
            auto it = idOf.find(key);
            if (it == idOf.end()) { bad = true; break; }   // 片段弧不存在
            int e = it->second;
            for (int j = 0; j < i; j++) if (es[j] == e) { bad = true; break; } // 片段内重复弧
            if (bad) break;
            es[i] = e;
        }
        if (bad) break;
        for (int i = 0; i + 2 < k; i++) {
            int e1 = es[i], e2 = es[i + 1];
            if ((nxtE[e1] != -1 && nxtE[e1] != e2) || (prvE[e2] != -1 && prvE[e2] != e1)) {
                bad = true; break;      // 粘合冲突
            }
            nxtE[e1] = e2; prvE[e2] = e1;
        }
    }
    if (bad) { printf("NIE\n"); return 0; }

    // 收缩：链的起始弧 = prvE == -1 的弧；全环粘合块任取代表
    vector<int> unitOf(m, -1);
    int unitCnt = 0;
    vector<int> unitTail, unitHead;
    vector<char> used(m, 0);
    for (int i = 0; i < m; i++) {
        if (prvE[i] != -1 || used[i]) continue;
        // 从 i 沿 nxt 走完链
        int head = i;
        while (nxtE[head] != -1 && nxtE[head] != i) head = nxtE[head];
        int e = i;
        while (true) {
            used[e] = 1; unitOf[e] = unitCnt;
            if (nxtE[e] == -1 || nxtE[e] == i) break;
            e = nxtE[e];
        }
        unitTail.push_back(edges[i].u);
        unitHead.push_back(edges[e].v);
        unitCnt++;
    }
    for (int i = 0; i < m; i++) if (!used[i]) {  // 剩下的全环块
        int e = i;
        unitTail.push_back(edges[i].u);
        int last = i;
        while (true) {
            used[e] = 1; unitOf[e] = unitCnt;
            last = e;
            if (nxtE[e] == -1) break;
            e = nxtE[e];
            if (e == i) break;
        }
        unitHead.push_back(edges[last].v);
        unitCnt++;
    }

    // 收缩图度数 + 弱连通
    vector<int> din(n + 1, 0), dout(n + 1, 0);
    vector<vector<int>> adj(n + 1);
    for (int u = 0; u < unitCnt; u++) {
        int a = unitTail[u], b = unitHead[u];
        dout[a]++; din[b]++;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    for (int v = 1; v <= n; v++) if (din[v] != dout[v]) { bad = true; break; }
    if (bad) { printf("NIE\n"); return 0; }

    // 弱连通（非零度点）
    vector<char> vis(n + 1, 0);
    int start = -1;
    for (int v = 1; v <= n; v++) if (din[v] > 0 || dout[v] > 0) { start = v; break; }
    if (start != -1) {
        static queue<int> q;
        q.push(start); vis[start] = 1;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int w : adj[u]) if (!vis[w]) { vis[w] = 1; q.push(w); }
        }
        for (int v = 1; v <= n; v++)
            if ((din[v] > 0 || dout[v] > 0) && !vis[v]) { bad = true; break; }
    }
    printf(bad ? "NIE\n" : "TAK\n");
    return 0;
}
