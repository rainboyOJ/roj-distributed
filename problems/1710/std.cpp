// 一本通 1710《构造完全图》标程（高手训练 图论）
//
// 题意来源：.ybt-import/staging/1710/content.md
//   给一棵树 T，求 T 能扩展出的边权和最小的完全图 G（即：以 T 为唯一最小生成树的完全图最小边权和）。
//
// 解法来源（公开 AC 代码，与本题目描述/样例完全一致）：
//   1) CSDN 《【并查集】构造完全图》
//      https://blog.csdn.net/weixin_42146061/article/details/97137163
//      （同题：LOJ 10067「一本通 3.1 练习 2」构造完全图 / codevs2796，样例 4 组 1 2 1 / 1 3 1 / 1 4 2 -> 12 完全一致）
//   2) CSDN 《libreoj 10067「一本通 3.1 练习 2」构造完全图 题解》
//      https://blog.csdn.net/lightninguz/article/details/105019741
//   3) CSDN 《走廊泼水节 题解&代码》（同型经典题：走廊泼水节，算法完全相同）
//      https://blog.csdn.net/zhuchangcheng1003/article/details/87978082
//
// 算法（Kruskal 思想 + 并查集，O(n log n)）：
//   把树边按权值从小到大排序，依次合并两个连通块。设两块大小分别为 sx, sy，
//   当前边权 w，则跨两块的所有点对共有 sx*sy 条边：其中 1 条已作为树边（权 w）计入答案，
//   其余 sx*sy-1 条在完全图里必须 >= w+1（否则唯一 MST 会被破坏），且取 w+1 恰好可行
//   （此时该 w 的边仍是唯一最小桥接边 -> T 仍是唯一 MST）。
//   故贡献为 w + (sx*sy - 1) * (w + 1)，合并后 size 相加。
//
//   唯一性论证：每条树边 w 在 Kruskal 序中，其两侧连通块之间的所有非树边权值都 > w
//   （构造取 w+1），因此按 Kruskal 顺序贪心选择时 T 的每条边都严格优于任何可替代边，
//   唯一 MST 成立。
//
// 数据范围（题面）：N <= 100000，1 <= D_i <= 100000。
//   答案量级：最坏约 (n^2/2)*1e5 ≈ 5e14，超 32 位，全程使用 long long。
//
// 本文件为按上述公开题解自行改写的实现：C++17，stdin -> stdout，快速读入。

#include <cstdio>
#include <algorithm>
#include <vector>
#include <numeric>
using namespace std;

namespace fastio {
    static const int BUFSZ = 1 << 20;
    static char ibuf[BUFSZ];
    static int ipos = 0, ilen = 0;

    static inline int gc() {
        if (ipos == ilen) {
            ilen = (int)fread(ibuf, 1, BUFSZ, stdin);
            ipos = 0;
            if (ilen <= 0) return -1;
        }
        return (unsigned char)ibuf[ipos++];
    }

    static inline bool readInt(long long &out) {
        int c = gc();
        while (c != -1 && (c < '0' || c > '9') && c != '-') c = gc();
        if (c == -1) return false;
        bool neg = false;
        if (c == '-') { neg = true; c = gc(); }
        long long x = 0;
        while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
        out = neg ? -x : x;
        return true;
    }
}  // namespace fastio

struct DSU {
    vector<int> fa;
    vector<long long> sz;  // 连通块点数（long long 防乘法前溢出）
    explicit DSU(int n) : fa(n + 1), sz(n + 1, 1) {
        for (int i = 1; i <= n; ++i) fa[i] = i;
    }
    int find(int x) {
        while (fa[x] != x) {
            fa[x] = fa[fa[x]];
            x = fa[x];
        }
        return x;
    }
};

struct Edge {
    int u, v;
    long long w;
    bool operator<(const Edge &o) const { return w < o.w; }
};

int main() {
    long long n;
    if (!fastio::readInt(n)) return 0;

    if (n <= 1) {
        // 退化：单点完全图无任何边，边权和为 0（防御性分支，题面 N>=2 时不会触发）
        printf("0\n");
        return 0;
    }

    vector<Edge> edges((size_t)(n - 1));
    long long sum = 0;
    for (long long i = 0; i < n - 1; ++i) {
        long long u, v, w;
        fastio::readInt(u);
        fastio::readInt(v);
        fastio::readInt(w);
        edges[(size_t)i] = {(int)u, (int)v, w};
        sum += w;  // 树边本身的权值全部计入答案
    }

    sort(edges.begin(), edges.end());

    DSU dsu((int)n);
    for (const Edge &e : edges) {
        int a = dsu.find(e.u), b = dsu.find(e.v);
        if (a == b) continue;  // 输入保证是树，此分支不会命中
        long long sx = dsu.sz[a], sy = dsu.sz[b];
        // 跨集合的 sx*sy 条边中，1 条是树边（已计入 sum），
        // 其余 sx*sy-1 条取 w+1 才能不破坏唯一 MST。
        sum += (sx * sy - 1) * (e.w + 1);
        if (sx < sy) {  // 按大小合并（保持路径压缩效率）
            dsu.fa[a] = b;
            dsu.sz[b] = sx + sy;
        } else {
            dsu.fa[b] = a;
            dsu.sz[a] = sx + sy;
        }
    }

    printf("%lld\n", sum);
    return 0;
}
