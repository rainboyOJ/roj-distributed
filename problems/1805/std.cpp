// 一本通 1805《数数》标程
//
// 同源原题：JZOJ 3492 /【NOIP2013模拟联考12】数数(count)
// 题意：给定等差数列 B+A, B+2A, ..., B+N*A（共 N 项），
//       统计每一项二进制表示中 1 的总个数。多组询问（T 组）。
//
// 思路（类欧几里得 / floor_sum）：
//   一个数 x 的第 k 位为 1  <=>  (x>>k) - 2*(x>>(k+1)) = 1，
//   故所有项 popcount 之和 = Σ_k [ S_k - 2*S_{k+1} ]，其中
//     S_k = Σ_{i=1}^{N} floor((B + A*i) / 2^k)
//         = Σ_{i=0}^{N-1} floor((A*i + (A+B)) / 2^k) = f(A, A+B, 2^k, N-1)。
//   其中 f(a,b,c,n) = Σ_{i=0}^{n} floor((a*i+b)/c)，用类欧几里得递归 O(log) 求出。
//   k 从 0（2^k=1）枚举到 2^k > B+A*N 为止（至多约 55 项）。
//
//   注意：S_0 = 所有项之和 = N*B + A*N*(N+1)/2，在 N≤1e12、B≤1e16 时
//   可达约 1e28，远超 64 位，故内部全程使用 __int128；
//   答案本身 ≤ 55*N ≈ 5.5e13，同样用 __int128 输出以防万一。
//
// 参考来源（联网检索得到，代码按题面自行改写并用题面样例验证）：
//   1) https://www.cnblogs.com/lfri/p/11665428.html
//      《JZOJ3492数数(count)&&GDOI2018超级异或绵羊——位&&类欧几里得》(Rogn)
//      ——含题面特征句原文「ztxz16想知道对于一个给定的等差数列…」及类欧标程：
//        for (mi=1; mi<=b+a*n; mi*=2)
//            ans += f(a, a+b, mi, n-1) - f(a, a+b, mi*2, n-1)*2;
//   2) https://blog.csdn.net/Cold_Chair/article/details/78847930
//      《【NOIP2013模拟联考12】数数(数位dp||类欧几里得）》
//   3) https://blog.csdn.net/HOWARLI/article/details/78851694
//      《【JZOJ 3492】【NOIP2013模拟联考12】数数 (count)》
//   原题在一本通高手训练的题号：1805（ybt.ssoier.cn/problem_show.php?pid=1805）。
#include <cstdio>
#include <cstring>

typedef __int128 i128;

// 打印 __int128
static void print_i128(i128 x)
{
    if (x == 0) { putchar('0'); return; }
    if (x < 0) { putchar('-'); x = -x; }
    char buf[64];
    int p = 0;
    while (x > 0) { buf[p++] = char('0' + (int)(x % 10)); x /= 10; }
    while (p--) putchar(buf[p]);
}

// f(a,b,c,n) = Σ_{i=0}^{n} floor((a*i + b) / c)   (a,b,c >= 0, n >= 0)
static i128 f(i128 a, i128 b, i128 c, i128 n)
{
    if (a == 0) return (b / c) * (n + 1);
    if (a >= c || b >= c)
        return f(a % c, b % c, c, n)
             + n * (n + 1) / 2 * (a / c)
             + (n + 1) * (b / c);
    i128 m = (a * n + b) / c;
    return n * m - f(c, c - b - 1, a, m - 1);
}

int main()
{
    int T;
    if (scanf("%d", &T) != 1) return 0;
    while (T--) {
        long long A, B, N;
        scanf("%lld %lld %lld", &A, &B, &N);
        long long limit = B + A * N;      // 最大项，≤ 2e16 < 2^55
        i128 ans = 0;
        for (long long mi = 1; mi <= limit; mi *= 2) {
            // S_{2^k} = f(A, A+B, 2^k, N-1)
            i128 s_lo = f(A, A + B, mi, N - 1);
            i128 s_hi = f(A, A + B, mi * 2, N - 1);
            ans += s_lo - 2 * s_hi;
        }
        print_i128(ans);
        putchar('\n');
    }
    return 0;
}
