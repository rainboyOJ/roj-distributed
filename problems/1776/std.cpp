/*
 * 一本通 1776《最大值》 —— 标准程序（std）
 * ---------------------------------------------------------------------------
 * 题面来源（已 curl 实抓核对）:
 *   http://ybt.ssoier.cn:8088/problem_show.php?pid=1776
 *   该页标题「1776：最大值」，时间限制 1500 ms，内存限制 131072 KB，
 *   提交数 475 / 通过数 106，输入/输出样例与本目录 content.md 逐字一致。
 *
 * 公开题解检索记录（均未检索到本题解，故为自研实现）:
 *   1) CSDN 站内搜索 API:
 *      https://so.csdn.net/api/v3/search?q=<关键词>&p=1&s=0&tm=0&lv=-1&ft=0&ia=1
 *      关键词「一本通 1776 最大值 题解」「找最大值的游戏 一本通」→ 0 条相关结果；
 *   2) Bing 网页/RSS: https://www.bing.com/search?q=<关键词>&format=rss
 *      → 无相关结果；
 *   3) 博客园搜索: https://zzk.cnblogs.com/s?w=找最大值的游戏 → 0 篇（并要求人机验证）。
 *   本题非任何经典题的改写（题面自带 Alice/Bob 包装，三算子混合），无公开代码可参考。
 *
 * 算法依据（三个算子分别用各自的经典最优做法，复杂度均为 O(值域位数 × n)）:
 *   c=1 与运算(and): 逐位贪心。设 cur 为当前已确认的答案位集合，尝试 cand = cur | (1<<b)，
 *                    若存在 >= 2 个元素满足 (A_i & cand) == cand，则这一位可取。
 *                    （“最大与对”经典做法；可行谓词 P(m)=“存在一对数的 AND 覆盖 m”对子集单调）
 *   c=2 异或运算(xor): 0-1 Trie（二进制字典树）求最大异或对，经典套路
 *                    （即「最大异或对 / 最长异或路径」一类题的 0-1 Trie 写法；
 *                     此处不引 URL —— acwing/luogu 站点对 curl 返回 302 跳转，无法实取正文核对）。
 *   c=3 或运算(or):  逐位贪心 + 超集(SOS)预处理。cand 可取 ⟺ 存在一对数其 OR 覆盖 cand。
 *                    记 t_i = cand & ~A_i（A_i 在 cand 上缺失的位），则条件等价于
 *                    存在 i≠j 使 t_i ∩ t_j = ∅，亦即存在 i 使「某个值 v 满足 v ⊇ t_i」。
 *                    先对值域做一次超集 SOS 变换得到 sup[m] = 「是否存在值 v ⊇ m」，
 *                    之后每位判定只需 O(n)（每个元素 O(1) 查询）。
 *                    ⚠ 注意：最大元素不一定出现在最优或对中（反例 {10,5,12}: 10|5=15 > 12|10=14），
 *                    所以不能用「最大值与次大值配对」的简化写法。
 *
 * 复杂度: 每组数据 O(B·n + 2^(B)·B)（B = 值域最高位+1，题面 B <= 20），
 *         其中 2^B·B 仅 c=3 且所有值 < 2^20 时执行一次超集变换。
 * 输入: 第一行 T；随后每组两行——「n c」与 n 个整数 A_i。
 *       c=1 → and，c=2 → xor，c=3 → or（注意题面映射顺序与直觉不同）。
 * 输出: 每组一行一个整数，即 max_{1<=i<j<=n} (A_i op A_j)。
 * ---------------------------------------------------------------------------
 */
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

/* 数组上限按题面上限 × 安全系数开:
 *   n <= 10^5（题面）→ MAXN = 10^5 + 5
 *   T <= 6（题面）    → MAXT = 6 + 2（本程序逐组处理，未用数组，留注释说明）
 *   A_i < 2^20（题面）→ 值域 DOM = 2^20；Trie 按 31 位预留（越界数据兜底） */
static const int MAXN = 100000 + 5;
static const int MAXB = 20;                     /* 题面 A_i < 2^20 */
static const int DOM  = 1 << MAXB;              /* 1048576 */
static const int TRIEB = 30;                    /* Trie 位宽（含越界兜底） */
static const int MAXNODE = MAXN * (TRIEB + 1) + 5;

static int a[MAXN];
static int ch0[MAXNODE], ch1[MAXNODE];
static unsigned char sup[DOM];                  /* sup[m] = 1 ⟺ 存在值 v ⊇ m */
static int distinct_[MAXN];

static int nodeCnt;

static void trieReset(void) { nodeCnt = 0; ch0[0] = 0; ch1[0] = 0; }

static void trieInsert(int x, int hi) {
    int u = 0;
    for (int b = hi; b >= 0; --b) {
        int bit = (x >> b) & 1;
        int &nxt = bit ? ch1[u] : ch0[u];
        if (!nxt) { ++nodeCnt; ch0[nodeCnt] = 0; ch1[nodeCnt] = 0; nxt = nodeCnt; }
        u = nxt;
    }
}

/* 返回 x 与已插入元素的最大异或值（含与自身异或的 0，不影响最大值正确性） */
static int trieQuery(int x, int hi) {
    int u = 0, res = 0;
    for (int b = hi; b >= 0; --b) {
        int bit = (x >> b) & 1;
        int want = bit ^ 1;
        int nxt = want ? ch1[u] : ch0[u];
        if (nxt) { res |= (1 << b); u = nxt; }
        else { u = want ? ch0[u] : ch1[u]; }
    }
    return res;
}

static int hiBit(int mx) { int h = 0; while ((mx >> (h + 1)) != 0) ++h; return h; }

int main(void) {
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T-- > 0) {
        int n, c;
        if (scanf("%d %d", &n, &c) != 2) break;
        int mx = 0;
        for (int i = 0; i < n; ++i) { scanf("%d", &a[i]); if (a[i] > mx) mx = a[i]; }
        int hi = hiBit(mx);
        long long ans = 0;

        if (c == 1) {
            /* 最大与对: 逐位贪心 */
            int cur = 0;
            for (int b = hi; b >= 0; --b) {
                int cand = cur | (1 << b);
                int cnt = 0;
                for (int i = 0; i < n; ++i) {
                    if ((a[i] & cand) == cand) { if (++cnt >= 2) break; }
                }
                if (cnt >= 2) cur = cand;
            }
            ans = cur;
        } else if (c == 2) {
            /* 最大异或对: 0-1 Trie */
            trieReset();
            for (int i = 0; i < n; ++i) trieInsert(a[i], hi);
            int best = 0;
            for (int i = 0; i < n; ++i) { int v = trieQuery(a[i], hi); if (v > best) best = v; }
            ans = best;
        } else {
            /* 最大或对: 逐位贪心 + 超集判定 */
            int cur = 0;
            if (hi < MAXB) {
                int dom = 1 << (hi + 1);
                memset(sup, 0, (size_t)dom);
                for (int i = 0; i < n; ++i) sup[a[i]] = 1;
                for (int b = 0; b < hi + 1; ++b) {
                    int bit = 1 << b;
                    for (int m = 0; m < dom; ++m)
                        if (!(m & bit) && sup[m | bit]) sup[m] = 1;
                }
                for (int b = hi; b >= 0; --b) {
                    int cand = cur | (1 << b);
                    bool ok = false;
                    for (int i = 0; i < n; ++i) {
                        int r = cand & ~a[i];
                        if (r == 0 || sup[r]) { ok = true; break; }   /* n>=2 保证有第二个下标 */
                    }
                    if (ok) cur = cand;
                }
            } else {
                /* 兜底路径: 仅当数据越出题面上限（A_i >= 2^20）时触发，
                 * 退化为「去重后逐个值判定」，正确但最坏较慢（题面范围内不会走到这里）。 */
                int m = 0;
                for (int i = 0; i < n; ++i) distinct_[i] = a[i];
                sort(distinct_, distinct_ + n);
                m = (int)(unique(distinct_, distinct_ + n) - distinct_);
                for (int b = hi; b >= 0; --b) {
                    int cand = cur | (1 << b);
                    bool ok = false;
                    for (int i = 0; i < n && !ok; ++i) {
                        int r = cand & ~a[i];
                        if (r == 0) { ok = true; break; }
                        for (int j = 0; j < m; ++j)
                            if ((distinct_[j] & r) == r) { ok = true; break; }
                    }
                    if (ok) cur = cand;
                }
            }
            ans = cur;
        }
        printf("%lld\n", ans);
    }
    return 0;
}
