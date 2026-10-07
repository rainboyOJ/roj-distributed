// 一本通 1777《寻找整数》标程  ——  C++17, stdin -> stdout
//
// ── 来源 ──────────────────────────────────────────────────────────────────
// 本题与 Codeforces 431D "Random Task" 完全同源（题面逐字对应）：
//   原题：https://codeforces.com/problemset/problem/431/D
//   参考题解（二分答案 + 数位 DP）：https://blog.csdn.net/paulliant/article/details/82850301
//   （同源判定：该题解给出的题面为「给定 m 和 k，求一个 n 使得 [n+1,2n] 中二进制恰好
//    有 k 个 1 的数恰有 m 个，0<=m<=10^18，1<=k<=64」，与 content.md 完全一致；
//    本机 codeforces.com 被 Cloudflare 拦截 403，故以该题解页面作为题面/解法依据。）
// 本仓库题目在原题基础上**多问一项**：「满足条件的 n 的个数（无穷多记 -1）」，
// 该部分为自研推导（见下），原题只需输出最小的 n。
//
// ── 思路 ──────────────────────────────────────────────────────────────────
// 记 f(n) = #{ x : n < x <= 2n 且 popcount(x) = k }，g(y) = #{ x : 0 <= x <= y, popcount(x)=k }。
// 则 f(n) = g(2n) - g(n)。又 2n 为偶数，偶数 x <= 2n 与 x/2 <= n 一一对应且 popcount 不变，故
//   g(2n) = g(n) + #{ 奇 x <= 2n : popcount(x) = k }
//         = g(n) + #{ y <= n-1 : popcount(2y+1) = k }
//         = g(n) + #{ y <= n-1 : popcount(y) = k-1 }.
// 于是
//   f(n) = C_k(n) := #{ y : 0 <= y <= n-1, popcount(y) = k-1 }.
// （等价地：f(n) - f(n-1) = [popcount(2n-1) = k] = [popcount(n-1) = k-1]，也即题解的单调性。）
//
// 因此 f(n) = m  ⇔  恰有 m 个「popcount = k-1」的数严格小于 n。
// 设 A = (所有 popcount = k-1 的非负整数) 升序，a_i 为其中第 i+1 小（0-indexed，a_0 = 2^{k-1}-1），
// 则 C_k(n) = m ⇔ a_{m-1} < n <= a_m（m >= 1），故
//   * m >= 1：n 取遍 [a_{m-1}+1, a_m]，最小 n = a_{m-1}+1，个数 = a_m - a_{m-1}；
//   * m = 0 ：n 取遍 [1, a_0]，取 n = 1，个数 = a_0 = 2^{k-1} - 1；
//   * k = 1 ：k-1 = 0，只有 y = 0 一个，C_1(n) ≡ 1 (n >= 1)，故 m = 1 时无穷多个 n → 个数 -1
//             （m ≠ 1 时 10^18 内无解，题面保证不出现）。
// 求 a_i：二分最小的 X 使 #{0<=j<=X : popcount(j) = p} >= i+1，计数走 64 位组合数 O(64)。
//
// ── 复杂度 ────────────────────────────────────────────────────────────────
// 每个询问 2 次二分（<= 64 步）× O(64) 组合计数 ≈ 8e3 次基本运算；
// t <= 2000 → 约 1.6e7 次，1s 限制内绰绰有余（最大点实测见 gen-report.md）。
// 所有中间量 <= C(64,32) ≈ 1.83e18 < 2^64，用 unsigned long long 不会溢出；
// 合法询问下 a_{m-1} < 10^18、a_m < 2^62，输出 n、个数同样落在 unsigned long long 内。

#include <cstdio>

typedef unsigned long long u64;

static u64 C[65][65];

static void initC() {
    for (int i = 0; i <= 64; ++i) {
        C[i][0] = 1;
        for (int j = 1; j <= i; ++j) C[i][j] = C[i - 1][j - 1] + (j <= i - 1 ? C[i - 1][j] : 0);
        for (int j = i + 1; j <= 64; ++j) C[i][j] = 0;
    }
}

// #{ j : 0 <= j <= X, popcount(j) == p }
static u64 countLE(u64 X, int p) {
    if (p < 0) return 0;
    u64 res = 0;
    int used = 0;
    for (int i = 63; i >= 0; --i) {
        if ((X >> i) & 1ULL) {
            int need = p - used;                       // 该位取 0，低位任取
            if (need >= 0 && need <= i) res += C[i][need];
            if (++used > p) return res;                // 已超 p 个 1，后续前缀都不合法
        }
    }
    if (used == p) ++res;                              // X 自身
    return res;
}

// 最小的 X 使 countLE(X, p) >= m（要求 m >= 1）
static u64 kth(u64 m, int p) {
    u64 lo = 0, hi = ~0ULL;
    while (lo < hi) {
        u64 mid = lo + ((hi - lo) >> 1);
        if (countLE(mid, p) >= m) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

int main() {
    initC();
    int t;
    if (scanf("%d", &t) != 1) return 0;
    while (t--) {
        u64 m;
        int k;
        if (scanf("%llu %d", &m, &k) != 2) break;

        if (k <= 1) {                       // popcount(x)=0 只有 x=0
            if (k == 1 && m == 1) printf("1 -1\n");   // 无穷多个 n
            else if (k == 0 && m == 0) printf("1 -1\n");
            else printf("0 0\n");                     // 题面保证不出现（10^18 内无解）
            continue;
        }

        int p = k - 1;                      // 1 <= p <= 63
        if (m == 0) {
            u64 a0 = (1ULL << p) - 1;       // n ∈ [1, 2^{k-1}-1]
            printf("1 %llu\n", a0);
            continue;
        }
        if (countLE(~0ULL, p) < m + 1) {    // 2^64 范围内无解（题面保证不出现）
            printf("0 0\n");
            continue;
        }
        u64 am1 = kth(m, p);                // a_{m-1}
        u64 am = kth(m + 1, p);             // a_m
        printf("%llu %llu\n", am1 + 1, am - am1);
    }
    return 0;
}
