// 一本通 1762《与非》 标程
// ---------------------------------------------------------------------------
// 来源依据（联网检索）：
//   https://www.cnblogs.com/yiqiAtiya/p/13922033.html  《一本通1762:与非》
//   该文明确本题做法为「树链剖分 + 线段树，对不满足结合律的 nand 运算
//   同时维护两个方向（自上而下 L / 自下而上 R）的复合结果」，并给出关键提示
//   “对于不满足结合律的运算，要处理出两个方向的结果，查询时也要注意方向”。
//   本文献等价改写（非盲抄）：原文按位开 int L[32][N<<2][2] / R[32][N<<2][2]
//   （≈205 MB，作者自述被卡常）；本实现利用「nand 按位独立」这一点，
//   把一段区间的变换压成两个 k 位掩码 (A,B)=(F(0^k), F(1^k))，复合 O(1)，
//   线段树每结点只存正/反两个方向各一对掩码（内存 ≈6 MB）。
//
// 题意（据 content.md 与样例反推，见 gen-report.md「题面复原」）：
//   记 k 位 nand 为 x nand y = ~(x & y)（按位，结果取低 k 位）。
//   Query x y：设 x->y 路径为 S1..SL，f(0)=0，f(i)=f(i-1) nand w[S_i]，
//              输出 f(L)。（等价写法 f(1)=2^k-1，f(i)=f(i-1) nand w[S_i]）
//   Replace x y：w[x]=y。
//
// 算法：
//   nand 每一位独立，故 f 在 k 位向量上诱导一个逐位函数 F，可用
//   A = F(0^k)、B = F(1^k) 唯一表示：F(x) = (x & B) | (~x & A)。
//   单点 b 的 F_b(x) = ~(x & b)，故 A=2^k-1，B=~b。
//   复合 (F_after ∘ F_before)：
//     A = (A_before & B_after) | (~A_before & A_after)
//     B = (B_before & B_after) | (~B_before & A_after)
//   ——函数复合满足结合律，于是可以线段树维护。
//   树链剖分：x 侧路径自下而上（线段树反向复合），y 侧自上而下（正向复合），
//   最后按 “x 侧先、y 侧后” 复合，答案 = 总函数在 0 处的取值 = A。
//   复杂度 O((n + m) log^2 n)，k≤32，unsigned int 即可。
// ---------------------------------------------------------------------------
#include <bits/stdc++.h>
using namespace std;

typedef unsigned int u32;

static const int MAXN = 100005;
static const int MAXE = 200005;

int n, m, k;
u32 MASK;

/* ---------- 邻接表（链式前向星） ---------- */
int headArr[MAXN], eTo[MAXE], eNxt[MAXE], ecnt;
static inline void addEdge(int u, int v) {
    eTo[++ecnt] = v; eNxt[ecnt] = headArr[u]; headArr[u] = ecnt;
}

/* ---------- 树链剖分 ---------- */
int parent_[MAXN], depth_[MAXN], sz[MAXN], heavy[MAXN], top[MAXN], dfn[MAXN], rev[MAXN];
int order_[MAXN];

/* ---------- 区间变换：(A,B) = (F(0^k), F(1^k)) ---------- */
struct Seg { u32 A, B; };

static inline Seg comp(const Seg &after, const Seg &before) {
    // (after ∘ before)
    Seg r;
    r.A = ((before.A & after.B) | (~before.A & after.A)) & MASK;
    r.B = ((before.B & after.B) | (~before.B & after.A)) & MASK;
    return r;
}

Seg fwd[MAXN << 2], bwd[MAXN << 2];   // 正向（dfn 递增）/ 反向（dfn 递减）
u32 wv[MAXN];                         // 点权

static inline Seg leafSeg(u32 w) {
    Seg r; r.A = MASK; r.B = (~w) & MASK; return r;   // F(x) = ~(x & w)
}

static void build(int node, int l, int r) {
    if (l == r) { fwd[node] = bwd[node] = leafSeg(wv[rev[l]]); return; }
    int mid = (l + r) >> 1;
    build(node << 1, l, mid);
    build(node << 1 | 1, mid + 1, r);
    fwd[node] = comp(fwd[node << 1 | 1], fwd[node << 1]);
    bwd[node] = comp(bwd[node << 1], bwd[node << 1 | 1]);
}

static void update(int node, int l, int r, int pos, u32 w) {
    if (l == r) { fwd[node] = bwd[node] = leafSeg(w); return; }
    int mid = (l + r) >> 1;
    if (pos <= mid) update(node << 1, l, mid, pos, w);
    else update(node << 1 | 1, mid + 1, r, pos, w);
    fwd[node] = comp(fwd[node << 1 | 1], fwd[node << 1]);
    bwd[node] = comp(bwd[node << 1], bwd[node << 1 | 1]);
}

Seg acc;

// 正向查询：按 dfn 递增顺序复合（自上而下）
static void queryF(int node, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) { acc = comp(fwd[node], acc); return; }
    int mid = (l + r) >> 1;
    if (ql <= mid) queryF(node << 1, l, mid, ql, qr);
    if (qr > mid) queryF(node << 1 | 1, mid + 1, r, ql, qr);
}

// 反向查询：按 dfn 递减顺序复合（自下而上）
static void queryB(int node, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) { acc = comp(bwd[node], acc); return; }
    int mid = (l + r) >> 1;
    if (qr > mid) queryB(node << 1 | 1, mid + 1, r, ql, qr);
    if (ql <= mid) queryB(node << 1, l, mid, ql, qr);
}

static int lcaOf(int x, int y) {
    while (top[x] != top[y])
        if (depth_[top[x]] >= depth_[top[y]]) x = parent_[top[x]];
        else y = parent_[top[y]];
    return depth_[x] < depth_[y] ? x : y;
}

static u32 Query(int x, int y) {
    int l = lcaOf(x, y);
    Seg ID; ID.A = 0; ID.B = MASK;          // 恒等函数
    Seg fx = ID, fy = ID;

    // x 侧：x 向上到 l（含 l），方向自下而上
    while (top[x] != top[l]) {
        acc = fx; queryB(1, 1, n, dfn[top[x]], dfn[x]); fx = acc;
        x = parent_[top[x]];
    }
    acc = fx; queryB(1, 1, n, dfn[l], dfn[x]); fx = acc;

    // y 侧：l（不含）向下到 y，方向自上而下
    while (top[y] != top[l]) {
        acc = ID; queryF(1, 1, n, dfn[top[y]], dfn[y]); fy = comp(fy, acc);
        y = parent_[top[y]];
    }
    if (y != l) { acc = ID; queryF(1, 1, n, dfn[l] + 1, dfn[y]); fy = comp(fy, acc); }

    Seg total = comp(fy, fx);               // 先走 x 侧，再走 y 侧
    return total.A;                         // = F(0^k) = f(L)
}

int main() {
    if (scanf("%d %d %d", &n, &m, &k) != 3) return 0;
    MASK = (k >= 32) ? 0xFFFFFFFFu : ((1u << k) - 1u);

    for (int i = 1; i <= n; ++i) {
        unsigned long long t;
        scanf("%llu", &t);
        wv[i] = (u32)t;
    }
    for (int i = 1; i < n; ++i) {
        int a, b; scanf("%d %d", &a, &b);
        addEdge(a, b); addEdge(b, a);
    }

    /* --- 迭代式树链剖分（避免链状数据递归爆栈） --- */
    int qh = 0, qt = 0;
    parent_[1] = 0; depth_[1] = 0; order_[qt++] = 1;
    while (qh < qt) {
        int u = order_[qh++];
        for (int e = headArr[u]; e; e = eNxt[e]) {
            int v = eTo[e];
            if (v == parent_[u]) continue;
            parent_[v] = u; depth_[v] = depth_[u] + 1;
            order_[qt++] = v;
        }
    }
    for (int i = n - 1; i >= 0; --i) {
        int u = order_[i];
        sz[u] = 1; heavy[u] = 0;
        for (int e = headArr[u]; e; e = eNxt[e]) {
            int v = eTo[e];
            if (v == parent_[u]) continue;
            sz[u] += sz[v];
            if (heavy[u] == 0 || sz[v] > sz[heavy[u]]) heavy[u] = v;
        }
    }
    {
        int cur = 0;
        static int stkU[MAXN], stkT[MAXN];
        int sp = 0;
        stkU[sp] = 1; stkT[sp] = 1; ++sp;
        while (sp) {
            --sp;
            int u = stkU[sp], t = stkT[sp];
            for (int x = u; x; x = heavy[x]) {
                top[x] = t; dfn[x] = ++cur; rev[cur] = x;
                for (int e = headArr[x]; e; e = eNxt[e]) {
                    int v = eTo[e];
                    if (v != parent_[x] && v != heavy[x]) { stkU[sp] = v; stkT[sp] = v; ++sp; }
                }
            }
        }
    }

    build(1, 1, n);

    char op[16];
    while (m--) {
        int x; unsigned long long y;
        scanf("%15s %d %llu", op, &x, &y);
        if (op[0] == 'Q') printf("%u\n", Query(x, (int)y));
        else update(1, 1, n, dfn[x], (u32)y);
    }
    return 0;
}
