// 一本通 1713《生成树》标程（信息学奥赛一本通 · 高手训练篇 · 三、图论）
//
// ── 来源情况（2024 检索结论）──
//   按任务书建议关键词在 CSDN 站内搜索与通用搜索引擎检索：
//     · 「一本通 1713 题解」        → 无本题解法（仅 PCI-1713 硬件文档等无关结果）
//     · 「一本通 1713 生成树」      → 仅命中题解目录
//       https://blog.csdn.net/qq_36230375/article/details/136483654
//       （目录中列有「1713 生成树」条目，但该文中无对应题解正文/代码）
//     · 「1713：生成树」「信息学奥赛一本通 生成树 参考代码」
//       「生成树边权最大公约数 最小公倍数」→ 均无本题公开题解或 AC 代码
//   结论：本题暂无公开题解可直接改写，故按题面自研实现（思路见下），
//   并用暴力枚举全部生成树的对拍程序 work/brute.cpp 验证正确性（work/stress.py）。
//
// ── 题意 ──
//   N 个点 M 条边的无向图，对每一棵生成树求其边权的 gcd，
//   再对所有生成树的 gcd 求 lcm，输出该 lcm。
//
// ── 关键结论 ──
//   记 D = { d ≥ 1 : 只保留权值能被 d 整除的边后，图连通 }，则 ans = lcm(D)。
//   证明：
//     (⊆) 任取生成树 T，令 g = gcd(T)。由 gcd 定义 g | w(e) 对 T 的每条边成立，
//         故 T ⊆ G_g，G_g 连通，即 g ∈ D；于是 lcm_{T} gcd(T) | lcm(D)。
//     (⊇) 设 d ∈ D。G_d 连通，取其生成树 T，则 d | gcd(T)，故 d | lcm_{T} gcd(T)。
//         对所有 d ∈ D 取 lcm 得 lcm(D) | lcm_{T} gcd(T)。
//   两向合并：ans = lcm(D)。
//   （该结论与「矩阵树定理 + 莫比乌斯反演」类题目的 gcd/lcm 格结构同源，
//     此处按本题只需连通性判定，无需计数。）
//
// ── 算法与复杂度 ──
//   d 从 1 枚举到 maxW(≤ 32767)，并查集判断 G_d 是否连通，若连通则 ans = lcm(ans, d)。
//   把边按权值分桶（排序 + 前缀定位），判定 d 时只需遍历权值为 d 倍数的桶，
//   总并查集操作 Σ_e τ(w_e)（τ 为约数个数，平均约 10），加上每轮 O(N) 的 DSU 重置，
//   约 3.3e7 次基本操作，远小于 1s。
//   答案用 unsigned long long：题面保证 ans ≤ 2^64-1；按 d 递增累乘时每个中间 lcm
//   都整除最终答案，故不会中途溢出。
//
// 编译：g++ -O2 -std=c++17 std.cpp -o std

#include <cstdio>
#include <cstring>
#include <algorithm>
#include <vector>

using namespace std;

typedef unsigned long long ull;

// ---------- 快速读入 ----------
static const int BUFSZ = 1 << 20;
static char ibuf[BUFSZ];
static int ipos = 0, ilen = 0;

static inline int getch() {
    if (ipos == ilen) {
        ilen = (int)fread(ibuf, 1, BUFSZ, stdin);
        ipos = 0;
        if (ilen <= 0) return -1;
    }
    return (unsigned char)ibuf[ipos++];
}

static inline int readInt() {
    int c = getch();
    while (c != -1 && (c < '0' || c > '9')) c = getch();
    int x = 0;
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = getch();
    }
    return x;
}

// ---------- 并查集（按大小合并 + 路径减半） ----------
static int par[1024], sz[1024];

static inline void dsu_init(int n) {
    for (int i = 1; i <= n; ++i) { par[i] = i; sz[i] = 1; }
}

static inline int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}

static inline bool unite(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return false;
    if (sz[a] < sz[b]) swap(a, b);
    par[b] = a; sz[a] += sz[b];
    return true;
}

static inline ull gcd_ull(ull a, ull b) {
    while (b) { ull t = a % b; a = b; b = t; }
    return a;
}

static inline ull lcm_ull(ull a, ull b) {   // b 整除最终答案，故 a/gcd*b 不溢出
    return a / gcd_ull(a, b) * b;
}

int main() {
    int n = readInt();
    int m = readInt();

    struct RawEdge { int u, v, w; };
    vector<RawEdge> es;
    es.reserve(m > 0 ? m : 1);
    int maxW = 0;
    for (int i = 0; i < m; ++i) {
        int u = readInt(), v = readInt(), w = readInt();
        es.push_back(RawEdge{u, v, w});
        if (w > maxW) maxW = w;
    }

    // n = 1：只有唯一的空生成树，约定答案为 1（题面（M=N-1 子任务）允许 M=0）
    if (n <= 1 || m == 0 || maxW == 0) {
        printf("1\n");
        return 0;
    }

    // ---------- 按权值分桶：排序后记录每个权值的起始下标 ----------
    sort(es.begin(), es.end(), [](const RawEdge& a, const RawEdge& b) { return a.w < b.w; });
    vector<int> start(maxW + 2, 0), cnt(maxW + 1, 0);
    for (int i = 0; i < m; ++i) ++cnt[es[i].w];
    for (int w = 1; w <= maxW; ++w) start[w + 1] = start[w] + cnt[w];

    ull ans = 1;
    for (int d = 1; d <= maxW; ++d) {
        // 若 d 的倍数中一条边都没有，G_d 必不连通，快速跳过
        bool any = false;
        for (int k = d; k <= maxW; k += d) {
            if (cnt[k]) { any = true; break; }
        }
        if (!any) continue;

        dsu_init(n);
        int comp = n;
        for (int k = d; k <= maxW && comp > 1; k += d) {
            if (!cnt[k]) continue;
            int lo = start[k], hi = start[k] + cnt[k];
            for (int i = lo; i < hi; ++i) {
                if (unite(es[i].u, es[i].v)) --comp;
            }
        }
        if (comp == 1) ans = lcm_ull(ans, (ull)d);   // G_d 连通 ⇒ d ∈ D
    }

    printf("%llu\n", ans);
    return 0;
}
