// 一本通 1804《最大真因数》 标程（C++17）
//
// 来源 / 依据（网络检索，题面逐字一致的同源题：BZOJ 5244 / FJWC2018《最大真因数》）：
//   [1] https://blog.csdn.net/banchangyue3928/article/details/101775221
//       —— 【FJWC2018】最大真因数（题面与本题目逐字相同，含样例 1..5 与 min_25 筛做法 + 参考代码）
//   [2] https://blog.csdn.net/zltjohn/article/details/79672366
//       —— [JZOJ5594][min25筛]最大真因数
//   [3] https://blog.csdn.net/qq_33229466/article/details/79765380
//       —— bzoj 5244: [Fjwc2018]最大真因数 Min_25筛
//   [4] https://blog.csdn.net/zxyoi_dreamer/article/details/100120668
//       —— 【FJWC2018】最大真因数（min_25筛）
//   本实现按 [1] 的思路改写：去掉 unsigned 溢出的写法，改用 __int128 精确存储 g 数组，
//   并对 sqrt 取下整做了浮点校正（题面上限 r=5e9，sqrt 需精确）。
//
// 算法：
//   合数 n 的最大真因数 = n / spf(n)（spf 为最小质因子；n 的最大真因数即 n 除以最小质因子）。
//   令 f(n)=n/spf(n)（对质数 p 有 f(p)=1），则 [l,r] 内合数最大真因数之和
//       = Solve(r) - Solve(l-1)，Solve(N)=Σ_{合数 n<=N} n/spf(n)。
//   min_25 筛的 g 数组取权值 f(x)=x（恒等），筛到质数 p_j 时
//       g(n/p_j, j-1) - Σ_{i<j} p_i = Σ{ m : 2<=m<=n/p_j, spf(m)>=p_j }，
//   这正是「最小质因子恰为 p_j 的合数 n=p_j*m」的最大真因数之和（每个合数贡献 m=n/spf(n)），
//   仅在 i==1（w=n）处累加即得 Solve(n)。
//   复杂度 O(n^{3/4}/log n)，n=5e9 可秒过（题限 2000 ms）。
//
// 数值安全：w[1]=n 时 w*(w+1) 最大约 2.5e19 > 2^64，若用 unsigned long long 会溢出；
//   故 g / sp / ans 一律用 __int128 精确计算，最终答案 <= ~1.25e19 亦由 __int128 输出。
#include <cstdio>
#include <cmath>

typedef unsigned long long ull;
typedef __int128 lll;

static const int MAXM = 250005;   // 2*sqrt(5e9) ≈ 1.42e5，留足余量

static int prime[MAXM], tot;
static bool vis[MAXM];
static lll w[MAXM], g[MAXM], sp[MAXM];
static int id1[MAXM], id2[MAXM], m;

// 线性筛 [2, n]，prime[1..tot] 递增，sp[j]=Σ_{i<=j} prime[i]
static void Pre(int n) {
    tot = 0;
    for (int i = 2; i <= n; i++) {
        if (!vis[i]) { prime[++tot] = i; sp[tot] = sp[tot - 1] + i; }
        for (int j = 1; j <= tot && 1LL * i * prime[j] <= n; j++) {
            vis[i * prime[j]] = true;
            if (i % prime[j] == 0) break;
        }
    }
}

static lll Solve(ull n) {
    if (n < 4) return 0;              // 无合数（1、2、3 均无合数）
    tot = 0; m = 0;
    ull sqr = (ull)sqrtl((long double)n);
    while ((sqr + 1) * (sqr + 1) <= n) ++sqr;
    while (sqr * sqr > n) --sqr;
    Pre((int)sqr);

    // 把 n 的所有不同商 n/i 作为 w[1..m]（递减），并初始化 g = Σ_{2<=x<=w} x
    for (ull i = 1, j; i <= n; i = j + 1) {
        j = n / (n / i);
        w[++m] = n / i;
        g[m] = w[m] * (w[m] + 1) / 2 - 1;
        if (w[m] <= sqr) id1[w[m]] = m; else id2[n / w[m]] = m;
    }

    lll ans = 0;
    for (int j = 1; j <= tot; j++) {
        for (int i = 1; i <= m && (lll)prime[j] * prime[j] <= w[i]; i++) {
            ull v = w[i] / (ull)prime[j];
            int k = (v <= sqr) ? id1[v] : id2[n / v];
            if (i == 1) ans += g[k] - sp[j - 1];        // 累加最小质因子为 p_j 的合数之和
            g[i] -= (lll)prime[j] * (g[k] - sp[j - 1]); // 常规 min_25 筛转移
        }
    }
    return ans;
}

static void print(lll x) {
    if (x < 0) { putchar('-'); x = -x; }
    if (x > 9) print(x / 10);
    putchar('0' + (int)(x % 10));
}

int main() {
    ull l, r;
    if (scanf("%llu %llu", &l, &r) != 2) return 0;
    lll ans = Solve(r) - Solve(l - 1);
    print(ans);
    putchar('\n');
    return 0;
}
