// 一本通 1734《删边问题》标程（C++17, stdin -> stdout）
//
// 题意：n 个点 m 条边的**无向图**（点、边均从 0 编号，允许重边与自环），
//       Q 次询问，每次给出边编号 x，问删去该边后图中「互不可达的无序点对 (u,v)」
//       有多少个，答案模 1000 输出（题面 输出 小节：结果保留后三位(即模 1000)）。
//
// 关键读法（由题面样例唯一确定）：统计的是删边后**全图**互不可达的无序点对，
//   包含删边前就已经不可达的点对。样例 n=4（点 3 孤立）、3 条边 0:(0,1) 1:(1,0) 2:(0,2)：
//     初始不可达点对 = C(4,2) - C(3,2) - C(1,2) = 6 - 3 - 0 = 3；
//     删 x=0（重边之一，非桥）→ 3 ✓；删 x=1 → 3 ✓；
//     删 x=2（桥，切出 {2} 与 {0,1}）→ 3 + 1*2 = 5 ✓。与输出 3 3 5 完全一致。
//
// 算法（Tarjan 求桥 + 并查集连通块 + DFS 树子树大小，O(n + m + Q)）：
//   1) 并查集求连通块大小，T0 = C(n,2) - Σ C(sz_c,2) 为初始互不可达点对数。
//   2) 删一条边只有在该边是所在连通块的桥时才会改变可达性：设该连通块大小为 C，
//      桥把 DFS 树子树部分（大小 s）与其余部分（C - s）分开，
//      则新增互不可达点对 s*(C-s)。故 ans(x) = T0 + [x 是桥]*s*(C-s)。
//   3) 重边：dfs 判桥时只跳过「与父边同编号」的那条边（按边编号而非父顶点跳过），
//      因此两条平行边互认为返祖边，都不会被误判为桥；自环同理不影响连通性。
//   4) n、m、Q 最大 1e5 / 1e6 / 8e5，DFS 用**显式栈迭代**实现，避免链状数据递归爆栈。
//
// 参考来源（**未检索到本题 1734 的公开题解**，故为按经典模型自研改写，通用资料如下）：
//   [1] BYVoid《图的割点、桥与双连通分支》 https://byvoid.com/zhs/blog/biconnect/
//       —— 无向图 Tarjan 求桥的标准判定 low[v] > dfn[u]（本标程判桥依据）。
//       该文亦出现在针对本题的检索结果中（bing/brave 关键词「无向图 删去某条边 桥 题解」）。
//   [2] LeetCode 2316 Count Unreachable Pairs of Nodes in an Undirected Graph
//       https://leetcode.cn/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/
//       —— 初始互不可达点对 = C(n,2) - Σ C(组件大小,2)，与本题样例验证出的 T0 部分一致。
//   [3] 洛谷 P1656 炸铁路 https://www.luogu.com.cn/problem/P1656 —— 桥模板题（判定式同 [1]）。
//   [4] 重边按边编号跳过父边：oi-wiki 图论概念 / Tarjan 割边说明（重边与自环处理）。
//   检索过程：题面特征句「删去编号为x的边后，会有多少个无序点对」「一本通 1734 删边问题
//   (题解)」「ybtoj 1734」在 Bing / Brave / Sogou / CSDN 站内搜索均无本题公开代码，
//   命中的都是同名的「删两条边」「删边最短路」等他题，未采用。
//
// 样例验证：输入 4 3 3 / 0 1 / 1 0 / 0 2 / 0 1 2 → 输出 3 3 5（与题面输出一致）。

#include <cstdio>
#include <vector>

using namespace std;

namespace {

// ---------------- 快速读入 / 输出 ----------------
const int BUF = 1 << 16;
char inBuf[BUF];
int inPos = 0, inLen = 0;

inline int readChar() {
    if (inPos == inLen) {
        inLen = (int)fread(inBuf, 1, BUF, stdin);
        inPos = 0;
        if (inLen <= 0) return -1;
    }
    return inBuf[inPos++];
}

inline int readInt() {
    int c = readChar();
    while (c != -1 && (c < '0' || c > '9')) c = readChar();
    if (c == -1) return -1;
    int x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = readChar();
    }
    return x;
}

char outBuf[BUF];
int outPos = 0;

inline void flushOut() {
    if (outPos) {
        fwrite(outBuf, 1, outPos, stdout);
        outPos = 0;
    }
}

inline void putChar(char c) {
    if (outPos == BUF) flushOut();
    outBuf[outPos++] = c;
}

inline void writeInt(long long x) {
    char t[24];
    int n = 0;
    if (x == 0) t[n++] = '0';
    while (x > 0) {
        t[n++] = (char)('0' + (int)(x % 10));
        x /= 10;
    }
    while (n > 0) putChar(t[--n]);
    putChar('\n');
}

}  // namespace

// 数组上限按题面上限开安全系数：n <= 1e5 -> ×2；m <= 1e6 -> +10 余量；邻接表 2m 条弧。
const int MAXN = 100000 * 2 + 10;
const int MAXM = 1000000 + 10;
const int MAXE = MAXM * 2 + 10;

int n, m, Q;

int head[MAXN];   // 邻接表头（-1 为空）
int to[MAXE];     // 弧终点
int nxt[MAXE];    // 下一条弧
int en = 0;       // 弧计数；第 k 条输入边的两条有向弧编号为 2k 与 2k+1

int dsu[MAXN];    // 并查集
int dsz[MAXN];    // 并查集大小（仅根有效）

int dfn[MAXN], low[MAXN];
int pe[MAXN];     // 该点在 DFS 树中的父边编号（-1 表示无）
int sub[MAXN];    // DFS 树子树大小
int iter[MAXN];   // 显式栈 DFS 的当前弧指针
int childOfEdge[MAXM];  // 该边为桥时，它在 DFS 树中的孩子端点；否则 -1

int findRoot(int x) {
    while (dsu[x] != x) {
        dsu[x] = dsu[dsu[x]];
        x = dsu[x];
    }
    return x;
}

int main() {
    n = readInt();
    m = readInt();
    Q = readInt();
    if (n < 0) return 0;  // 空输入保护（本题必有输入）

    for (int i = 0; i < n; i++) {
        head[i] = -1;
        dsu[i] = i;
        dsz[i] = 1;
        dfn[i] = 0;
        pe[i] = -1;
        sub[i] = 1;
    }
    for (int i = 0; i < m; i++) childOfEdge[i] = -1;

    for (int i = 0; i < m; i++) {
        int u = readInt(), v = readInt();
        to[en] = v; nxt[en] = head[u]; head[u] = en++;
        to[en] = u; nxt[en] = head[v]; head[v] = en++;
        int a = findRoot(u), b = findRoot(v);
        if (a != b) {
            if (dsz[a] < dsz[b]) { int t = a; a = b; b = t; }
            dsu[b] = a;
            dsz[a] += dsz[b];
        }
    }

    // T0：删边前全图的互不可达无序点对数
    long long T0 = (long long)n * (n - 1) / 2;
    for (int i = 0; i < n; i++)
        if (findRoot(i) == i) T0 -= (long long)dsz[i] * (dsz[i] - 1) / 2;

    // 迭代式 Tarjan 求桥 + DFS 树子树大小（重边按边编号跳过父边）
    vector<int> stk;
    stk.reserve(n);
    int timer = 0;
    for (int s = 0; s < n; s++) {
        if (dfn[s]) continue;
        dfn[s] = low[s] = ++timer;
        iter[s] = head[s];
        stk.clear();
        stk.push_back(s);
        while (!stk.empty()) {
            int u = stk.back();
            if (iter[u] != -1) {
                int e = iter[u];
                iter[u] = nxt[e];
                if ((e >> 1) == pe[u]) continue;  // 父边（两个方向）都不走
                int v = to[e];
                if (!dfn[v]) {
                    dfn[v] = low[v] = ++timer;
                    pe[v] = e >> 1;
                    sub[v] = 1;
                    iter[v] = head[v];
                    stk.push_back(v);
                } else if (dfn[v] < low[u]) {
                    low[u] = dfn[v];
                }
            } else {
                stk.pop_back();
                if (!stk.empty()) {
                    int p = stk.back();
                    sub[p] += sub[u];
                    if (low[u] < low[p]) low[p] = low[u];
                    if (low[u] > dfn[p]) childOfEdge[pe[u]] = u;  // 桥
                }
            }
        }
    }

    for (int q = 0; q < Q; q++) {
        int x = readInt();
        long long ans = T0;
        int ch = childOfEdge[x];
        if (ch >= 0) {  // 桥：切出 s 与 C-s 两部分
            long long C = dsz[findRoot(ch)];
            long long s = sub[ch];
            ans += s * (C - s);
        }
        writeInt(ans % 1000);
    }
    flushOut();
    return 0;
}
