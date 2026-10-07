// 一本通 1729《魔法石》标程（多组数据，C++17）
//
// 题意（见 .ybt-import/staging/1729/content.md）：
//   n 个岛、m 条石桥，桥心石墩上可能有魔法石（输入边权 c=1 表示有）。
//   约翰尼从 src 走到 dst，每条桥（无向）只能走一次（走过即崩塌，不能回头）。
//   问能否在途中收集到至少一块魔法石并安全到达 dst。
//
// 本题即 Codeforces 652E "Pursuit For Artifacts"（Johnny、每条边只能走一次、
// 求 a→b 是否存在经过至少一条权 1 边的 trail），题面样例逐组一致（3 组 YES/NO/YES）。
//
// 来源 URL：
//   1. https://codeforces.com/problemset/problem/652/E
//      —— 英文原题（判定为同题：人物 Johnny、"每条边只能通过一次"、边权 0/1、多组数据、n,m<=3e5）
//      另见题解页 https://www.luogu.com.cn/problem/CF652E
//   2. https://ddosvoid.github.io/2021/03/03/CF-652E-Pursuit-For-Artifacts/
//      —— 思路来源：「边双缩点成一棵树；若 s→t 的路径上某个边双内部有权 1 的边，
//         或路径上的割边有权 1，则 YES」；并给出 tarjan 求割边 + 缩点 + dfs 找路径的实现。
//   3. https://blog.csdn.net/weixin_42750325/article/details/102555860
//      —— 第二份独立实现（同为边双缩点；其写法额外在 s,t 间连一条虚边再判 s,t 是否同边双），
//         结论与来源 2 一致，用于交叉确认判定准则。
//
// 判定准则（与来源 2/3 等价，本实现采用更直接的路径判据）：
//   1) 对图做 tarjan 求割边，将非割边连通块（边双, e-DCC）缩点，得到一棵"桥树"；
//   2) 设 P 为桥树上 comp[src] → comp[dst] 的路径；
//   3) 答案 = YES ⇔ (P 上存在权 1 的桥) 或 (P 上任一边双内部存在权 1 的边)；
//      否则 NO；若 comp[dst] 不可达（图不连通）也输出 NO。
//   依据：边双内任意两点间存在欧拉式走法，可以顺路走遍内部的任何一条边（含权 1 边）
//   且每条边只用一次（2-边连通 ⇒ 任意顶点到任一条边端点存在两条边不交路径）；而桥必须
//   按 P 的方向各用一次，不能绕到 P 的分支再回来。
//   例：题面样例第 3 组 {1,2,3}∪{3,4,5} 整块 2-边连通，内部有权 1 边 ⇒ YES。
//
// 本实现相对来源的改写点：
//   - 迭代式 tarjan（显式栈）：n=3e5 的长链若用递归 DFS 会爆栈，题面上限内必须迭代；
//   - fread 快读 / 手写输出缓冲：Σm 可达 10*3e5=3e6 条边，需避免 cin 慢读；
//   - 割边判定按"边下标"跳过父边（eid^1），因此**重边**（两岛之间多座桥）与自环都被正确处理；
//   - 不保证图连通：src 与 dst 不在同一连通块时输出 NO（题面未承诺连通）；
//   - 每组复杂度 O(n+m)，一次性复用全局数组并按下标覆盖。
//
// 编译：g++ -O2 -std=c++17 -Wall -Wextra std.cpp -o std

#include <cstdio>
#include <cstring>
#include <cstdlib>

namespace {

const int MAXN = 300000 + 5;
const int MAXM = 300000 + 5;

int n, m;
int head[MAXN];          // 静态邻接表头
int eto[2 * MAXM];       // 边端点
int enxt[2 * MAXM];      // 下一条边
int ewt[2 * MAXM];       // 边权（0/1，1 表示桥心有魔法石）
int ecnt;

int dfn[MAXN], low[MAXN];
int itEdge[MAXN];        // 迭代 DFS 时当前扫描到的边
int parEdge[MAXN];       // 结点在 DFS 树中的入边（边下标）
unsigned char isBridge[2 * MAXM];

int dsuFa[MAXN], dsuSz[MAXN];
int comp[MAXN];          // 结点所属边双编号（用 DSU 根表示）
unsigned char dccHas[MAXN];

// 桥树邻接表
int thead[MAXN], tto[2 * MAXM], tnxt[2 * MAXM], twt[2 * MAXM], tcnt;

int stk[MAXN];           // 迭代 tarjan 用的栈
int bfsq[MAXN];
unsigned char seen[MAXN];
unsigned char acc[MAXN]; // 桥树上从 comp[src] 出发的路径 OR 值

inline void addEdge(int u, int v, int w) {
    eto[ecnt] = v; ewt[ecnt] = w; enxt[ecnt] = head[u]; head[u] = ecnt++;
}
inline void addTreeEdge(int u, int v, int w) {
    tto[tcnt] = v; twt[tcnt] = w; tnxt[tcnt] = thead[u]; thead[u] = tcnt++;
}

int findRoot(int x) {
    int r = x;
    while (dsuFa[r] != r) r = dsuFa[r];
    while (dsuFa[x] != r) { int nx = dsuFa[x]; dsuFa[x] = r; x = nx; }
    return r;
}
inline void unite(int a, int b) {
    a = findRoot(a); b = findRoot(b);
    if (a == b) return;
    if (dsuSz[a] < dsuSz[b]) { int t = a; a = b; b = t; }
    dsuFa[b] = a; dsuSz[a] += dsuSz[b];
}

// ---------------- 快读 / 快写 ----------------
char inBuf[1 << 22];
size_t inLen = 0, inPos = 0;
inline int readInt() {
    if (inPos == inLen) {
        inLen = fread(inBuf, 1, sizeof(inBuf), stdin);
        inPos = 0;
        if (inLen == 0) return -1;
    }
    while (inPos < inLen && (inBuf[inPos] < '0' || inBuf[inPos] > '9')) {
        if (++inPos == inLen) {
            inLen = fread(inBuf, 1, sizeof(inBuf), stdin);
            inPos = 0;
            if (inLen == 0) return -1;
        }
    }
    int x = 0;
    while (inPos < inLen && inBuf[inPos] >= '0' && inBuf[inPos] <= '9') {
        x = x * 10 + (inBuf[inPos] - '0');
        if (++inPos == inLen) {
            inLen = fread(inBuf, 1, sizeof(inBuf), stdin);
            inPos = 0;
            if (inLen == 0) break;
        }
    }
    return x;
}

char outBuf[1 << 16];
size_t outPos = 0;
inline void outFlush() {
    if (outPos) { fwrite(outBuf, 1, outPos, stdout); outPos = 0; }
}
inline void outStr(const char *s, int len) {
    if (outPos + (size_t)len > sizeof(outBuf)) outFlush();
    for (int i = 0; i < len; ++i) outBuf[outPos++] = s[i];
}

} // namespace

int main() {
    int T = readInt();
    if (T < 0) T = 0;
    while (T--) {
        n = readInt(); m = readInt();
        if (n < 0) n = 0;
        if (m < 0) m = 0;

        // 清空按本次使用范围（避免 T 组间 O(MAXN) 反复 memset 造成常数浪费）
        for (int i = 1; i <= n; ++i) {
            head[i] = -1;
            dfn[i] = 0;
            parEdge[i] = -1;
            dsuFa[i] = i; dsuSz[i] = 1;
            thead[i] = -1;
            seen[i] = 0; acc[i] = 0;
            dccHas[i] = 0;
        }
        ecnt = 0; tcnt = 0;

        for (int i = 0; i < m; ++i) {
            int x = readInt(), y = readInt(), c = readInt();
            if (c < 0) c = 0;
            addEdge(x, y, c);
            addEdge(y, x, c);
        }
        for (int i = 0; i < ecnt; ++i) isBridge[i] = 0;

        // ---- 迭代式 tarjan 求割边（按边下标跳过父边，重边/自环安全）----
        int timer = 0;
        for (int root = 1; root <= n; ++root) {
            if (dfn[root]) continue;
            int top = 0;
            stk[top++] = root;
            dfn[root] = low[root] = ++timer;
            itEdge[root] = head[root];
            parEdge[root] = -1;
            while (top > 0) {
                int u = stk[top - 1];
                int e = itEdge[u];
                if (e != -1) {
                    itEdge[u] = enxt[e];
                    if (parEdge[u] != -1 && e == (parEdge[u] ^ 1)) continue; // 跳过 DFS 树父边的反向边
                    int v = eto[e];
                    if (!dfn[v]) {
                        parEdge[v] = e;
                        itEdge[v] = head[v];
                        dfn[v] = low[v] = ++timer;
                        stk[top++] = v;
                    } else if (dfn[v] < low[u]) {
                        low[u] = dfn[v];
                    }
                } else {
                    --top;
                    int pe = parEdge[u];
                    if (pe != -1) {
                        int p = eto[pe ^ 1];      // u 的父亲
                        if (low[u] < low[p]) low[p] = low[u];
                        if (low[u] > dfn[p]) {    // (p,u) 是割边
                            isBridge[pe] = 1;
                            isBridge[pe ^ 1] = 1;
                        }
                    }
                }
            }
        }

        // ---- 非割边连通块 = 边双，DSU 缩点 ----
        for (int e = 0; e < ecnt; e += 2) {
            if (!isBridge[e]) unite(eto[e], eto[e ^ 1]);
        }
        for (int v = 1; v <= n; ++v) comp[v] = findRoot(v);
        for (int e = 0; e < ecnt; e += 2) {
            if (!isBridge[e]) {
                if (ewt[e]) dccHas[comp[eto[e]]] = 1;   // 边双内部有权 1 的边
            } else {
                addTreeEdge(comp[eto[e]], comp[eto[e ^ 1]], ewt[e]);
                addTreeEdge(comp[eto[e ^ 1]], comp[eto[e]], ewt[e]);
            }
        }

        int src = readInt(), dst = readInt();
        if (src < 1 || src > n || dst < 1 || dst > n) {  // 防御：越界输入按不可达处理
            outStr("NO\n", 3);
            continue;
        }
        int cs = comp[src], cd = comp[dst];

        // ---- 桥树上 BFS，累积路径上的 (边双内部 1) 与 (桥权 1) ----
        int qh = 0, qt = 0;
        bfsq[qt++] = cs; seen[cs] = 1; acc[cs] = dccHas[cs];
        while (qh < qt) {
            int u = bfsq[qh++];
            for (int e = thead[u]; e != -1; e = tnxt[e]) {
                int v = tto[e];
                if (seen[v]) continue;
                seen[v] = 1;
                unsigned char f = acc[u];
                if (twt[e]) f = 1;
                if (dccHas[v]) f = 1;
                acc[v] = f;
                bfsq[qt++] = v;
            }
        }

        if (seen[cd] && acc[cd]) outStr("YES\n", 4);
        else outStr("NO\n", 3);
    }
    outFlush();
    return 0;
}
