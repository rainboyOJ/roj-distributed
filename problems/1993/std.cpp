// 一本通 1993 开关switch —— 线段树（区间翻转 + 区间求和，懒标记）
// 参考来源（改写自该博客的题解代码）：
//   https://www.cnblogs.com/lyc-lb-blogs/p/14969883.html
// 思路：维护每个区间开灯数 sum 与区间长度 len；区间翻转即 sum = len - sum，
// 懒标记 tag 异或 1。初始全关，sum = 0。
#include <cstdio>
#include <initializer_list>

const int MAXN = 100000 + 5;

int n, m;
int sumv[MAXN * 4];  // 区间内开着的灯数
int lenv[MAXN * 4];  // 区间长度
int tag[MAXN * 4];   // 懒标记：是否需要翻转

void build(int u, int l, int r) {
    lenv[u] = r - l + 1;
    sumv[u] = 0;
    tag[u] = 0;
    if (l == r) return;
    int mid = (l + r) >> 1;
    build(u << 1, l, mid);
    build(u << 1 | 1, mid + 1, r);
}

void pushDown(int u) {
    if (tag[u]) {
        for (int s : {u << 1, u << 1 | 1}) {
            sumv[s] = lenv[s] - sumv[s];
            tag[s] ^= 1;
        }
        tag[u] = 0;
    }
}

void pushUp(int u) {
    sumv[u] = sumv[u << 1] + sumv[u << 1 | 1];
}

void modify(int u, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) {
        sumv[u] = lenv[u] - sumv[u];
        tag[u] ^= 1;
        return;
    }
    pushDown(u);
    int mid = (l + r) >> 1;
    if (ql <= mid) modify(u << 1, l, mid, ql, qr);
    if (qr > mid) modify(u << 1 | 1, mid + 1, r, ql, qr);
    pushUp(u);
}

int query(int u, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return sumv[u];
    pushDown(u);
    int mid = (l + r) >> 1, res = 0;
    if (ql <= mid) res += query(u << 1, l, mid, ql, qr);
    if (qr > mid) res += query(u << 1 | 1, mid + 1, r, ql, qr);
    return res;
}

int main() {
    scanf("%d %d", &n, &m);
    build(1, 1, n);
    while (m--) {
        int c, a, b;
        scanf("%d %d %d", &c, &a, &b);
        if (c == 0)
            modify(1, 1, n, a, b);
        else
            printf("%d\n", query(1, 1, n, a, b));
    }
    return 0;
}
