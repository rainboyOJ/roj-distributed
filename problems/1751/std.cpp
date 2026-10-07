// 一本通 1751《字符串排序》 标程 (std.cpp)
//
// ---------------------------------------------------------------------------
// 来源 / 依据（网络检索，2026-10-06 实取正文核对）
// ---------------------------------------------------------------------------
// [1] 本题同源原题：Codeforces 558E "A Simple Task"
//     （n<=1e5, q<=1e5, 每次把子串按升序/降序排序，字符串只含小写字母）。
//     实取 CSDN《【CF558E】A Simple Task（线段树）》正文核对：
//     https://blog.csdn.net/hhaannyyii/article/details/78166952
//     其 Description 为「给定一个长度为 n 的小写字母序列，有 m 个操作，每次将第 l 个字母
//     到第 r 个字母排成升序或倒序，求最后得到的序列」——与本题题面逐句一致；
//     且本题题面输入样例 `5 2 / cabcd / 1 3 1 / 3 5 0`、数据范围（40% n,m<=1000；
//     100% n,m<=1e5）与 CF558E 完全一致 —— 判定为 CF558E 同源。
//     另见 CSDN《CF558E A Simple Task 线段树》
//     https://blog.csdn.net/xxxxxiao123/article/details/115538696
//
// [2] 一本通题解（直接对应题号 ybt 高效进阶 4-4-5 = 一本通 1751）：
//     CSDN《【ybt高效进阶4-4-5】字符串排序》
//     https://blog.csdn.net/weixin_43346722/article/details/115336217
//     该文给出「26 个线段树/树状数组分别记录每个字符出现情况 + 区间覆盖（赋值）
//     而非区间累加」的做法：对一次排序，先统计区间内 26 个字母各有多少个，
//     再按升/降序把这 26 段字符整段整段地覆盖回原区间。
//     该文 main() 读入顺序实为 `scanf("%d %d %d", &x, &y, &op)`，其中 x 作左端点、
//     y 作右端点（即 `l r x`）——与题面样例互证输入顺序。
//
// ---------------------------------------------------------------------------
// 算法
// ---------------------------------------------------------------------------
// 每个字母 c (0..25) 维护一棵线段树 tree_c，位置 i 的值为 1 当且仅当 S_i == c。
// 支持两种操作：
//   * range_sum(c, l, r)  —— 区间求和（得到 c 在 [l,r] 中的出现次数）
//   * range_assign(c,l,r,v) —— 区间覆盖为常量 v（v=1 表示把 [l,r] 全部刷成字母 c）
// 一次排序 (l,r,x)：
//   1) 对 c=0..25 求 cnt[c] = range_sum(c, l, r)；
//   2) 因为 26 棵树相互独立，赋值前必须先把 [l,r] 内“所有出现过的字母”清 0
//      （cnt[c]>0 的 c；cnt[c]==0 的字母在该区间本就全 0，无需清）。否则旧字母
//      残留在自己的树里，会与新区间划分冲突。
//   3) pos=l；若 x=1 升序，c 从 0 到 25；若 x=0 降序，c 从 25 到 0：
//        对每个 cnt[c]>0 的 c：range_assign(c, pos, pos+cnt[c]-1, 1)，pos += cnt[c]。
//      因为 cnt[] 是对 [l,r] 的一个划分，全部覆盖完成后 [l,r] 内每个位置恰属一个字母。
//   4) 清空 + 覆盖后 26 棵树在 [l,r] 上保持一致。
// 最后逐位求值（DFS 收集）得到答案串。
//
// 复杂度：每次操作 O(26 log n)（26 次区间求和 + ≤26 次区间清零 + ≤26 次区间覆盖），
//         总 O((n + 78 m) log n)；空间 O(26 n)。
//
// 相对来源 [2] 的改写点：
//   * 来源 [2] 用一棵 26 计数的合并线段树（每个节点存 26 个计数，向上合并循环 26 次），
//     单次覆盖的向上合并代价为 O(26 log n)，26 段即 O(26^2 log n)/次操作；
//     本标程改为 **26 棵独立线段树**，每棵向上合并 O(1)，单次操作降到 O(26 log n)，
//     常数更小、更适合 n,m=1e5 顶格数据（其余逻辑与来源一致）。
//   * 输入参数顺序按题面【输入样例】确认为 `l r x`（题面正文写“x,l,r”与样例矛盾，
//     以样例为准：`1 3 1` 表示 l=1,r=3,升序，`3 5 0` 表示 l=3,r=5,降序 → 输出 abdcc）。
//   * 采用 fast stdin/stdout（scanf/putchar），边界按题面上限 n<=1e5 开 4n。
//
// 编译：g++ -O2 -std=c++17 -Wall -Wextra std.cpp -o std
// ---------------------------------------------------------------------------

#include <cstdio>

static const int MAXN = 100005;

int n, m;
char s[MAXN + 1];

// tree[c]: 字母 c 的线段树（区间和）；tag[c]: 区间覆盖标记（-1 无标记，0/1 覆盖值）
static int tree[26][4 * MAXN];
static signed char tag[26][4 * MAXN];

void build(int c, int node, int l, int r) {
    tag[c][node] = -1;
    if (l == r) {
        tree[c][node] = (s[l] - 'a' == c) ? 1 : 0;
        return;
    }
    int mid = (l + r) >> 1;
    build(c, node << 1, l, mid);
    build(c, node << 1 | 1, mid + 1, r);
    tree[c][node] = tree[c][node << 1] + tree[c][node << 1 | 1];
}

inline void apply(int c, int node, int l, int r, int v) {
    tree[c][node] = v ? (r - l + 1) : 0;
    tag[c][node] = (signed char)v;
}

inline void pushdown(int c, int node, int l, int r) {
    if (tag[c][node] == -1 || l == r) return;
    int mid = (l + r) >> 1;
    int v = tag[c][node];
    apply(c, node << 1, l, mid, v);
    apply(c, node << 1 | 1, mid + 1, r, v);
    tag[c][node] = -1;
}

int query(int c, int node, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return tree[c][node];
    pushdown(c, node, l, r);
    int mid = (l + r) >> 1, res = 0;
    if (ql <= mid) res += query(c, node << 1, l, mid, ql, qr);
    if (qr > mid) res += query(c, node << 1 | 1, mid + 1, r, ql, qr);
    return res;
}

void update(int c, int node, int l, int r, int ql, int qr, int v) {
    if (ql > qr) return;
    if (ql <= l && r <= qr) {
        apply(c, node, l, r, v);
        return;
    }
    pushdown(c, node, l, r);
    int mid = (l + r) >> 1;
    if (ql <= mid) update(c, node << 1, l, mid, ql, qr, v);
    if (qr > mid) update(c, node << 1 | 1, mid + 1, r, ql, qr, v);
    tree[c][node] = tree[c][node << 1] + tree[c][node << 1 | 1];
}

char ans[MAXN + 1];

// 收集字母 c 出现在哪些位置（跳过整段为 0 的子树，整体 O(26 n) 以内）
void collect(int c, int node, int l, int r) {
    if (tree[c][node] == 0) return;
    if (l == r) {
        ans[l] = (char)('a' + c);
        return;
    }
    pushdown(c, node, l, r);
    int mid = (l + r) >> 1;
    collect(c, node << 1, l, mid);
    collect(c, node << 1 | 1, mid + 1, r);
}

int main() {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    if (scanf("%s", s + 1) != 1) return 0;

    for (int c = 0; c < 26; ++c) build(c, 1, 1, n);

    int cnt[26];
    for (int q = 0; q < m; ++q) {
        int l, r, x;
        if (scanf("%d %d %d", &l, &r, &x) != 3) break;
        for (int c = 0; c < 26; ++c) cnt[c] = query(c, 1, 1, n, l, r);
        // 先把区间内出现过的字母整段清 0（26 棵树独立，赋值不会自动清掉旧字母）
        for (int c = 0; c < 26; ++c)
            if (cnt[c] > 0) update(c, 1, 1, n, l, r, 0);
        int pos = l;
        if (x == 1) {  // 升序：a..z 从左到右
            for (int c = 0; c < 26 && pos <= r; ++c) {
                if (cnt[c] > 0) {
                    update(c, 1, 1, n, pos, pos + cnt[c] - 1, 1);
                    pos += cnt[c];
                }
            }
        } else {  // 降序：z..a 从左到右
            for (int c = 25; c >= 0 && pos <= r; --c) {
                if (cnt[c] > 0) {
                    update(c, 1, 1, n, pos, pos + cnt[c] - 1, 1);
                    pos += cnt[c];
                }
            }
        }
    }

    for (int c = 0; c < 26; ++c) collect(c, 1, 1, n);

    ans[n + 1] = '\0';
    fputs(ans + 1, stdout);
    putchar('\n');
    return 0;
}
