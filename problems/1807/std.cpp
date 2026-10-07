// 一本通 1807《区间计数》
//
// 题意：令 S(n) 为 n 的各位数字之和，D(n) 为其迭代至 <10 的结果（即数根，n>=1 时
//       D(n) = 1 + (n-1) % 9）。若一个数 m 能写成 x * D(x)（题面写作 x*d(x)，样例
//       证实取的就是 D(x)）的形式，则称 m 是"小D喜欢的数"。多组询问 [L,R]，问其中
//       有多少个喜欢的数。
//       T <= 20，L,R <= 10^18，时限 1000ms / 256MB。
//
// 思路来源 / 依据：
//   官方 OJ 题目页（题名《区间计数》，1000 ms / 262144 KB，样例与本目录 content.md 一致）：
//     http://ybt.ssoier.cn:8088/problem_show.php?pid=1807
//   检索过程（3 轮，均无可用题解代码，故按题面自研，依据为下方数学推导）：
//     - Bing / DuckDuckGo / 百度：关键词「一本通 1807 区间计数 题解」「"小D喜欢的数" 题解」
//       均被拦截或返回无关结果；
//     - CSDN 站内搜索 API：关键词「一本通1807 区间计数」「小D喜欢的数」，返回均为无关文章。
//   本实现未照抄任何网络代码，正确性由题面样例（已复现）+ 数学推导 + 手算用例（见
//   gen-report.md）保证。
//
// 数学推导（std 算法）：
//   1) 数根性质：对 x >= 1，D(x) = d (1<=d<=9) <=> x ≡ d (mod 9)。
//   2) 于是 m 被"喜欢" <=> 存在 d ∈ [1,9]，使 m = x*d 且 x ≡ d (mod 9)，x >= 1。
//      把 x = d + 9k (k >= 0) 代入：m = d*(d + 9k) = d^2 + 9d*k。
//      所以  S_d = { m : m >= d^2 且 m ≡ d^2 (mod 9d) }，
//      喜欢的数 = ∪_{d=1..9} S_d（注意 S_d 之间会重叠，例如 m=36 = 12*D(12) = 6*D(6)
//      同时属于 S_3 与 S_6；m=64 同时属于 S_1 与 S_8，故不能简单求和，必须去重）。
//   3) 对 m >= 82（> 81 = max d^2）下界 m >= d^2 自动满足，条件只依赖 m 的余数；
//      而每个模数 9d 都整除 P = lcm(9,18,27,36,45,54,63,72,81) = 2^3*3^4*5*7 = 22680，
//      因此 m >= 82 时"是否喜欢"仅由 m mod P 决定 —— 喜欢的数集从 82 起以 P 为周期。
//   4) 预处理一个周期内每个余数 r ∈ [0,P-1] 的判定 ok[r] 与周期内计数 fullCnt、
//      以及按窗口起点 82 对齐的前缀和 prefOk[·]，则
//      count(N) = (m<=81 直接判定) + (N>=82 时： q*fullCnt + prefOk[rem])，
//      答案 = count(R) - count(L-1)。每组询问 O(1)（预处理 O(P)）。
//
// 复杂度：预处理 O(P) = O(22680)，每组询问 O(1)；T<=20 时总计约 1e5 次运算，远低于 1000ms。
// 答案上界 <= 10^18，long long 足够。

#include <cstdio>
#include <algorithm>
using namespace std;

typedef long long ll;

static const int DMAX = 9;          // d(x) 的取值范围 1..9
static const int SMALL = 81;        // max d^2 = 81
static const ll PERIOD = 22680;     // lcm(9,18,27,36,45,54,63,72,81)

// m <= 81 时的精确判定（含下界 m >= d^2）
static inline bool likedSmall(ll m) {
    for (int d = 1; d <= DMAX; ++d) {
        ll md = 9LL * d;
        if (m >= (ll)d * d && m % md == ((ll)d * d) % md) return true;
    }
    return false;
}

static bool okRes[PERIOD];      // okRes[r]：m >= 82 且 m % PERIOD == r 时是否喜欢
static ll prefOk[PERIOD + 1];   // prefOk[i] = #{j < i : okRes[(82 + j) % PERIOD]}
static ll fullCnt = 0;          // 一个周期内喜欢的余数个数

static void build() {
    for (int r = 0; r < (int)PERIOD; ++r) {
        bool ok = false;
        for (int d = 1; d <= DMAX && !ok; ++d) {
            ll md = 9LL * d;
            if (r % md == ((ll)d * d) % md) ok = true;
        }
        okRes[r] = ok;
        if (ok) ++fullCnt;
    }
    prefOk[0] = 0;
    for (int i = 0; i < (int)PERIOD; ++i)
        prefOk[i + 1] = prefOk[i] + (okRes[(82 + i) % PERIOD] ? 1 : 0);
}

// [1,N] 中喜欢的数的个数
static ll countUpto(ll N) {
    if (N <= 0) return 0;
    ll res = 0;
    ll lim = N < (ll)SMALL ? N : (ll)SMALL;
    for (ll m = 1; m <= lim; ++m) if (likedSmall(m)) ++res;
    if (N <= SMALL) return res;
    ll len = N - SMALL;             // [82,N] 的长度 = N - 81
    ll q = len / PERIOD, rem = len % PERIOD;
    res += q * fullCnt + prefOk[rem];
    return res;
}

int main() {
    build();
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        ll L, R;
        scanf("%lld %lld", &L, &R);
        printf("%lld\n", countUpto(R) - countUpto(L - 1));
    }
    return 0;
}
