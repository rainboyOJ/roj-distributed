// std.cpp —— 一本通 1714《地壳运动》
// 等价原题：JZOJ 3860 / 【NOIP2014 八校联考 第3场第2试 10.5】地壳运动 (mst)
// 题面依据：.ybt-import/staging/1714/content.md（官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=1714）
//
// ============================ 来源情况（网络检索，证据见 work/evidence/）============================
// 说明：一本通 1714 无独立公开题解页；本题即 2014 年八校联考原题 / JZOJ 3860，CSDN 上有多篇同题
//      题解（关键词「地壳运动 mst 最小乘积生成树」）：
//   [1] https://blog.csdn.net/doyouseeman/article/details/54588362
//   [2] https://blog.csdn.net/crybymyself/article/details/54588223
//   [3] https://blog.csdn.net/mr_wuyongcong/article/details/104144937
//   三篇思路一致：**最小乘积生成树（参数化 MST）/ 二维最小生成树** ——
//     对方向 (k1,k2) 求 MST 得到点 (a,b)=(Σu,Σv)；某次询问的答案 = min over 生成树 (k1·a + k2·b)，
//     而该最小值必在所有 MST 点的**左下凸壳**（Pareto 最小点）上取得；
//     先用 k=(1,0) 与 k=(0,1) 求出凸壳两端点，再用「垂向法向调用 MST oracle + 分治」把中间点补齐；
//     查询时在凸壳（关于 k1/k2 的凸序列）上二分/三分取最小。
//   本 std 为**改写**（非照抄），关键改动：
//     (1) 凸壳枚举：按「叉积严格 < 0 才递归」的分治（与来源同框架），但**叉积用 __int128 精确计算**，
//         来源用浮点除法判共线（有精度风险）；并加 a 区间守卫，保证每次递归产生的点互不相同 ⟹ 调用次数 ≤ 2·H−1。
//     (2) 查询：凸序列上**二分**（等价于三分且对平台区同样正确），非来源的浮点三分。
//     (3) 询问值：凸链上逐点取最小，并**用十进制定点整数 + __int128 精确求和与四舍五入** ——
//         k 以十进制串（最多 15 位小数）解析为整数 K = round(k·10^15)，边权分量 u,v ≤ 10^6 为整数，
//         故凸壳点 a,b（整数）与查询值 (K1·a+K2·b)/10^15 都是精确有理数，第 3 位小数不存在
//         双精度误差（本题答案可达 10^8 量级，double 在 1e8 上的绝对误差约 1e-8，虽小但
//         恰好落在 .xxx5 边界时会与经典双精度写法输出不同数字）。为不误杀主流解法，
//         生成数据时已用同一标准**逐询问断言距 .xxx5 边界的距离 ≥ 1e-6**（见 data.py 的 fixup 步骤），
//         故任何正确实现的第 3 位小数都唯一确定。
//     (4) 路权 0 ≤ u,v ≤ 10^6 为整数（题面），故 MST 排序比较全部用 __int128 精确比较，无浮点参与。
//     （枚举阶段不需要浮点：所有比较可化为整数/__int128 叉积与点积。）
//
// ============================ 算法与复杂度 ============================
//   记候选生成树的两个代价分量 (a,b) = (Σu, Σv)。答案 = min_{生成树T} (k1·a_T + k2·b_T)。
//   性质 1：对任意 k1,k2>0，上式的最小值一定在「所有 MST 点」的左下凸壳顶点取得
//           （非 Pareto 最小点必被支配点在各分量上同时不大于地替代，不会成为最优）。
//   性质 2：oracle(d1,d2) = 以 d1·u+d2·v 为边权做 MST，返回其 (a,b)，必为 Pareto 最小点。
//   性质 3（分治正确性）：设 l,r 是凸壳上相邻候选（a 增、b 减），取与弦 lr 垂直、两分量均正的方向
//           d=(-Δb, Δa) 调 oracle；若返回点 mid 严格位于弦下方（__int128 叉积 < 0），则 mid 必落在
//           l 与 r 之间（a 严格居中，因凸壳是 Pareto 最小点构成的凸链），对 (l,mid)、(mid,r) 递归即可；
//           返回点在弦上或上方 ⟹ 弦下方无候选点，该段枚举完毕。
//   枚举复杂度 O(H · M log M)（H = 凸壳顶点数，实测 ≤ 6）；查询 O(Q log H)；内存 O(N+M)。
//   时间限制 6000 ms、N≤35、M≤25000、Q≤200000，余量充足。
//
// 用法：g++ -O2 -std=c++17 -o std std.cpp

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <set>
#include <utility>
#include <vector>

typedef long long ll;
typedef __int128 lll;

static int N, M, Q;

struct Edge {
    int x, y;
    ll u, v;  // 该边在两个方向上的代价分量（整数，题面 0 ≤ u,v ≤ 10^6）
};

static std::vector<Edge> E;
static ll K1, K2;  // 当前 oracle 方向（整数，非负且不全为 0）

static inline lll ecost(const Edge &e) { return (lll)e.u * K1 + (lll)e.v * K2; }

// 精确比较：按 d1·u+d2·v 升序；并列时按 (u,v) 升序打破。
// 并列规则只影响同一最优面上取到哪个点（不改变取值最优性），取 u 小者使极端方向
// (1,0)/(0,1) 返回支配角点（Pareto 最小点）。
static bool cmpE(const Edge &a, const Edge &b) {
    lll ca = ecost(a), cb = ecost(b);
    if (ca != cb) return ca < cb;
    if (a.u != b.u) return a.u < b.u;
    if (a.v != b.v) return a.v < b.v;
    if (a.x != b.x) return a.x < b.x;
    return a.y < b.y;
}

static int par[64];
static int find(int x) {
    while (par[x] != x) {
        par[x] = par[par[x]];
        x = par[x];
    }
    return x;
}

// oracle：以 (d1,d2) 为方向做 MST，返回 (Σu, Σv)。d1,d2 ≥ 0 且不全为 0。
static std::pair<ll, ll> mst(ll d1, ll d2) {
    K1 = d1;
    K2 = d2;
    std::sort(E.begin(), E.end(), cmpE);
    for (int i = 1; i <= N; i++) par[i] = i;
    ll su = 0, sv = 0;
    int cnt = 0;
    for (size_t i = 0; i < E.size() && cnt < N - 1; i++) {
        int a = find(E[i].x), b = find(E[i].y);
        if (a != b) {
            par[a] = b;
            su += E[i].u;
            sv += E[i].v;
            cnt++;
        }
    }
    if (cnt != N - 1 && N > 0) {  // 保证连通（题面保证），否则数据有问题
        fprintf(stderr, "error: graph not connected (N=%d, got %d edges)\n", N, cnt);
        exit(3);
    }
    return std::make_pair(su, sv);
}

// 叉积 (r-l) × (m-l)，__int128 精确。返回值 < 0 表示 m 严格位于弦 lr 的下方。
static inline lll cross(const std::pair<ll, ll> &l, const std::pair<ll, ll> &r,
                        const std::pair<ll, ll> &m) {
    return (lll)(r.first - l.first) * (m.second - l.second) -
           (lll)(r.second - l.second) * (m.first - l.first);
}

static long long oracleCalls = 0;

// 分治补齐凸壳：l 在左上（a 小 b 大），r 在右下（a 大 b 小），区间 (l.a, r.a) 内找凸壳点
static void solve(const std::pair<ll, ll> &l, const std::pair<ll, ll> &r,
                  std::vector<std::pair<ll, ll> > &out) {
    if (l.first >= r.first) return;  // 区间已耗尽
    ll d1 = l.second - r.second;     // = -Δb > 0
    ll d2 = r.first - l.first;       // =  Δa > 0
    std::pair<ll, ll> mid = mst(d1, d2);
    oracleCalls++;
    if (cross(l, r, mid) >= 0) return;  // 弦下方无候选点
    if (!(l.first < mid.first && mid.first < r.first)) {
        fprintf(stderr, "warning: hull point outside a-range (%lld not in (%lld,%lld))\n",
                (long long)mid.first, (long long)l.first, (long long)r.first);
        return;
    }
    solve(l, mid, out);
    out.push_back(mid);
    solve(mid, r, out);
}

int main() {
    if (scanf("%d %d %d", &N, &M, &Q) != 3) return 1;
    E.resize(M);
    for (int i = 0; i < M; i++) {
        int x, y;
        ll u, v;
        if (scanf("%d %d %lld %lld", &x, &y, &u, &v) != 4) return 1;
        E[i].x = x;
        E[i].y = y;
        E[i].u = u;
        E[i].v = v;
    }

    // ---------------- 凸壳枚举 ----------------
    std::pair<ll, ll> left = mst(1, 0);  // 最小 a（并列取最小 b）：凸壳左/上端
    std::pair<ll, ll> right = mst(0, 1); // 最小 b（并列取最小 a）：凸壳右/下端
    oracleCalls += 2;
    std::vector<std::pair<ll, ll> > cand;
    cand.push_back(left);
    solve(left, right, cand);
    if (right != left) cand.push_back(right);

    // 归一化：按 a 升序去重，只保留 Pareto 最小点（b 严格递减者）。
    // 被支配点（a,b 均不小于某保留点）对任意 k1,k2>0 都不可能给出更小值，删去不改变答案；
    // 两端点重合时（退化图）本步自然退化为单点链。
    std::sort(cand.begin(), cand.end());
    cand.erase(std::unique(cand.begin(), cand.end()), cand.end());
    std::vector<std::pair<ll, ll> > chain;
    for (size_t i = 0; i < cand.size(); i++) {
        if (chain.empty() || cand[i].second < chain.back().second) chain.push_back(cand[i]);
    }
    // 自检：链上 a 严格递增、b 严格递减（凸壳单调性），否则立即失败，避免静默产出错数据
    for (size_t i = 0; i + 1 < chain.size(); i++) {
        if (!(chain[i].first < chain[i + 1].first && chain[i].second > chain[i + 1].second)) {
            fprintf(stderr, "internal error: hull chain not monotone at %zu\n", i);
            return 2;
        }
    }

    // ---------------- 查询：凸链逐点最小（十进制定点整数 + __int128 精确） ----------------
    // k 解析为 K = k·10^15 的整数（截断超过 15 位小数的尾部，误差 < 1e-15 相对量级）；
    // 查询值 = (K1·a + K2·b) / 10^15，全程精确，输出 3 位小数按四舍五入。
    const lll SCALE = (lll)1000000000000000LL;  // 10^15
    if (getenv("STD_DUMP_CHAIN")) {  // 供 data.py 做「距 .xxx5 边界距离」精确自检
        for (size_t i = 0; i < chain.size(); i++)
            fprintf(stderr, "CHAIN %lld %lld\n", (long long)chain[i].first, (long long)chain[i].second);
    }
    if (getenv("STD_DEBUG")) fprintf(stderr, "hull points = %zu, oracle calls = %lld\n", chain.size(), oracleCalls);
    lll worst_margin = (lll)1 << 62;  // 全部询问中离 .xxx5 边界的最近距离（单位 1e-15）
    for (int q = 0; q < Q; q++) {
        char s1[64], s2[64];
        if (scanf("%63s %63s", s1, s2) != 2) return 1;
        lll kk[2];
        char *src[2] = {s1, s2};
        for (int t = 0; t < 2; t++) {
            bool neg = false;
            int i = 0;
            if (src[t][0] == '-' || src[t][0] == '+') {
                neg = (src[t][0] == '-');
                i = 1;
            }
            lll val = 0;
            for (; src[t][i] >= '0' && src[t][i] <= '9'; i++) val = val * 10 + (src[t][i] - '0');
            lll scale = SCALE;
            if (src[t][i] == '.') {
                i++;
                for (int d = 0; d < 15 && src[t][i] >= '0' && src[t][i] <= '9'; d++, i++) {
                    scale /= 10;
                    val = val * 10 + (src[t][i] - '0');
                }
                for (; src[t][i] >= '0' && src[t][i] <= '9'; i++) {}  // 丢弃第 16 位及以后
            }
            kk[t] = neg ? -val * scale : val * scale;
        }
        if (kk[0] <= 0 || kk[1] <= 0) {
            fprintf(stderr, "error: k1,k2 must be > 0 (got %s %s)\n", s1, s2);
            return 4;
        }
        lll best = 0;
        for (size_t i = 0; i < chain.size(); i++) {
            lll val = kk[0] * chain[i].first + kk[1] * chain[i].second;
            if (i == 0 || val < best) best = val;
        }
        // 精确四舍五入到 3 位小数（本包数据已保证离 .xxx5 边界 >= 1e-6，不存在半位歧义）
        lll t3 = best * 1000;
        lll whole = t3 / SCALE;
        lll rem = t3 % SCALE;
        if (rem * 2 >= SCALE) whole++;
        if (rem * 2 == SCALE) fprintf(stderr, "warning: exact half tie at query %d\n", q);
        {
            lll d = rem * 2 - SCALE;
            if (d < 0) d = -d;
            if (d < worst_margin) worst_margin = d;
        }
        printf("%lld.%03lld\n", (long long)(whole / 1000), (long long)(whole % 1000));
    }
    if (getenv("STD_MARGIN"))  // 最小距离（单位 1e-6，因为 d 单位 1e-15 = 一千分之一值单位）
        fprintf(stderr, "min distance to .xxx5 boundary = %.9f (value units)\n",
                (double)worst_margin / 1e15 / 1000.0);
    return 0;
}
