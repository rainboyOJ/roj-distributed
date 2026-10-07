// std.cpp  ——  一本通 1755《星际探测》标程
//
// 来源 / 依据：
//   题面特征句「DX3906星系，Melancholy星上，我在勘测这里的地质情况。」精确检索，可判定本题
//   即原题 JZOJ 4237 Melancholy（五校联考 5day1）。
//   公开题解（检索到的 C++ 参考实现）：
//     - https://www.cnblogs.com/mastervan/p/10331709.html          （原始博客）
//     - https://blog.csdn.net/weixin_34192993/article/details/94566345 （CSDN 镜像，含题面+代码）
//     - https://blog.csdn.net/johann_oier/article/details/49280219  （【NOIP or 省选】Melancholy ——线段树+容斥原理）
//   本文件在参考实现思路（线段树维护 1..6 次初等对称和 + 定位最小值位置，两侧分别查询后合并）
//   基础上重写为清晰版本，并逐字用题面样例验证。
//
// 题意：N 个区域，每个有 (D,V)。Q 次询问 [L,R],K：
//   取所有 D∈[L,R] 的区域，去掉其中 V 最小的那一块（V 互不相同，位置唯一），
//   在剩下的区域中「有次序地」选 K 块，评估值 P = 所有选取方案 V 乘积之和
//   = K! * e_K(剩余 V 集合)（e_K 为 K 次初等对称和）。若可选区域不足 K 块，P=0。
//   输出 P mod 2^32。
//
// 算法：按 D 排序后区间连续。
//   - 线段树每个节点维护该段 V 的 e_1..e_6 及区间最小值及其位置。
//   - 合并两段（多项式卷积）：e_i = eL_i + eR_i + Σ_{j=1}^{i-1} eL_j * eR_{i-j}。
//   - 询问：先查区间最小 V 的位置 pos，再分别查 [l,pos-1] 与 [pos+1,r] 的 e 向量并合并，
//     最后乘以 K!。取模 2^32 用 uint32_t 自然溢出。
//   复杂度 O((N + Q log N) * K^2)，K<=6，最大点远小于 2s 限制。
//
// 编译：g++ -O2 -std=c++17 -o std std.cpp

#include <cstdio>
#include <cstdint>
#include <cstring>
#include <algorithm>

using namespace std;

typedef uint32_t u32;

static const int MAXN = 100000 + 10;   // 题面 N 上限 1e5，留安全系数
static const int KMAX = 6;             // 题面 K 上限

static int n, q;

struct Pt { u32 d, v; };
static Pt a[MAXN + 1];

static bool cmpD(const Pt &x, const Pt &y) { return x.d < y.d; }

static u32 seg[MAXN * 4][KMAX + 1];    // e_1..e_6
static u32 mnv[MAXN * 4];              // 区间最小 V
static int mnp[MAXN * 4];              // 区间最小 V 的位置（排序后下标）

static void build(int node, int l, int r) {
    if (l == r) {
        memset(seg[node], 0, sizeof seg[node]);
        seg[node][1] = a[l].v;
        mnv[node] = a[l].v;
        mnp[node] = l;
        return;
    }
    int mid = (l + r) >> 1;
    int L = node << 1, R = L | 1;
    build(L, l, mid);
    build(R, mid + 1, r);

    if (mnv[L] <= mnv[R]) { mnv[node] = mnv[L]; mnp[node] = mnp[L]; }
    else                  { mnv[node] = mnv[R]; mnp[node] = mnp[R]; }

    for (int i = 1; i <= KMAX; i++) {
        u32 s = seg[L][i] + seg[R][i];
        for (int j = 1; j < i; j++) s += seg[L][j] * seg[R][i - j];
        seg[node][i] = s;
    }
}

static u32 qmin;
static int qpos;

static void queryMin(int node, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) {
        if (mnv[node] < qmin) { qmin = mnv[node]; qpos = mnp[node]; }
        return;
    }
    int mid = (l + r) >> 1;
    if (ql <= mid) queryMin(node << 1, l, mid, ql, qr);
    if (mid < qr)  queryMin(node << 1 | 1, mid + 1, r, ql, qr);
}

// 把区间 [ql,qr] 的 e 向量卷积进 acc（acc[0] 隐式为 1）
static void queryPoly(int node, int l, int r, int ql, int qr, u32 acc[KMAX + 1]) {
    if (ql > r || qr < l) return;
    if (ql <= l && r <= qr) {
        u32 c[KMAX + 1];
        for (int i = 1; i <= KMAX; i++) {
            u32 s = acc[i] + seg[node][i];
            for (int j = 1; j < i; j++) s += acc[j] * seg[node][i - j];
            c[i] = s;
        }
        for (int i = 1; i <= KMAX; i++) acc[i] = c[i];
        return;
    }
    int mid = (l + r) >> 1;
    if (ql <= mid) queryPoly(node << 1, l, mid, ql, qr, acc);
    if (mid < qr)  queryPoly(node << 1 | 1, mid + 1, r, ql, qr, acc);
}

int main() {
    if (scanf("%d %d", &n, &q) != 2) return 0;
    for (int i = 1; i <= n; i++) scanf("%u", &a[i].d);
    for (int i = 1; i <= n; i++) scanf("%u", &a[i].v);

    sort(a + 1, a + n + 1, cmpD);
    build(1, 1, n);

    for (int t = 0; t < q; t++) {
        u32 L, R;
        int K;
        scanf("%u %u %d", &L, &R, &K);

        int l = int(lower_bound(a + 1, a + n + 1, Pt{L, 0}, cmpD) - a);
        int r = int(upper_bound(a + 1, a + n + 1, Pt{R, 0}, cmpD) - a) - 1;

        if (l > r || (r - l + 1) <= K) { printf("0\n"); continue; }

        qmin = 0xFFFFFFFFu;
        qpos = -1;
        queryMin(1, 1, n, l, r);
        int pos = qpos;

        u32 left[KMAX + 1], right[KMAX + 1];
        memset(left, 0, sizeof left);
        memset(right, 0, sizeof right);
        if (l <= pos - 1) queryPoly(1, 1, n, l, pos - 1, left);
        if (pos + 1 <= r) queryPoly(1, 1, n, pos + 1, r, right);

        u32 ans[KMAX + 1];
        memset(ans, 0, sizeof ans);
        for (int i = 1; i <= KMAX; i++) {
            u32 s = left[i] + right[i];
            for (int j = 1; j < i; j++) s += left[j] * right[i - j];
            ans[i] = s;
        }

        u32 res = ans[K];
        for (int i = 2; i <= K; i++) res *= (u32)i;   // * K!
        printf("%u\n", res);
    }
    return 0;
}
