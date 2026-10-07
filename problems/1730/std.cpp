// 一本通 1730《二分图》标程（C++17）
// 自研（无公开题解检索需求，经典「边属于某最大匹配」判定）：
//   1) Hopcroft-Karp 求最大匹配；若 < n（无完美匹配）→ 全输出 1。
//   2) 固定最大匹配 M（|M|=n 饱和左部，右部可有自由点），建有向图 D：
//      匹配边 (u,v) → u→v，非匹配边 (u,v) → v→u。
//      非匹配边 (u,v) 属于某个完美匹配 ⟺
//        (a) u、v 在同一 SCC（该边在 M-交错环上），或
//        (b) v 可从某个 M 自由点到达（沿交错路径前缀翻转即可让该边入选）。
//      匹配边恒属于。若 |M|<n 则无完美匹配，全输出 1。
//   3) 输出取反：属于 → 0，否则（含非边）→ 1。
#include <cstdio>
#include <cstring>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

const int MAXN = 305, MAXM = 1505;
const int MAXV = MAXN + MAXM;

int n, m;
int matchL[MAXN], matchR[MAXM];
int lev[MAXN];
vector<int> g[MAXN];

bool bfs() {
    static queue<int> que;
    fill(lev, lev + n + 1, 0);
    for (int i = 1; i <= n; i++) {
        if (!matchL[i]) { lev[i] = 1; que.push(i); }
    }
    bool found = false;
    while (!que.empty()) {
        int u = que.front(); que.pop();
        for (int v : g[u]) {
            int w = matchR[v];
            if (w && !lev[w]) {
                lev[w] = lev[u] + 1;
                que.push(w);
            } else if (!w) {
                found = true;
            }
        }
    }
    return found;
}

bool dfs(int u) {
    for (int v : g[u]) {
        int w = matchR[v];
        if (!w || (lev[w] == lev[u] + 1 && dfs(w))) {
            matchL[u] = v;
            matchR[v] = u;
            return true;
        }
    }
    lev[u] = 0;
    return false;
}

int hopcroft() {
    int match = 0;
    while (bfs())
        for (int i = 1; i <= n; i++)
            if (!matchL[i] && dfs(i)) match++;
    return match;
}

// ---- Tarjan SCC on V = n + m vertices ----
int head[MAXV], size1;
struct Edge { int to, ne; } ed[500005];  // 上限 n*m=450000
void addE(int x, int y) { ed[++size1] = {y, head[x]}; head[x] = size1; }

int dfn[MAXV], low[MAXV], stk[MAXV], top, timer;
bool instk[MAXV];
int sccOf[MAXV], sccCnt;
bool reachable[MAXV];

void tarjan(int u) {
    dfn[u] = low[u] = ++timer;
    stk[++top] = u; instk[u] = true;
    for (int e = head[u]; e; e = ed[e].ne) {
        int v = ed[e].to;
        if (!dfn[v]) {
            tarjan(v);
            low[u] = min(low[u], low[v]);
        } else if (instk[v]) {
            low[u] = min(low[u], dfn[v]);
        }
    }
    if (low[u] == dfn[u]) {
        sccCnt++;
        int w;
        do {
            w = stk[top--];
            instk[w] = false;
            sccOf[w] = sccCnt;
        } while (w != u);
    }
}

char line[MAXM];
char ans[MAXN][MAXM];

int main() {
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= n; i++) {
        scanf("%s", line + 1);
        for (int j = 1; j <= m; j++)
            if (line[j] == '1') g[i].push_back(j);
    }
    int match = hopcroft();
    // 初始：全部输出 1
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) ans[i][j] = '1';
        ans[i][m + 1] = 0;
    }
    if (match < n) {
        for (int i = 1; i <= n; i++) puts(ans[i] + 1);
        return 0;
    }
    // 建有向图 D：左部 1..n，右部 n+1..n+m；匹配边 u→v，非匹配边 v→u
    for (int i = 1; i <= n; i++) {
        for (int j : g[i]) {
            if (matchL[i] == j) addE(i, n + j);       // 匹配边 u→v
            else addE(n + j, i);                       // 非匹配边 v→u
        }
    }
    for (int v = 1; v <= n + m; v++)
        if (!dfn[v]) tarjan(v);
    // (b) 从右部自由点出发可达的右部点
    static queue<int> que;
    for (int j = 1; j <= m; j++)
        if (!matchR[j]) { reachable[n + j] = true; que.push(n + j); }
    while (!que.empty()) {
        int u = que.front(); que.pop();
        for (int e = head[u]; e; e = ed[e].ne) {
            int v = ed[e].to;
            if (!reachable[v]) { reachable[v] = true; que.push(v); }
        }
    }
    for (int i = 1; i <= n; i++) {
        for (int j : g[i]) {
            if (matchL[i] == j) ans[i][j] = '0';
            else if (sccOf[i] == sccOf[n + j]) ans[i][j] = '0';          // (a) 交错环
            else if (reachable[n + j]) ans[i][j] = '0';  // (b) 右端点自由点可达
        }
    }
    for (int i = 1; i <= n; i++) puts(ans[i] + 1);
    return 0;
}
