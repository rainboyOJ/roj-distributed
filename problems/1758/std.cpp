/* ===========================================================================
 * 一本通 1758《连通能力》 标准程序 std.cpp
 * ---------------------------------------------------------------------------
 * 题意：给定一棵以 1 号点为根的带权树（N 点 N-1 边）。对每个点 i，取"以 i 为根
 *       的子树"（即 i 的全部后代构成的连通块）。在这棵子树中，某点的代价 = 它到
 *       子树内其它点的距离最大值（偏心距），连通能力 = 代价最小的点的代价，即
 *       子树的"半径"。求所有 i 的答案，输出 N 行。
 *
 * 算法（O(N log N)）：
 *   1) 树形 DP 求每个子树 i 的：
 *        f1[i], p1[i] : i 的子树中离 i 最远的点及其距离（最长链）
 *        f2[i], p2[i] : 次长链（来自另一棵孩子子树），无则为 0 / i 本身
 *        D[i]         : 子树 i 的直径 = max( max_child D[c] , f1[i]+f2[i] )
 *   2) 关键结论：对树上任意直径端点 (a,b)，任意点 v 的偏心距 = max(d(v,a),d(v,b))，
 *      故半径 = min_{v 在 a-b 路径上} max(d(v,a),d(v,b))，最优点就是"离直径中点最近
 *      的那个点"。
 *   3) 若 D[i] 由某孩子子树继承（max_child D[c] > f1+f2），则半径 R[i] = R[c]
 *      （(a,b) 仍是 i 的直径端点，子树外的点只会更远）。
 *      否则直径穿过 i，端点为 p1[i]、p2[i]，用**树上倍增**把 p1 沿祖先往上跳，
 *      找到最高的、仍满足 d(p1,x) <= d(x,p2) 的点 x（即中点的左侧点），
 *      答案取 min( max(d(p1,x),d(x,p2)), max(d(p1,fa[x]),d(fa[x],p2)) )。
 *
 * 来源 / 依据（网络检索到的公开题解，算法完全一致）：
 *   - CSDN《连通能力[树形DP][树上倍增]》
 *     https://blog.csdn.net/sslz_fsy/article/details/82179452
 *   - CSDN《【2018/07/26测试T3】【SOJ 1912】连通能力》
 *     https://blog.csdn.net/forever_dreams/article/details/81218182
 *   - CSDN《【NOIP模拟】连通能力》
 *     https://blog.csdn.net/ashley_2013/article/details/101711820
 *   本程序在其基础上做了必要的健壮化改写：
 *   (a) 所有距离/答案用 long long —— 参考代码用 int，而 N=1e6、w<=1e4 时距离
 *       可达 1e10，int 必然溢出；
 *   (b) 递归 DFS 改为迭代 BFS（N=1e6 的链会爆栈），并顺带算出倍增表；
 *   (c) 手写快读快写（N=1e6 输入约 20MB）。
 * ===========================================================================
 */
#include <cstdio>
#include <cstring>
#include <cstdlib>

static const int MAXN = 1000005;
/* 2^20-1 = 1048575 > 1e6，故 20 层（j=0..19）足够覆盖任意祖先跳跃 */
static const int LOG = 20;

static int n;
static int head[MAXN], nxt[2 * MAXN], to[2 * MAXN], wt[2 * MAXN];
static int ecnt;

static int dep[MAXN];                 /* 深度（边数+1） */
static int p1[MAXN], p2[MAXN];        /* 最长/次长链端点 */
static int order[MAXN];               /* BFS 序，逆序即自底向上 */
static long long dis[MAXN];           /* 到根的距离 */
static long long f1[MAXN], f2[MAXN];  /* 最长/次长链长度 */
static long long dia[MAXN];           /* 子树直径 */
static long long ans[MAXN];           /* 子树半径 = 答案 */

static int fa[LOG][MAXN];             /* 倍增祖先 */

/* ---------------- 快读 ---------------- */
static char ibuf[1 << 20];
static int ilen = 0, ipos = 0;

static inline int gc() {
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen <= 0) return -1;
    }
    return (unsigned char)ibuf[ipos++];
}
static inline int readInt() {
    int c = gc();
    while (c != -1 && (c < '0' || c > '9')) c = gc();
    if (c == -1) return -1;
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

/* ---------------- 快写 ---------------- */
static char obuf[1 << 22];
static int olen = 0;

static inline void oflush() {
    if (olen) { fwrite(obuf, 1, olen, stdout); olen = 0; }
}
static inline void oputc(char c) {
    if (olen == (int)sizeof(obuf)) oflush();
    obuf[olen++] = c;
}
static inline void oputll(long long x) {
    char t[24];
    int k = 0;
    if (x == 0) t[k++] = '0';
    while (x > 0) { t[k++] = (char)('0' + (int)(x % 10)); x /= 10; }
    while (k) oputc(t[--k]);
}

static inline void addEdge(int u, int v, int w) {
    ++ecnt; to[ecnt] = v; wt[ecnt] = w; nxt[ecnt] = head[u]; head[u] = ecnt;
    ++ecnt; to[ecnt] = u; wt[ecnt] = w; nxt[ecnt] = head[v]; head[v] = ecnt;
}

int main() {
    n = readInt();
    if (n <= 0) n = 1;                     /* 极端防御，正常 N>=1 */

    for (int i = 1; i < n; ++i) {
        int u = readInt(), v = readInt(), w = readInt();
        addEdge(u, v, w);
    }

    /* ---- BFS 定根（根为 1），同时建倍增表 ---- */
    int qt = 0;
    order[qt++] = 1;
    dep[1] = 1;
    dis[1] = 0;
    for (int j = 0; j < LOG; ++j) fa[j][1] = 0;
    for (int qh = 0; qh < qt; ++qh) {
        int u = order[qh];
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to[e];
            if (v == fa[0][u]) continue;   /* 父亲（树上无重边） */
            fa[0][v] = u;
            dep[v] = dep[u] + 1;
            dis[v] = dis[u] + wt[e];
            for (int j = 1; j < LOG; ++j) fa[j][v] = fa[j - 1][fa[j - 1][v]];
            order[qt++] = v;
        }
    }

    /* ---- 逆 BFS 序做树形 DP ---- */
    for (int i = 1; i <= n; ++i) {
        ans[i] = 0; dia[i] = 0; f1[i] = 0; f2[i] = 0;
        p1[i] = i; p2[i] = i;
    }

    for (int idx = qt - 1; idx >= 0; --idx) {
        int cur = order[idx];
        for (int e = head[cur]; e; e = nxt[e]) {
            int t = to[e];
            if (t == fa[0][cur]) continue;
            /* 孩子直径更大 -> 先继承（半径相同，见头注第 3 点） */
            if (ans[t] > ans[cur]) { dia[cur] = dia[t]; ans[cur] = ans[t]; }
            /* 更新最长 / 次长链 */
            long long val = f1[t] + wt[e];
            if (val > f1[cur]) {
                f2[cur] = f1[cur]; p2[cur] = p1[cur];
                f1[cur] = val;     p1[cur] = p1[t];
            } else if (val > f2[cur]) {
                f2[cur] = val;     p2[cur] = p1[t];
            }
        }
        if (dia[cur] < f1[cur] + f2[cur]) {     /* 直径穿过 cur，需重算半径 */
            dia[cur] = f1[cur] + f2[cur];
            int x = p1[cur];
            for (int j = LOG - 1; j >= 0; --j) {
                int a = fa[j][x];
                /* a 必须在 cur 的子树内（不能跳出子树），且 d(p1,a) <= d(a,p2) */
                if (dep[a] >= dep[cur] &&
                    f1[cur] - (dis[a] - dis[cur]) <= f2[cur] + (dis[a] - dis[cur]))
                    x = a;
            }
            long long best = f2[cur] + (dis[x] - dis[cur]);   /* d(x,p2) */
            int px = fa[0][x];
            long long alt = f1[cur] - (dis[px] - dis[cur]);   /* d(p1,fa[x]) */
            if (alt < best) best = alt;
            ans[cur] = best;
        }
    }

    for (int i = 1; i <= n; ++i) { oputll(ans[i]); oputc('\n'); }
    oflush();
    return 0;
}
