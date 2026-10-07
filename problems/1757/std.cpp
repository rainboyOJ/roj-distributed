// 一本通 1757《避难向导》 标程（C++17）
// ---------------------------------------------------------------------------
// 原题：P3489【2015多校联训5】避难向导（by BZ），亦见 CQBZOJ2937 / NKOJ3489。
// 来源依据（网络检索，2025 实抓）：
//   [1] https://blog.csdn.net/c20182024/article/details/77119718
//       《CQBZOJ 【重庆市NOIP模拟赛】避难向导》—— 含完整 AC 代码（树 DP 求最远点 +
//       树上倍增 f/g 数组 + getg1/getg2 拆分路径查询），本标程的查询框架依据此文。
//   [2] https://blog.csdn.net/getsum/article/details/53038726
//       《NOIP 2015模拟赛[八中题]题解&总结》—— 含完整 AC 代码，明确指出「先求一条直径，
//       到直径的某一个端点一定是最远距离」，再用倍增 maxq 数组求路径区间最值。本标程
//       的 d_i 求法（直径两端点）依据此文。
//   [3] https://blog.csdn.net/mogician_evian/article/details/78397281
//       《NKOJ 3489 避难向导（LCA+倍增+DFS/DP）》—— 算法说明（Maxdis[i][k] 为 i 的父亲
//       往上 2^k 个节点中最大安全系数）。
//   [4] https://blog.csdn.net/rgnoh/article/details/78492532
//       《避难向导 树的直径 树上倍增 二分答案》—— 同源题解（标题即思路）。
//   [5] https://blog.csdn.net/dingwufu9301/article/details/102100261
//       《省选专练之避难向导》—— 树形 DP + ST 表倍增。
//   另见 CSDN 检索命中：fire_crazy/102511196、c20181220_xiang_m_y/102488306、
//   outer_form/49047115、weixin_30652271/95261056 等，均为同题同解。
//
// 题意：
//   树 n 个点（1 号首都），边带正权；叶子（度数=1）称边境城市。
//   封闭系数 d_i = 城市 i 到「最远的边境城市」的距离；
//   安全系数 S_i = (d_i + a) * b mod c。
//   m 次询问 (x,y,q)：在 x→y 的唯一路径上，求离 x 最近的、S>=q 的城市编号，无则 -1。
//
// 算法（O((n+m) log n)）：
//   1) 树的直径端点 A、B（两遍 DFS）。树上「离 i 最远的点必是直径端点」，而直径端点
//      必是叶子（度数 1），故 d_i = max(dist(i,A), dist(i,B))。
//   2) S_i = (d_i + a) * b % c（中间量用 64 位）。
//   3) 以 1 为根求 dep / up[k][v]（2^k 级祖先）；MXE[k][v] = v 往上 2^k 个点（含 v）的
//      S 最大值（稀疏表）：MXE[k][v] = max S over 距离 v 0..2^k 的 2^k+1 个点（含 v 与 2^k 级祖先）。
//   4) 询问：l = LCA(x,y)，路径拆成 x→l 与 l→y 两段：
//        · 先在 x→l 段求「离 x 最近」的合法点（getDeepest：从 x 向上贪心跳，块内全非法则跳过）；
//        · 该段无解再在 l→y 段求「离 l 最近」（= 离 x 最近）的合法点
//          （getShallowest：先递归搜靠 l 的上半段，再在下方 2^t 块内二分定位最靠上者）。
//      两段内部块均为连续链段，贪心跳 + 末位检查即可，单次询问 O(log n)。
//
// 复杂度：预处理 O(n log n)，每次询问 O(log n)。n<=1e5, m<=3e5 → 约 1e7 次操作，1s 内可过。
// 数组按题面上限 ×2 安全系数开（MAXN=200005），LOG=19（2^19>2e5）。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

static const int MAXN = 200005;   // 题面 n<=100000，×2 安全系数
static const int LOG  = 19;       // 2^19 = 524288 > MAXN
static const int NEG  = -1;       // 不存在的节点：S 值视作 -1（S>=0 恒成立）

static int N, M;
static long long A, B, C;

static int head[MAXN], nxt[2 * MAXN], to[2 * MAXN], ecnt;
static long long wt[2 * MAXN];

static long long distA[MAXN], distB[MAXN];
static int Sv[MAXN];
static int dep[MAXN], par[MAXN];
static int up[LOG + 1][MAXN];
static int MXE[LOG + 1][MAXN];    // MXE[k][v] = max S over {v, up[0][v], ..., up[k-1][v]} (2^k 个点)
static int lg2tab[MAXN];
static int stk[MAXN];

static inline void addEdge(int u, int v, long long w) {
    to[ecnt] = v; wt[ecnt] = w; nxt[ecnt] = head[u]; head[u] = ecnt++;
}

// ---- 快速读入 ----
static char ibuf[1 << 20];
static int ipos = 0, ilen = 0;
static inline int gc() {
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen <= 0) return -1;
    }
    return (unsigned char)ibuf[ipos++];
}
static inline long long readLL() {
    int c = gc();
    while (c != -1 && c != '-' && (c < '0' || c > '9')) c = gc();
    int sign = 1;
    if (c == '-') { sign = -1; c = gc(); }
    long long x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x * sign;
}
static inline int readInt() { return (int)readLL(); }

// ---- 树的直径：从 src 出发 DFS，回填 dist[]，返回最远点 ----
static int farthest(int src, long long *dist) {
    int top = 0;
    stk[top++] = src;
    par[src] = 0;
    dist[src] = 0;
    int best = src;
    while (top > 0) {
        int u = stk[--top];
        if (dist[u] > dist[best]) best = u;
        for (int e = head[u]; e != -1; e = nxt[e]) {
            int v = to[e];
            if (v == par[u]) continue;
            par[v] = u;
            dist[v] = dist[u] + wt[e];
            stk[top++] = v;
        }
    }
    return best;
}

// ---- 以 1 为根，BFS 求 dep / par ----
static int order[MAXN];
static void buildRooted() {
    int qh = 0, qt = 0;
    order[qt++] = 1;
    par[1] = 0;
    dep[1] = 0;
    while (qh < qt) {
        int u = order[qh++];
        for (int e = head[u]; e != -1; e = nxt[e]) {
            int v = to[e];
            if (v == par[u]) continue;
            par[v] = u;
            dep[v] = dep[u] + 1;
            order[qt++] = v;
        }
    }
}

static inline int lca(int u, int v) {
    if (dep[u] < dep[v]) { int t = u; u = v; v = t; }
    int d = dep[u] - dep[v];
    for (int k = 0; k <= LOG; k++)
        if ((d >> k) & 1) u = up[k][u];
    if (u == v) return u;
    for (int k = LOG; k >= 0; k--)
        if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
    return up[0][u];
}

// x→anc（anc 是 x 的祖先）这一段上「离 x 最近」的合法点（即最深者）；无则 -1。
static int getDeepest(int u, int anc, int q) {
    if (Sv[u] >= q) return u;
    int cur = u;
    for (int k = LOG; k >= 0; k--) {
        int dest = up[k][cur];
        if (dest == 0) continue;                 // 不存在
        if (dep[dest] < dep[anc]) continue;      // 会越过 anc
        // 不变量：cur 本身非法（S[cur] < q），故 MXE[k][cur] 含 cur 亦不影响判定；
        // MXE[k][cur] >= q ⇔ cur 上方 2^k 个点中有合法者。
        if (MXE[k][cur] < q) cur = dest;         // cur 上方 2^k 个点全非法 → 跳过
    }
    if (dep[cur] > dep[anc] && Sv[up[0][cur]] >= q) return up[0][cur];
    return -1;
}

// x→y（y 是 x 的祖先）这一段上「离 y 最近」的合法点（即最浅者）；无则 -1。
static int getShallowest(int x, int y, int q) {
    if (x == y) return Sv[x] >= q ? x : -1;
    int L = dep[x] - dep[y];
    int t = lg2tab[L];
    int topX = up[t][x];
    int res = getShallowest(topX, y, q);         // 先搜靠近 y 的上半段
    if (res != -1) return res;
    // 再在下方 2^t 块 [x, topX] 内找最靠上者
    int mxIn = MXE[t][x];
    if (topX != 0 && Sv[topX] > mxIn) mxIn = Sv[topX];
    if (mxIn >= q) {
        for (int i = t - 1; i >= 0; i--) {
            int pi = up[i][x];
            int m = MXE[i][pi];
            int hi = up[i][pi];
            if (hi != 0 && Sv[hi] > m) m = Sv[hi];
            if (m >= q) x = pi;
        }
        int p = up[0][x];
        return (p != 0 && Sv[p] >= q) ? p : x;
    }
    return -1;
}

int main() {
    N = readInt(); M = readInt();
    A = readLL(); B = readLL(); C = readLL();

    memset(head, -1, sizeof(int) * (N + 1));
    ecnt = 0;
    for (int i = 1; i < N; i++) {
        int u = readInt(), v = readInt();
        long long w = readLL();
        addEdge(u, v, w);
        addEdge(v, u, w);
    }

    // 1) 直径端点 → d_i = max(dist(i,A), dist(i,B))
    if (N >= 2) {
        // 三遍 DFS：1 -> a0；a0 -> b0（同时 distA 变为「到 a0 的距离表」）；b0 -> distB。
        // 树的性质：任意点的最远点必是直径端点 a0 / b0 之一，故 d_i = max(distA[i], distB[i])。
        int a0 = farthest(1, distA);
        int b0 = farthest(a0, distA);
        farthest(b0, distB);
        (void)b0;
        for (int i = 1; i <= N; i++) {
            long long d = distA[i] > distB[i] ? distA[i] : distB[i];
            if (C == 0) Sv[i] = 0;
            else Sv[i] = (int)(((d + A) % C) * (B % C) % C);
        }
    } else {
        // n == 1：无边境城市，按两端点退化为自身，d_1 = 0（与各公开实现一致）
        Sv[1] = (C == 0) ? 0 : (int)(((0 + A) % C) * (B % C) % C);
    }

    // 2) 倍增表
    memset(up, 0, sizeof(up));
    memset(MXE, 0, sizeof(MXE));
    for (int i = 0; i < LOG + 1; i++) MXE[i][0] = NEG;
    buildRooted();
    for (int v = 1; v <= N; v++) {
        up[0][v] = par[v];
        int p = par[v];
        MXE[0][v] = Sv[v];
        if (p != 0 && Sv[p] > MXE[0][v]) MXE[0][v] = Sv[p];
    }
    for (int k = 1; k <= LOG; k++) {
        for (int v = 1; v <= N; v++) {
            int mid = up[k - 1][v];
            up[k][v] = mid ? up[k - 1][mid] : 0;
            int m = MXE[k - 1][v];
            int m2 = mid ? MXE[k - 1][mid] : NEG;
            MXE[k][v] = m > m2 ? m : m2;
        }
    }
    lg2tab[1] = 0;
    for (int i = 2; i <= N; i++) lg2tab[i] = lg2tab[i >> 1] + 1;

    // 3) 询问
    char obuf[1 << 20];
    int olen = 0;
    for (int i = 0; i < M; i++) {
        int x = readInt(), y = readInt(), q = readInt();
        int ans;
        if (x == y) {
            ans = (Sv[x] >= q) ? x : -1;
        } else {
            int l = lca(x, y);
            int a1 = getDeepest(x, l, q);
            if (a1 != -1) ans = a1;
            else ans = getShallowest(y, l, q);
        }
        if (ans < 0) { obuf[olen++] = '-'; obuf[olen++] = '1'; }
        else {
            char tmp[12]; int tn = 0;
            if (ans == 0) tmp[tn++] = '0';
            while (ans > 0) { tmp[tn++] = char('0' + ans % 10); ans /= 10; }
            while (tn > 0) obuf[olen++] = tmp[--tn];
        }
        obuf[olen++] = '\n';
        if (olen > (1 << 20) - 32) { fwrite(obuf, 1, olen, stdout); olen = 0; }
    }
    if (olen > 0) fwrite(obuf, 1, olen, stdout);
    return 0;
}
