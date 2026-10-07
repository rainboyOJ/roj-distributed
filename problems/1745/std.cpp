// 一本通 1745《分组》标程
// 参考来源 URL（题面同源原题 JZOJ 3854 / Codeforces 173E "Camping Groups" 的题解）:
//   https://blog.csdn.net/inferior_hjx/article/details/133385349
//   https://blog.csdn.net/chunkitlau/article/details/54576990
//   （题面特征句「小组中必须要有一个队长」「队长的地位应该是最高的」检索命中上述同题博客）
//
// 算法（排序 + BIT 计数 + 询问离线 + 权值线段树，年龄离散化）：
//   1) 小组条件改写：
//      a. 队长 r 值必须是全组最大（可并列）=> 组内所有成员 r <= r_队长；
//      b. 组内其他成员与队长年龄差 <= K（队长本人显然满足）。
//      因此「以 i 当队长」时小组最大人数
//        cnt[i] = #{ j : r_j <= r_i 且 |a_j - a_i| <= K }（含 i 自己）。
//      按 r 升序排序后，同 r 的一组先整体插入 BIT（下标为年龄），再统一查询
//      [a_i-K, a_i+K]，保证 r 相同的人互相计入。
//   2) 询问 (x, y) 离线：
//      队长必须同时满足 r_leader >= need = max(r_x, r_y)，
//      以及 a_leader ∈ [max(a_x,a_y)-K, min(a_x,a_y)+K]（两条年龄约束的交）。
//      把询问按「need 对应的最小排名 start」降序排序，指针把 rank >= start 的
//      人的 cnt 插入以年龄为下标的最大值线段树，区间查最大值即可。
//      答案 < 2 说明无法同组（x,y 自身一定被 cnt 计入，故 <2 即无解），输出 -1。
//   3) 年龄值域 1..1e9 离散化到 <= n 个坐标，复杂度 O((n + Q) log n)。
//
// 与博客原码的差异：博客对 r_x == r_y 的询问直接用排序后较大的 rank 作阈值，
// 会漏掉同 r 组内排名更小的人（地位并列同样可当队长）；本版用
// std::lower_bound 取「r >= need 的第一个排名」作阈值，覆盖并列情况。
#include <cstdio>
#include <algorithm>
using namespace std;

// 题面上限 n,Q <= 1e5，按 ×2 安全系数开数组（STATIC 用于下标数组，QSN 独立）
const int MAXN = 200005;   // n 数组：2 倍题面上限
const int MAXQ = 200005;   // 询问数组：2 倍题面上限

int n, K, Q;

struct Person {
    int r, a, id;
} p[MAXN];
bool cmpPerson(const Person &x, const Person &y) { return x.r < y.r; }

int rOfId[MAXN], aOfId[MAXN];   // 原编号 -> r / a
int sortedR[MAXN];              // 按 r 升序的 r 序列（1-indexed）
int ageVal[MAXN], m;            // 离散化年龄集合（1-indexed），m = 去重后个数
int ageRank[MAXN];              // 排序后第 i 个人的年龄坐标（1..m）
int cnt[MAXN];                  // cnt[i]: 以排序后第 i 个人为队长的小组最大人数

int fen[MAXN];                  // BIT：计数
void fenAdd(int i, int v) { for (; i <= m; i += i & -i) fen[i] += v; }
int fenSum(int i) { int s = 0; for (; i > 0; i -= i & -i) s += fen[i]; return s; }

int seg[4 * MAXN];  // 最大值线段树（年龄坐标）；4*2e5 = 8e5 int ≈ 3.2MB
void segUpd(int o, int l, int r, int pos, int val) {
    if (l == r) { if (val > seg[o]) seg[o] = val; return; }
    int mid = (l + r) >> 1;
    if (pos <= mid) segUpd(o << 1, l, mid, pos, val);
    else segUpd(o << 1 | 1, mid + 1, r, pos, val);
    seg[o] = max(seg[o << 1], seg[o << 1 | 1]);
}
int segQry(int o, int l, int r, int ql, int qr) {
    if (ql > r || qr < l) return 0;
    if (ql <= l && r <= qr) return seg[o];
    int mid = (l + r) >> 1;
    return max(segQry(o << 1, l, mid, ql, qr), segQry(o << 1 | 1, mid + 1, r, ql, qr));
}

// 第一个 >= v 的年龄坐标（无则 m+1）
int lowerIdx(int v) {
    int lo = 1, hi = m, res = m + 1;
    while (lo <= hi) {
        int mid = (lo + hi) >> 1;
        if (ageVal[mid] >= v) { res = mid; hi = mid - 1; } else lo = mid + 1;
    }
    return res;
}
// 最后一个 <= v 的年龄坐标（无则 0）
int upperIdx(int v) {
    int lo = 1, hi = m, res = 0;
    while (lo <= hi) {
        int mid = (lo + hi) >> 1;
        if (ageVal[mid] <= v) { res = mid; lo = mid + 1; } else hi = mid - 1;
    }
    return res;
}

struct Query {
    int start;  // 队长最小排名（r >= need 的第一个排名）
    int ql, qr; // 队长年龄区间（离散化坐标）
    int id;
} qs[MAXQ];
bool cmpQuery(const Query &x, const Query &y) { return x.start > y.start; }
int ans[MAXQ];

int main() {
    if (scanf("%d%d", &n, &K) != 2) return 0;
    for (int i = 1; i <= n; ++i) { scanf("%d", &p[i].r); p[i].id = i; }
    for (int i = 1; i <= n; ++i) scanf("%d", &p[i].a);
    for (int i = 1; i <= n; ++i) { rOfId[i] = p[i].r; aOfId[i] = p[i].a; }

    sort(p + 1, p + n + 1, cmpPerson);
    for (int i = 1; i <= n; ++i) { sortedR[i] = p[i].r; ageVal[i] = p[i].a; }
    sort(ageVal + 1, ageVal + n + 1);
    m = (int)(unique(ageVal + 1, ageVal + n + 1) - ageVal - 1);
    for (int i = 1; i <= n; ++i) ageRank[i] = lowerIdx(p[i].a);

    // 预处理 cnt[i]
    for (int i = 1; i <= n; ) {
        int j = i;
        while (j <= n && p[j].r == p[i].r) { fenAdd(ageRank[j], 1); ++j; }
        for (int t = i; t < j; ++t) {
            int l = lowerIdx(p[t].a - K), rr = upperIdx(p[t].a + K);
            cnt[t] = (l > rr) ? 0 : fenSum(rr) - fenSum(l - 1);
        }
        i = j;
    }

    scanf("%d", &Q);
    for (int i = 1; i <= Q; ++i) {
        int x, y;
        scanf("%d%d", &x, &y);
        int need = max(rOfId[x], rOfId[y]);
        int start = (int)(lower_bound(sortedR + 1, sortedR + n + 1, need) - sortedR);
        qs[i].start = start;
        qs[i].ql = lowerIdx(max(aOfId[x], aOfId[y]) - K);
        qs[i].qr = upperIdx(min(aOfId[x], aOfId[y]) + K);
        qs[i].id = i;
    }

    sort(qs + 1, qs + Q + 1, cmpQuery);
    int k = n;
    for (int i = 1; i <= Q; ++i) {
        while (k >= qs[i].start) { segUpd(1, 1, m, ageRank[k], cnt[k]); --k; }
        int v = 0;
        int lo = max(qs[i].ql, 1), hi = min(qs[i].qr, m);
        if (lo <= hi) v = segQry(1, 1, m, lo, hi);
        ans[qs[i].id] = (v < 2) ? -1 : v;
    }

    for (int i = 1; i <= Q; ++i) printf("%d\n", ans[i]);
    return 0;
}
