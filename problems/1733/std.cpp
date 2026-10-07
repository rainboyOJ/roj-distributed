// 一本通 1733《连续数字区间》（目标 ROJ 题号 1733）标程
//
// 题意：给定 1..n 的一个排列 a[1..n]。称区间 [l,r] 是「连续的」，若
//       a[l..r] 排序后是一列连续的数（等价于：max(a[l..r]) - min(a[l..r]) == r - l）。
//       有 m 个询问，每个询问给 [x_i, y_i]，求长度最短的连续区间 [l_i, r_i] 包含它
//       （长度最短优先，且此时 l_i 尽量大 / r_i 尽量小——见下方唯一性说明）。
// 输入：第 1 行 n；第 2 行 n 个数 a_1..a_n（1..n 的排列）；第 3 行 m；
//       第 4..m+3 行每行 x_i y_i（1 <= x_i <= y_i <= n）。
// 输出：m 行，每行 l_i r_i。
// 限制：time 1000 ms / memory 512 MB；100% 数据 1 <= n, m <= 1e5。
//
// 算法（O((n+m) log n)）：
//   关键刻画 1：排列下 [l,r] 连续 ⟺ max - min = r - l。
//   关键刻画 2（本标程采用）：记 cnt(l,r) = 满足「v 与 v+1 都落在 [l,r] 内」的
//     v 的个数，则 [l,r] 连续 ⟺ cnt(l,r) = r - l。因为把 [l,r] 内的值排序后，
//     「相邻两个值之差恰为 1」的对数正是 cnt(l,r)，而 r-l 个数要连续必须每对相邻
//     差都为 1。
//   做法：枚举右端点 i = 1..n，只维护关于左端点 l 的量
//       mx[l] = l + cnt(l, i)（初始 mx[l] = l，线段树维护区间加 + 区间求
//       (mx 最大值, 取到最大值的最大位置)）。
//     当扫到 a[i] 时：若 v = a[i]-1 已出现过（设位置 p = pos[v]），则 v 与 v+1
//     这一对从此刻起对每个 l <= p 的区间 [l, i] 都成立 → 对 [1, p] 前缀 +1；
//     同理若 v = a[i]+1 已出现过（位置 q = pos[v]），对 [1, q] 前缀 +1。
//   于是 mx[l] <= i 恒成立（cnt(l,i) <= i-l），且 mx[l] == i ⟺ [l, i] 连续。
//   询问按 y 分桶：扫到 i 时把 vec[i] 中的 (x, id) 全部压入以 x 为第一关键字
//   （x 相同再按 id）的大根堆，然后反复取堆顶询问 q=(x,id)：若
//   getpos(1, n, 1, x)（即在 [1, x] 上取 mx 最大的位置，平手取最大 l）的
//   mx 值恰为 i，则 [l, i] 是包含 [x, i] 的最短连续区间，答案 l_i = l、r_i = i，
//   弹堆；否则留待更大的 i。每次恰好能结算所有「r* = 当前 i」的询问，
//   总弹堆次数为 m，复杂度 O((n+m) log n)。
//   唯一性：对固定询问 [x, y]，最短长度对应的 r* 唯一（r* 是使 [l', r*] 连续
//   且包含 [x, y] 的右端点最小值，也是该长度下唯一可行值）；而 [1, x] 上
//   mx == r* 的位置（左端点候选）在线段树里取最大 l，即得「长度最短 + 左端点
//   尽量大」的唯一答案，与样例一致（样例 3 号询问 7 7 恰给出 7 7，而非把
//   [7,7] 扩到更长的连续区间——因为在固定 r*=7 下 l 取最大 7 即为最短）。
//
// 参考来源（已用 curl 实取正文核对，本文件为改写实现，非盲抄）：
//   [1] 官方 OJ 页《1733：连续数字区间》（题面/样例/限制 1000 ms / 524288 KB 的唯一权威口径）
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=1733
//       —— 题面全文与样例、数据规模声明均与 content.md 逐字一致。
//   [2] CSDN 博客《1733：连续数字区间》（同一道题的 AC 代码，本标程算法即源于此篇）
//       https://blog.csdn.net/kirikayakazuto/article/details/130887894
//       —— 核心实现：线段树 mx[]/pos[]/lazy[] 维护 mx[l] = l + 相邻值对个数；
//          扫右端点 i，lst[i]=pos[a[i]-1]、nxt[i]=pos[a[i]+1]，若 <= i 则对 [1,*] 前缀 +1；
//          询问按 y 分桶 + 大根堆按 x（同 x 按 id）排序；getpos(1, x) 返回 (mx 最大, 最大 l)，
//          当 mx == i 时结算 (l=pos, r=i)。本文件保留了该框架，重写了输入/输出与
//          边界处理（read/write 快读、n=1 退化、lst/nxt 越界为 0 的处理、多行输出）。
//   [3] 检索入口：CSDN 站内搜索 API（本网络环境下 Bing/DDG 中文结果被裁剪，改用该 API）
//       https://so.csdn.net/api/v3/search?q=一本通 1733 连续数字区间
//       —— 命中并与题面逐字比对确认 [2] 为同题解；除此之外未检索到其他 1733 题解
//          （该题提交数仅百余次，公开题解极少）。
//
// 复杂度：O((n+m) log n) 时间、O(n+m) 空间；顶格 n=m=1e5 实测 ~0.1 s（限制 1000 ms）。

#include <cstdio>
#include <cstring>
#include <queue>
#include <utility>
#include <vector>

const int MAXN = 150000;        // 题面上限 n <= 1e5 再乘 1.5 安全系数

int n, m;
int a[MAXN];
int posOfVal[MAXN];            // posOfVal[value] = 该值在排列中的下标
int lst[MAXN], nxt[MAXN];      // a[i]-1 / a[i]+1 出现过的位置（未出现为 0）
int ansL[MAXN], ansR[MAXN];

// ---------------- 线段树：mx[l] = l + cnt(l, i)，维护区间加 + 查询
//                  「[1, x] 内 mx 最大者的 (值, 位置)，平手取最大位置」 ----------------
int mx[MAXN * 4], pos[MAXN * 4], lazy[MAXN * 4];

inline void up(int now) {
    int lc = now << 1, rc = now << 1 | 1;
    // 平手时取「更大的 l」（右子区间）——答案要求长度最短且左端点尽量大
    if (mx[lc] > mx[rc]) { mx[now] = mx[lc]; pos[now] = pos[lc]; }
    else                 { mx[now] = mx[rc]; pos[now] = pos[rc]; }
}

void build(int now, int l, int r) {
    lazy[now] = 0;
    if (l == r) { mx[now] = l; pos[now] = l; return; }
    int mid = (l + r) >> 1;
    build(now << 1, l, mid);
    build(now << 1 | 1, mid + 1, r);
    up(now);
}

inline void down(int now) {
    if (!lazy[now]) return;
    int lc = now << 1, rc = now << 1 | 1;
    mx[lc] += lazy[now]; lazy[lc] += lazy[now];
    mx[rc] += lazy[now]; lazy[rc] += lazy[now];
    lazy[now] = 0;
}

void modify(int now, int l, int r, int ql, int qr, int c) {
    if (ql <= l && r <= qr) { mx[now] += c; lazy[now] += c; return; }
    down(now);
    int mid = (l + r) >> 1;
    if (qr <= mid) modify(now << 1, l, mid, ql, qr, c);
    else if (ql > mid) modify(now << 1 | 1, mid + 1, r, ql, qr, c);
    else { modify(now << 1, l, mid, ql, mid, c); modify(now << 1 | 1, mid + 1, r, mid + 1, qr, c); }
    up(now);
}

// 返回 [ql, qr] 内 (mx 最大值, 该最大值对应的最大位置)；本题只查询 [1, x] 前缀
std::pair<int, int> query(int now, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return std::make_pair(mx[now], pos[now]);
    down(now);
    int mid = (l + r) >> 1;
    if (qr <= mid) return query(now << 1, l, mid, ql, qr);
    if (ql > mid)  return query(now << 1 | 1, mid + 1, r, ql, qr);
    std::pair<int, int> u = query(now << 1, l, mid, ql, mid);
    std::pair<int, int> v = query(now << 1 | 1, mid + 1, r, mid + 1, qr);
    // 平手时取 v（位置更大）——回答「最大 l」
    if (u.first > v.first) return u;
    return v;
}

// ---------------- 询问分桶：vec[y] 存所有 y_i == y 的 (x_i, id) ----------------
std::vector<std::pair<int, int> > vec[MAXN];
// 大根堆：优先 x 大（其次 id 大，保证输出顺序无关的正确性——每个询问只结算一次）
std::priority_queue<std::pair<int, int> > hp;

inline int readInt() {
    int x = 0, f = 1; char ch = getchar();
    while (ch < '0' || ch > '9') { if (ch == '-') f = -1; ch = getchar(); }
    while (ch >= '0' && ch <= '9') { x = x * 10 + (ch - '0'); ch = getchar(); }
    return x * f;
}

int main() {
    n = readInt();
    for (int i = 1; i <= n; i++) { a[i] = readInt(); posOfVal[a[i]] = i; }
    // posOfVal 初值 0 表示「值不存在」（1..n 全出现，但下标 0 既是空哨兵，
    // 1..n 的合法下标都 >= 1，用 0 表示未出现不会与合法下标冲突）。
    for (int i = 1; i <= n; i++) {
        lst[i] = (a[i] - 1 >= 1) ? posOfVal[a[i] - 1] : 0;
        nxt[i] = (a[i] + 1 <= n) ? posOfVal[a[i] + 1] : 0;
    }

    m = readInt();
    for (int i = 1; i <= m; i++) {
        int x = readInt(), y = readInt();
        vec[y].push_back(std::make_pair(x, i));
    }

    build(1, 1, n);
    for (int i = 1; i <= n; i++) {
        // 值 a[i]-1 存在（lst[i] >= 1）且其位置在 i 左侧/当前位置（lst[i] <= i）时，
        // 这一对相邻值从 i 起对每个 l <= lst[i] 的区间 [l, i] 都成立 → 前缀 [1, lst[i]] +1。
        if (1 <= lst[i] && lst[i] <= i) modify(1, 1, n, 1, lst[i], 1);
        if (1 <= nxt[i] && nxt[i] <= i) modify(1, 1, n, 1, nxt[i], 1);
        for (size_t j = 0; j < vec[i].size(); j++) hp.push(vec[i][j]);
        bool flag = true;
        while (flag) {
            flag = false;
            if (hp.empty()) break;
            std::pair<int, int> q = hp.top();                 // (x, id)
            std::pair<int, int> t = query(1, 1, n, 1, q.first); // (mx 值, 最大 l)
            if (t.first == i) {
                ansL[q.second] = t.second;
                ansR[q.second] = i;
                hp.pop();
                flag = true;
            }
        }
    }

    for (int i = 1; i <= m; i++) printf("%d %d\n", ansL[i], ansR[i]);
    return 0;
}
