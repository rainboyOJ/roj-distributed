// 一本通 1748《大数计数》标程
// =====================================================================
// 题目等价于：[SCOI2016] 萌萌哒（洛谷 P3295 / BZOJ 4569）。
// 题意：长度为 n 的大数 S_1..S_n（S_1 为最高位，故 S_1 != 0），
//       给出 m 条限制，每条 (l1,r1,l2,r2) 表示子串 S[l1..r1] 与
//       S[l2..r2] 完全相同（长度相等）。求满足全部限制的 n 位数个数，
//       对 1e9+7 取模。范围：1 <= n,m <= 1e5。
//
// 做法：倍增（ST 表思想）+ 并查集（"逆用 ST 表"）
//   · 维护 log n 个并查集，第 k 个并查集刻画"以 i 开头、长度 2^k 的区间"
//     之间的相等关系。设 f[k][i] 为第 k 层上区间 [i, i+2^k-1] 的代表元。
//   · 加入限制 (l1,r1,l2,r2)（长度 L）：取 k = floor(log2 L)，用两段长度
//     2^k 的重叠区间覆盖 [l1,r1] 与 [l2,r2]：
//         unite(k, l1, l2);  unite(k, r1-2^k+1, r2-2^k+1);
//     两段 2^k 区间在各自范围内恰好覆盖整段，故与原限制等价。
//   · 自顶向下把高层关系"下放"到低层（逆用 ST 表）：
//         for k = log n .. 1:
//           for i (i+2^k-1 <= n):
//             p = find(k, i);
//             unite(k-1, i, p);
//             unite(k-1, i+2^(k-1), p+2^(k-1));
//   · 最后统计第 0 层并查集的连通块数 t（每个位置一个变量）。
//     块内数字必须相同；最高位所在块有 9 种选择（1..9），其余每块 10 种，
//     故答案 = 9 * 10^(t-1) mod (1e9+7)。（t=1 时答案恰为 9。）
//
// 复杂度 O((n+m) log n α)，内存 O(n log n)。
//
// 来源说明（已联网检索，代码按题面自行改写并编译 + 样例验证，非盲抄）：
//   本题经确认与 [SCOI2016] 萌萌哒 / 洛谷 P3295 / BZOJ 4569 同题。
//   1) https://blog.csdn.net/dibenshang5553/article/details/101207572
//      《【LG3295】[SCOI2016]萌萌哒》（转载自 http://www.cnblogs.com/heyujun/p/10542614.html）
//      —— 给出倍增并查集 AC 代码与公式 ans = 9*10^(t-1)（t 为底层连通块数）；
//         其"每次合并两段长度 2^k 的重叠区间 + 自顶向下下放"即本文做法。
//   2) https://blog.csdn.net/m0_74176921/article/details/137054273
//      《题解 P3295 【[SCOI2016]萌萌哒】》—— 详细解释"逆用 ST 表"的下放循环：
//         for(j=mx;j>=1;j--) for(i=1;i+(1<<j)-1<=n;i++){p=find(i,j);
//           merge(i,p,j-1), merge(i+(1<<(j-1)), p+(1<<(j-1)), j-1);}
//   3) 题解 P3295（洛谷专栏）https://www.luogu.com.cn/article/it7foeu6 —— 同上思路。
//   数据范围以一本通 content.md 为准（n,m <= 1e5），与洛谷 P3295 一致。
// =====================================================================
#include <cstdio>

const int MOD = 1000000007;
const int MAXN = 100005;
const int LOG = 18;   // 2^17 = 131072 > 1e5，层数 0..16 足够

static int fa[LOG][MAXN];   // fa[k][i]：第 k 层区间 [i, i+2^k-1] 的代表元
static int sz[LOG][MAXN];   // 按大小合并（size）
static int bin[LOG];        // bin[k] = 2^k

// 迭代式路径压缩 find，避免深层递归爆栈
static int find(int k, int x)
{
    int r = x;
    while (fa[k][r] != r) r = fa[k][r];
    while (fa[k][x] != r) { int nx = fa[k][x]; fa[k][x] = r; x = nx; }
    return r;
}

static void unite(int k, int a, int b)
{
    a = find(k, a);
    b = find(k, b);
    if (a == b) return;
    if (sz[k][a] < sz[k][b]) { int t = a; a = b; b = t; }
    fa[k][b] = a;
    sz[k][a] += sz[k][b];
}

int main()
{
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;

    bin[0] = 1;
    for (int k = 1; k < LOG; ++k) bin[k] = bin[k - 1] << 1;

    int lg = 0;
    while (lg + 1 < LOG && bin[lg + 1] <= n) ++lg;   // lg = floor(log2 n)

    for (int k = 0; k <= lg; ++k)
        for (int i = 1; i <= n; ++i) { fa[k][i] = i; sz[k][i] = 1; }

    for (int q = 0; q < m; ++q) {
        int l1, r1, l2, r2;
        scanf("%d %d %d %d", &l1, &r1, &l2, &r2);
        int len = r1 - l1 + 1;
        int k = 0;
        while (bin[k + 1] <= len) ++k;               // k = floor(log2 len)
        unite(k, l1, l2);
        unite(k, r1 - bin[k] + 1, r2 - bin[k] + 1);
    }

    // 自顶向下把高层相等关系下放到相邻两层
    for (int k = lg; k >= 1; --k) {
        int half = bin[k - 1];
        for (int i = 1; i + bin[k] - 1 <= n; ++i) {
            int p = find(k, i);
            unite(k - 1, i, p);
            unite(k - 1, i + half, p + half);
        }
    }

    // 统计底层连通块数
    int cnt = 0;
    for (int i = 1; i <= n; ++i)
        if (find(0, i) == i) ++cnt;

    long long ans = 9;                               // 最高位块：9 种（1..9）
    for (int i = 1; i < cnt; ++i) ans = ans * 10 % MOD;
    printf("%lld\n", ans);
    return 0;
}
