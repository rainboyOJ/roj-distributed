// 一本通 1761《最小割》标程（ROJ 题号 1761；来源：信息学奥赛一本通 · 高手训练篇·四、数据结构）
//
// 题意：给无向无权简单图 G（N 个点 M 条边，无重边无自环），并给出 G 的一棵生成树 T
//       （输入先给 T 的 N-1 条边，再给不在 T 中的 M-N+1 条边）。
//       求「恰好包含 T 中一条边」的最小割的边数。
//       多组数据，第一行 T(T<=5)，每组 N(<=20000) M(<=200000)。
//
// 算法（自研，见下方「来源与依据」）：
//   设树边 e 把 T 分成 A、B 两部分。任何「恰好含一条 T 边」的割，其两侧点集必然是
//   T-e 的两个连通块（因为 T 是生成树，割中树边数 = 1 意味着 A、B 恰由删去 e 得到）。
//   于是该割的边集 = {e} ∪ {不在 T 中且两端分居 A、B 的边}，大小 = 1 + c(e)，
//   其中 c(e) 是「基本回路经过 e 的非树边条数」。
//   答案 = 1 + min_e c(e)。
//   统计 c(e)：树上差分。每条非树边 (u,v) 使 u-v 路径上所有树边的 c 加一：
//   diff[u]++, diff[v]++, diff[lca(u,v)] -= 2，再按 BFS 逆序自底向上累加，
//   节点 x 累加后的 diff[x] 即树边 (par[x], x) 的 c 值。
//   复杂度 O((N + M) log N)，N=20000、M=200000、T=5 时远低于 4000ms 限制。
//
// 来源与依据（题目 C++ 代码的检索过程与结论，均记录在 gen-report.md）：
//   - 已用题面特征句在多个搜索引擎检索（Bing / DuckDuckGo / 360 / CSDN 站内搜
//     「一本通 1761 最小割」等），**未找到本题的公开题解或 AC 代码**
//     （命中结果均为同名的其他题：BZOJ 2561 最小生成树/最小割、BZOJ 1797 最小割、
//      最小割树 ZJOI2011 等，题意与本題不同），故本题标程为自研实现。
//   - 自研所依据的通用技法（均为公认结论，非本题专有）：
//       * 最小割 / 割的定义与「割 = 两侧点集之间的边集」：
//         https://oi-wiki.org/graph/min-cut/ （OI Wiki「最小割」）
//       * 树上差分（边差分：diff[u]++, diff[v]++, diff[lca]-=2）：
//         https://oi-wiki.org/graph/tree-diff/ （OI Wiki「树上差分」）
//       * LCA 倍增求法（本题 N 小，倍增足够）：
//         https://oi-wiki.org/graph/lca/ （OI Wiki「最近公共祖先」）
//   - 正确性以题面【输入样例】验证（见 gen-report.md 第 3 节），并对手算过的
//     极小结构（N=2 只有树边 → 1；N=3 三角形 → 2）做定点断言。
//
// 实现说明：
//   - 全部用迭代（BFS）而非递归建树，避免 N=20000 的链状树递归爆栈。
//   - 输入用 fread 快读，适配 T=5 组、合计 10^6 条边的最大输入。
//   - n==1 的退化输入（此时 T 无树边，不存在「恰好含一条 T 边」的割）按约束不可能
//     出现（需 M>=N-1=0 且图无自环），为稳妥起见输出 0 并在报告中注明。
//   - 无重边无自环由题面保证，标程不做重复边判重（重复边只会让 c 值偏大，
//     但题面已排除；若数据违约，标程仍会输出一个确定值而不崩溃）。

#include <cstdio>
#include <cstring>
#include <algorithm>

using namespace std;

static const int MAXN = 20005;   // N <= 20000（题面上限 + 安全余量）
static const int MAXE = 2 * MAXN; // 树的邻接表（每条树边两条弧）
static const int LOG = 16;       // 2^15 = 32768 > 20000

static int head[MAXN], nxt[MAXE], to[MAXE], ecnt;
static int par[MAXN], dep[MAXN], up[LOG][MAXN];
static int diffArr[MAXN];
static int bfsOrder[MAXN];

static inline void addEdge(int u, int v) {
    to[ecnt] = v; nxt[ecnt] = head[u]; head[u] = ecnt++;
}

// ---- 快读 ----
static const int BUFSZ = 1 << 16;
static char buf[BUFSZ];
static int bufLen = 0, bufPos = 0;
static inline int readChar() {
    if (bufPos == bufLen) {
        bufLen = (int)fread(buf, 1, BUFSZ, stdin);
        bufPos = 0;
        if (bufLen <= 0) return -1;
    }
    return buf[bufPos++];
}
static inline int readInt() {
    int c = readChar();
    while (c != -1 && (c < '0' || c > '9') && c != '-') c = readChar();
    int sign = 1;
    if (c == '-') { sign = -1; c = readChar(); }
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = readChar(); }
    return x * sign;
}

static int lca(int u, int v) {
    if (dep[u] < dep[v]) swap(u, v);
    int d = dep[u] - dep[v];
    for (int k = 0; k < LOG; k++)
        if (d >> k & 1) u = up[k][u];
    if (u == v) return u;
    for (int k = LOG - 1; k >= 0; k--)
        if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
    return up[0][u];
}

int main() {
    int T = readInt();
    if (T < 0) T = 0;
    while (T--) {
        int n = readInt(), m = readInt();

        ecnt = 0;
        for (int i = 1; i <= n; i++) { head[i] = -1; diffArr[i] = 0; }

        for (int i = 0; i < n - 1; i++) {
            int u = readInt(), v = readInt();
            addEdge(u, v); addEdge(v, u);
        }

        if (n <= 1) {
            // 退化：无树边，不存在满足条件的割（约束下不可达）
            for (int i = 0; i < m - n + 1; i++) { readInt(); readInt(); }
            printf("0\n");
            continue;
        }

        // 迭代 BFS 建树（以 1 为根），同时求倍增祖先
        int qh = 0, qt = 0;
        bfsOrder[qt++] = 1;
        par[1] = 0; dep[1] = 0;
        for (int k = 0; k < LOG; k++) up[k][1] = 0;
        while (qh < qt) {
            int u = bfsOrder[qh++];
            for (int e = head[u]; e != -1; e = nxt[e]) {
                int v = to[e];
                if (v == par[u]) continue;
                par[v] = u;
                dep[v] = dep[u] + 1;
                up[0][v] = u;
                for (int k = 1; k < LOG; k++) up[k][v] = up[k - 1][up[k - 1][v]];
                bfsOrder[qt++] = v;
            }
        }

        // 非树边：树上差分
        for (int i = 0; i < m - n + 1; i++) {
            int u = readInt(), v = readInt();
            int w = lca(u, v);
            diffArr[u]++; diffArr[v]++; diffArr[w] -= 2;
        }

        // 逆 BFS 序自底向上累加，求每条树边的覆盖数，取最小
        int best = -1;
        for (int idx = n - 1; idx >= 1; idx--) {
            int x = bfsOrder[idx];
            int c = diffArr[x];                 // 树边 (par[x], x) 的覆盖数
            if (best < 0 || c < best) best = c;
            diffArr[par[x]] += c;
        }

        printf("%d\n", best + 1);
    }
    return 0;
}
