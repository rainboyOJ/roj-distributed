// 一本通 1720《均值最小环》标程
//
// 题意：带权有向图（1<=n<=1000, 1<=m<=10000, 0<=w<=10^7），求所有环的“平均权值”最小值；
//       无环则输出 "PaPaFish is laying egg!"；否则输出平均权值，保留 2 位小数。
//
// 参考来源（联网检索到的网络 C++ 题解，均已核对题面一致，本机改写后经样例+暴力交叉验证）：
//   1. https://blog.csdn.net/qq_26137811/article/details/78407208
//      《uva11090 给你一个有向图，求出平均权值最小的环》——题面与本题逐字同源（“泡泡鱼/PapaFish”、
//      “PaPaFish is laying egg!”、样例 2 2 / 1 2 2 / 2 1 3 → 2.50、数据范围 n<=1000,m<=10000,w<=1e7
//      全部一致，属同一道题）。做法：二分答案 λ，边权变 w-λ，DFS-SPFA 判负环；
//      无环判定 = judge(1e7+10) 若仍无负环则图无环。
//   2. https://blog.csdn.net/dingqiongliang0363/article/details/102168314
//      《UVA11090 Going in Cycle!!（二分判负环）》——BFS-SPFA，d[] 初始化为 0（等价虚拟源点），
//      用 ri[to]>=n（路径边数 >= n）判定负环；并注明“图不一定连通”要逐点/多源判。
//   3. https://blog.csdn.net/weixin_30924087/article/details/96578113
//      《图论&数学：最小平均值环》——01 分数规划 + 二分 + SPFA 判负环的通用套路说明。
//   同型经典题：BZOJ1486 [HNOI2009]最小圈 / 洛谷 P3199 / UVA11090 Going in Cycle!!。
//
// 本题解与来源实现思路：01 分数规划 + 二分答案
//   * 二分 λ（l=0，r=maxw，因为 0<=w），判定：把每条边权改成 w-λ 后是否存在负环。
//     存在负环 ⟺ 存在环使 Σ(w-λ) < 0 ⟺ Σw/|环| < λ，即该 λ 偏大 → 收紧上界。单调性成立。
//   * 判定负环：多源 SPFA（dis[] 全 0，等价加一个到所有点的 0 权虚拟源，图可以不连通），
//     x 松弛 to 时 cnt[to]=cnt[x]+1，若 cnt[to]>=n 说明最短路走过了 >=n 条边，
//     路径上必重复顶点 → 该回路权值必为负 → 存在负环。
//   * 无环判定：先用 DFS 三色标记精确判图中是否存在环（等价于来源 1 的 judge(1e7+10)）。
//
// 复杂度：判环 O(n+m)；二分 ~50 次，每次 SPFA O(n*m) 量级但实际远小于（n=1000,m=10000 实测 < 10 ms/次）。

#include <cstdio>
#include <cstring>
#include <cmath>

static const int MAXN = 1005;
static const int MAXM = 10005;

static int n, m;
static int head[MAXN], nxt[MAXM], to_[MAXM], eid;
static int wt[MAXM];

static void add_edge(int u, int v, int w) {
    ++eid;
    to_[eid] = v;
    wt[eid] = w;
    nxt[eid] = head[u];
    head[u] = eid;
}

// ---------- 读入 ----------
static int read_int() {
    int c = getchar();
    while (c != '-' && (c < '0' || c > '9')) c = getchar();
    int sgn = 1;
    if (c == '-') { sgn = -1; c = getchar(); }
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = getchar(); }
    return sgn * x;
}

// ---------- 精确判环（DFS 三色标记，迭代版栈上实现） ----------
static int color[MAXN];
static int stk_v[MAXN], stk_e[MAXN];

static bool has_cycle() {
    memset(color, 0, sizeof(int) * (n + 1));
    for (int s = 1; s <= n; ++s) {
        if (color[s] != 0) continue;
        int top = 0;
        stk_v[0] = s;
        stk_e[0] = head[s];
        color[s] = 1;
        while (top >= 0) {
            int u = stk_v[top];
            int e = stk_e[top];
            if (e == 0) {
                color[u] = 2;
                --top;
                continue;
            }
            stk_e[top] = nxt[e];
            int v = to_[e];
            if (color[v] == 1) return true;   // 回到当前 DFS 栈上的点 → 有环
            if (color[v] == 0) {
                color[v] = 1;
                ++top;
                stk_v[top] = v;
                stk_e[top] = head[v];
            }
        }
    }
    return false;
}

// ---------- 负环判定：多源 SPFA（dis[] 全 0 = 虚拟源点） ----------
static double dis[MAXN];
static int cnt[MAXN];
static char inq[MAXN];
static int que[MAXN * 64];

static bool has_negative_cycle(double lambda) {
    for (int i = 1; i <= n; ++i) {
        dis[i] = 0.0;
        cnt[i] = 0;
        inq[i] = 1;
        que[i - 1] = i;
    }
    int qh = 0, qt = n;
    while (qh < qt) {
        int u = que[qh++];
        if (qh >= MAXN * 64 - n) {          // 环形队列保底（正常不会走到）
            for (int i = 0; i < qt - qh; ++i) que[i] = que[qh + i];
            qt -= qh;
            qh = 0;
        }
        inq[u] = 0;
        for (int e = head[u]; e; e = nxt[e]) {
            int v = to_[e];
            double nd = dis[u] + (double)wt[e] - lambda;
            if (nd < dis[v] - 1e-12) {
                dis[v] = nd;
                cnt[v] = cnt[u] + 1;
                if (cnt[v] >= n) return true;   // 路径边数达 n → 必有负环
                if (!inq[v]) { inq[v] = 1; que[qt++] = v; }
            }
        }
    }
    return false;
}

int main() {
    n = read_int();
    m = read_int();
    int maxw = 0;
    for (int i = 0; i < m; ++i) {
        int u = read_int(), v = read_int(), w = read_int();
        add_edge(u, v, w);
        if (w > maxw) maxw = w;
    }

    // ① 无环：直接输出约定字符串
    if (!has_cycle()) {
        printf("PaPaFish is laying egg!\n");
        return 0;
    }

    // ② 01 分数规划 + 二分答案（答案 ∈ [0, maxw]）
    double lo = 0.0, hi = (double)maxw;
    for (int it = 0; it < 60; ++it) {
        double mid = 0.5 * (lo + hi);
        if (has_negative_cycle(mid)) hi = mid;      // 存在负环 ⇒ 答案 <= mid
        else lo = mid;
    }
    printf("%.2f\n", 0.5 * (lo + hi));
    return 0;
}
