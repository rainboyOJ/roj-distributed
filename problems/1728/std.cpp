// std.cpp — 一本通 1728《构造序列》
// 等价经典题：洛谷 P3588 [POI2015] Pustynia（BZOJ 4383）
//
// 思路来源（拓扑排序 + 线段树优化建图）：
//   https://www.cnblogs.com/VisJiao/p/LgP3588.html      （洛谷 P3588 题解转载，主参考）
//   https://blog.csdn.net/tc1129/article/details/102121573（同型题解，交叉印证）
//   题面依据：.ybt-import/staging/1728/content.md
//
// 建模：边 (u,v,w) 表示 val[v] >= val[u] + w。
//   - 线段树上 儿子 -> 父亲 权 0（父亲(区间 max 下界) >= 儿子）
//   - 每条信息新建条件点 p（含义 min{x_1..x_k}）：每个“剩下的位置”所在区间节点 -> p 权 1
//     （min{x} > max{其余}），p -> x_i 权 0（x_i >= min{x}）。
//   - 已知位置叶子初值直接置 d（相当于以 d 为下界 ⇒ 弹出时 val==d 才算合法）；
//     其余入度 0 的点取下界 1。拓扑排序递推 val[v] = max(val[v], val[u]+w)。
//   - 无解判定：① 存在环（拓扑排序后仍有入度 > 0 的点）；
//     ② 某点下界 > 1e9（值域上界，题面坑点）；③ 已知位置叶子下界 > 给定值 d。
//     三条与公开题解一致（已用参考实现交叉核对，见 gen-report.md）。
//
// 与参考实现（上面两个 URL）的差异仅为实现方式，非语义：
//   1) 线段树用迭代式 1..2sz-1 数组（参考用递归式左右儿子数组），免去递归与指针开销；
//   2) 邻接表把边权（只有 0/1）压进 next 下标最低位，nxt[i] = (下一条 << 1) | w：
//      省去 pair 与第二组数组，最坏数据下常驻内存从参考实现实测 88MB 降到 66MB（限 128MB）；
//   3) 读入用 1MB fread 缓冲；输出用 4MB 缓冲一次性写出。
// 任意满足条件的一组解均可（题面允许多解）。输出：无解 "NIE"，否则 "TAK" + n 个正整数。
//
// 编译：g++ -O2 -std=c++17 std.cpp -o std

#include <cstdio>
#include <vector>

using namespace std;

static const int MAXV = 1000000000;

// ---------- 快速读入 ----------
static char ibuf[1 << 20];
static size_t ipos = 0, ilen = 0;
static inline int gc() {
    if (ipos == ilen) {
        ilen = fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen == 0) return -1;
    }
    return (unsigned char)ibuf[ipos++];
}
static inline int rd() {
    int c = gc();
    while (c < '0' || c > '9') c = gc();
    int x = 0;
    while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = gc(); }
    return x;
}

int main() {
    int n = rd(), s = rd(), m = rd();

    int sz = 1;
    while (sz < n) sz <<= 1;                 // 线段树：叶子 = sz + (i-1)，节点 1..2sz-1
    int segN = 2 * sz;                       // 线段树节点编号 1..2sz-1
    int V = segN + m;                        // 条件点编号 segN + q (q 从 0 起)

    vector<int> known(V + 1, 0);             // 已知值（只对叶子有效）
    for (int i = 0; i < s; i++) {
        int p = rd(), d = rd();
        known[sz + p - 1] = d;
    }

    // 先读入全部信息（l,r,k 与 k 个 x），便于精确统计边数
    vector<int> ql(m), qr(m), qxs;           // 扁平存 x，配 qoff
    vector<int> qoff(m + 1, 0);
    for (int q = 0; q < m; q++) {
        ql[q] = rd(); qr[q] = rd();
        int k = rd();
        qoff[q] = (int)qxs.size();
        qxs.resize(qxs.size() + k);
        for (int j = 0; j < k; j++) qxs[qoff[q] + j] = rd();
    }
    qoff[m] = (int)qxs.size();

    // 统计边数：儿子->父亲 2*sz-2 条；p->x 共 Σk 条；区间->p 用线段树分解
    long long cnt = 0;
    cnt += 2LL * sz - 2;                     // i=2..2sz-1 每个点向父亲
    cnt += qxs.size();                       // p -> x_i (权 0)
    auto count_range = [&](int l, int r) {   // [l,r] 1-indexed 闭区间分解成线段树节点
        if (l > r) return;
        int lo = l - 1 + sz, hi = r - 1 + sz + 1;
        while (lo < hi) {
            if (lo & 1) { cnt++; lo++; }
            if (hi & 1) { hi--; cnt++; }
            lo >>= 1; hi >>= 1;
        }
    };
    for (int q = 0; q < m; q++) {
        int prev = ql[q];
        for (int j = qoff[q]; j < qoff[q + 1]; j++) {
            count_range(prev, qxs[j] - 1);   // 剩下的位置：x_j 之前的空隙
            prev = qxs[j] + 1;
        }
        count_range(prev, qr[q]);            // 最后一个空隙
    }

    // 紧凑邻接表：head[u] 为第一条边下标，nxt[i] = (下一条 << 1) | 权值(0/1)
    vector<int> head(V + 1, -1), to, nxt;
    to.reserve((size_t)cnt);
    nxt.reserve((size_t)cnt);
    vector<int> indeg(V + 1, 0);
    auto add = [&](int u, int v, int w) {
        nxt.push_back((head[u] << 1) | w);
        to.push_back(v);
        head[u] = (int)to.size() - 1;
        indeg[v]++;
    };

    for (int i = 2; i < segN; i++) add(i, i >> 1, 0);   // 儿子 -> 父亲，权 0（区间 max）

    for (int q = 0; q < m; q++) {
        int p = segN + q;                                // 条件点：min{x}
        int prev = ql[q];
        for (int j = qoff[q]; j < qoff[q + 1]; j++) {
            int x = qxs[j];
            if (prev <= x - 1) {                         // 空隙区间 -> p，权 1
                int l = prev, r = x - 1;
                int lo = l - 1 + sz, hi = r - 1 + sz + 1;
                while (lo < hi) {
                    if (lo & 1) { add(lo, p, 1); lo++; }
                    if (hi & 1) { hi--; add(hi, p, 1); }
                    lo >>= 1; hi >>= 1;
                }
            }
            add(p, sz + x - 1, 0);                       // p -> x，权 0
            prev = x + 1;
        }
        int l = prev, r = qr[q];
        if (l <= r) {                                    // 末尾空隙
            int lo = l - 1 + sz, hi = r - 1 + sz + 1;
            while (lo < hi) {
                if (lo & 1) { add(lo, p, 1); lo++; }
                if (hi & 1) { hi--; add(hi, p, 1); }
                lo >>= 1; hi >>= 1;
            }
        }
    }

    // 拓扑排序：val 为“下界”，已知位置以 d 为下界初值（精确值）
    vector<int> val(V + 1, 0), que;
    que.reserve(V);
    for (int i = 1; i <= n; i++) {
        int leaf = sz + i - 1;
        if (known[leaf]) val[leaf] = known[leaf];
    }
    for (int u = 1; u <= V; u++)
        if (indeg[u] == 0) {
            if (val[u] < 1) val[u] = 1;
            que.push_back(u);
        }

    bool bad = false;
    for (size_t qi = 0; qi < que.size() && !bad; qi++) {
        int u = que[qi];
        if (val[u] > MAXV) bad = true;                   // 超过值域上界 -> 无解
        else if (known[u] && val[u] > known[u]) bad = true;   // 下界超过给定的精确值 -> 无解
        if (bad) break;
        for (int e = head[u]; e != -1; e = nxt[e] >> 1) {
            int v = to[e], w = nxt[e] & 1;
            if (val[v] < val[u] + w) val[v] = val[u] + w;
            if (--indeg[v] == 0) que.push_back(v);
        }
    }
    if (!bad)
        for (int u = 1; u <= V; u++)
            if (indeg[u] > 0) { bad = true; break; }      // 成环 -> 无解

    // 输出
    if (bad) { puts("NIE"); return 0; }
    for (int i = 1; i <= n && !bad; i++) {
        int v = val[sz + i - 1];
        if (v < 1 || v > MAXV) bad = true;
    }
    if (bad) { puts("NIE"); return 0; }
    puts("TAK");
    {
        static char obuf[1 << 22];
        int op = 0;
        auto wnum = [&](int x) {
            char tmp[12]; int t = 0;
            if (x == 0) tmp[t++] = '0';
            while (x > 0) { tmp[t++] = char('0' + x % 10); x /= 10; }
            while (t) obuf[op++] = tmp[--t];
        };
        for (int i = 1; i <= n; i++) {
            wnum(val[sz + i - 1]);
            obuf[op++] = (i == n ? '\n' : ' ');
        }
        fwrite(obuf, 1, op, stdout);
    }
    return 0;
}
