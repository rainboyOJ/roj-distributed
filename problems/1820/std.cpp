// std.cpp：区间最大利润 —— 线段树维护区间 (最小值, 最大值, 最大利润)
//
// 对一段区间，我们关心三件事：
//   minv : 区间内最低价（最适合买入）
//   maxv : 区间内最高价（最适合卖出）
//   best : 区间内 max(A[j] - A[i]) 且 i < j
//
// 合并两个相邻区间 L、R 时：
//   minv = min(L.minv, R.minv)
//   maxv = max(L.maxv, R.maxv)
//   best = max(L.best, R.best, R.maxv - L.minv)
// 第三项是「在 L 里买、在 R 里卖」的情况，天然满足 i < j。
//
// 复杂度：建树 O(n)，每次询问 O(log n)，总 O(n + q log n)。
#include <cstdio>
#include <algorithm>

using namespace std;

const int MAXN = 100005;
const long long NEG_INF = -2000000000000000000LL; // 答案可能为负，取足够小的初值

struct Node {
    long long minv; // 区间最低价
    long long maxv; // 区间最高价
    long long best; // 区间内最大利润（i < j）
};

int n, q;
long long a[MAXN];
Node tree[MAXN * 4];

// 把左右两个孩子合并成父结点
Node merge_node(const Node &L, const Node &R)
{
    Node res;
    res.minv = min(L.minv, R.minv);
    res.maxv = max(L.maxv, R.maxv);
    res.best = max(max(L.best, R.best), R.maxv - L.minv);
    return res;
}

// 建树：单点就是一个价格，自己和自己不能构成交易，所以 best 设为负无穷
void build(int p, int l, int r)
{
    if (l == r) {
        tree[p].minv = a[l];
        tree[p].maxv = a[l];
        tree[p].best = NEG_INF; // 长度为 1 的区间没有合法交易
        return;
    }
    int mid = (l + r) / 2;
    build(p * 2, l, mid);
    build(p * 2 + 1, mid + 1, r);
    tree[p] = merge_node(tree[p * 2], tree[p * 2 + 1]);
}

// 查询区间 [ql, qr]
Node query(int p, int l, int r, int ql, int qr)
{
    if (ql <= l && r <= qr) // 完全覆盖，直接返回
        return tree[p];

    int mid = (l + r) / 2;
    if (qr <= mid) // 全在左边
        return query(p * 2, l, mid, ql, qr);
    if (ql > mid)  // 全在右边
        return query(p * 2 + 1, mid + 1, r, ql, qr);

    // 跨过中点，左右都查，再合并
    Node L = query(p * 2, l, mid, ql, qr);
    Node R = query(p * 2 + 1, mid + 1, r, ql, qr);
    return merge_node(L, R);
}

int main()
{
    scanf("%d %d", &n, &q);
    for (int i = 1; i <= n; i++)
        scanf("%lld", &a[i]);

    build(1, 1, n);

    for (int i = 0; i < q; i++) {
        int l, r;
        scanf("%d %d", &l, &r);
        Node res = query(1, 1, n, l, r);
        printf("%lld\n", res.best);
    }
    return 0;
}
