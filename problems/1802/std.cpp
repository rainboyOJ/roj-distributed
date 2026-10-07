// 一本通 1802《寿司晚宴》标程
// 同源原题：NOI2015 Day1 T2 寿司晚宴（BZOJ 4197 / Luogu P2150）——题面逐字一致，判定依据见 gen-report.md §1。
//
// 算法：状压 DP + 按大质因子分组（分组背包）。
//   寿司 i (2<=i<=n) 的美味度即 i。方案和谐 <=> 不存在 x∈G, y∈W 使 gcd(x,y)>1
//   <=> 对每个质数 q，2..n 中 q 的倍数只能全归 G、全归 W 或全不选。
//   因 n<=500，任意 i<=500 至多含一个 >sqrt(500)≈22.36 的质因子（两个则积 >=23*23=529>500）。
//   故把 2..n 按「除掉小质数后剩下的那个大质因子」分组：
//     - 大质因子 == 1 的数是「小质数数」：其质因子全在 {2,3,5,7,11,13,17,19} 内，
//       用 mask 记录「G 已用的小质数集合」与「W 已用的小质数集合」，逐个做三选一（给 G / 给 W / 不给）；
//     - 大质因子 == q>1 的同一组：整组只能给 G 或整组只能给 W（不能给两人，否则二人各有一个 q 的倍数不互质）。
//       对每组开两份临时数组 g[0]/g[1]（分别表示本组给 W / 给 G），组内逐个加入，最后
//       f = g[0] + g[1] - f（减去「本组一个都不选」在两份里被重复计入的部分）。
//   答案 = sum f[maskG][maskW]，全程对 p 取模。
//
// 复杂度：状态 2^8 * 2^8 = 65536，元素 n-1 个，每个元素扫一遍状态 => O(n * 4^8) ≈ 3.3e7，
//   顶格 n=500 实测 < 0.1 s（题限 2000 ms），内存约 1 MB（题限 512 MB）。
//
// 参考来源（网络题解，已按题面自行改写并编译验证，非盲抄）：
//   1) https://blog.csdn.net/weixin_30951389/article/details/96553979
//      《【BZOJ4197】【Noi2015】寿司晚宴》——给出与本题完全同型的实现：
//      d[i]={i, 小质数mask, 除掉小质数后的大质因子}，按大质因子排序后分组，
//      g[0]/g[1] 双临时数组 + f=g0+g1-f 去重。本 std 的算法框架依据此篇。
//   2) https://blog.csdn.net/guapisolo/article/details/82779974
//      《NOI 2015 寿司晚宴 (状压DP+分组背包)》——同上框架，强调「大质因子分组、组内只能选一人」。
//   3) https://blog.csdn.net/jwg2732/article/details/118614831
//      《[NOI2015] 寿司晚宴(状压DP)》——同上；并确认小质数集合恰为 2..19 共 8 个（n<=500 时）。
//   检索证据与原始页面见 work/sources/、work/evidence/。
//
// 说明（与参考实现的差异，均为健壮性改写，算法等价）：
//   - 参考实现把 2..n 存在 d[1..n-1] 并依赖 d[n] 的全局零初始化来终止小质数循环；
//     本实现显式用长度 m=n-1 与 `while (j <= m && ...)` 边界，避免 n=2 时越界读。
//   - 参考实现用 int 承载 (g0+g1)（<2e9，接近 int 上限）；本实现统一 long long 防溢出。
//   - 加了 p<=0 的保底（题面表写作 0<=p<=1e9，原 NOI 题面为 0<p<=1e9；p=0 取模无定义，
//     正式数据严格 p>=1，见 gen-report.md §6）。
#include <cstdio>
#include <cstring>
#include <algorithm>

typedef long long ll;

static const int SP[8] = {2, 3, 5, 7, 11, 13, 17, 19};  // 小质数（<=19；23>sqrt(500) 归入大质因子）
static const int ALL = 1 << 8;                          // 小质数掩码空间 256

struct Item {
    int bigp;   // 除掉全部小质数后剩下的部分：1 表示「小质数数」，>1 即该数唯一的大质因子
    int mask;   // 小质数因子掩码（第 j 位 = 含质数 SP[j]）
};

static Item a[1005];        // 题面上限 n<=500，按 2 倍安全系数开
static bool cmpBigp(const Item &x, const Item &y) { return x.bigp < y.bigp; }

static ll f[ALL][ALL];
static ll g[2][ALL][ALL];

int main() {
    int n = 0;
    ll mod = 0;
    if (scanf("%d %lld", &n, &mod) != 2) return 0;
    if (mod <= 0) { printf("0\n"); return 0; }  // 保底：p=0 取模无定义，正式数据不出现

    int m = 0;
    for (int x = 2; x <= n; x++) {
        int y = x, mask = 0;
        for (int j = 0; j < 8; j++) {
            if (y % SP[j] == 0) {
                mask |= 1 << j;
                while (y % SP[j] == 0) y /= SP[j];
            }
        }
        a[++m].bigp = y;
        a[m].mask = mask;
    }
    std::sort(a + 1, a + m + 1, cmpBigp);

    memset(f, 0, sizeof(f));
    f[0][0] = 1;

    int i = 1;
    // ---- 第一段：大质因子为 1 的小质数数，逐个做「给 G / 给 W / 不给」----
    while (i <= m && a[i].bigp == 1) {
        int s = a[i].mask;
        for (int x = ALL - 1; x >= 0; x--) {
            for (int y = ALL - 1; y >= 0; y--) {
                ll v = f[x][y];
                if (!v) continue;
                if (!(s & y)) { ll &t = f[x | s][y]; t = (t + v) % mod; }  // 给 G：G 的掩码并上 s，且与 W 不冲突
                if (!(s & x)) { ll &t = f[x][y | s]; t = (t + v) % mod; }  // 给 W：对称
            }
        }
        i++;
    }

    // ---- 第二大段：按大质因子分组，每组只能整组给同一个人 ----
    while (i <= m) {
        int j = i;
        while (j + 1 <= m && a[j + 1].bigp == a[i].bigp) j++;  // 组区间 [i, j]
        memcpy(g[0], f, sizeof(f));  // g[0]：本组给 W
        memcpy(g[1], f, sizeof(f));  // g[1]：本组给 G
        for (int t = i; t <= j; t++) {
            int s = a[t].mask;
            for (int x = ALL - 1; x >= 0; x--) {
                for (int y = ALL - 1; y >= 0; y--) {
                    ll v0 = g[1][x][y];
                    if (v0 && !(s & y)) { ll &t2 = g[1][x | s][y]; t2 = (t2 + v0) % mod; }
                    ll v1 = g[0][x][y];
                    if (v1 && !(s & x)) { ll &t2 = g[0][x][y | s]; t2 = (t2 + v1) % mod; }
                }
            }
        }
        for (int x = 0; x < ALL; x++) {
            for (int y = 0; y < ALL; y++) {
                ll v = (g[0][x][y] + g[1][x][y] - f[x][y]) % mod;  // 减去两份重复计入的「本组不选」
                if (v < 0) v += mod;
                f[x][y] = v;
            }
        }
        i = j + 1;
    }

    ll ans = 0;
    for (int x = 0; x < ALL; x++)
        for (int y = 0; y < ALL; y++) ans = (ans + f[x][y]) % mod;
    printf("%lld\n", ans);
    return 0;
}
