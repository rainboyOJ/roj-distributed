// 一本通 1801《异或》标程（C++17，stdin -> stdout）
//
// ============================ 参考来源（联网检索） ============================
// 检索方式：CSDN 站内搜「一本通 1801 异或」直接命中同题题解；另以题面特征句
//   「gcd(a,b)=a xor b」定位到原题 UVA 12716 GCD XOR（同源，题面即本题）。
//   [1] https://blog.csdn.net/longxuan01/article/details/134631138
//       《1801：异或》—— 题面与 content.md **逐字一致**（含样例 3 -> 1、"只有(2,3)满足"
//       与 n<=10^7 数据规模），并给出核心思路与 O(n log n) 代码：
//         若 a>b，则 gcd(a,b)<=a-b 且 a xor b>=a-b，故 gcd(a,b)=a xor b 迫使
//         c := a-b = a xor b = gcd(a,b)；枚举 c，令 a=i*c（c|a），b=a-c，
//         再校验 (a xor b)==c 即可。复杂度 O(n log2 n)。
//   [2] https://blog.csdn.net/tc_to_top/article/details/48296401
//       《UVA 12716 GCD XOR (数论 gcd和异或不等式)》—— 同源原题的经典解，思路与 [1] 完全一致
//       （由 gcd<=a-b<=a xor b 得等号链，枚举 c 与倍数），互相印证。
//   [3] https://blog.csdn.net/dylan_frank/article/details/69443490
//       《Uva 12716 - GCD XOR(数域筛法+qijiyinqiao)》—— 同题另一篇，结论一致（数域筛法 = 本筛）。
// 依据：以上来源给出同一结论，与题面样例一致，故按 [1] 的思路改写为本实现
//       （非盲抄：[1] 的代码用 i 当 c、j 当 a 的嵌套循环，本文整理为带注释的清晰版本，
//        变量名与头文件风格重写，并加 long long 计数）。
// =============================================================================
//
// 题面（content.md）：给定正整数 n，求 [1,n] 内满足 gcd(a,b)=a xor b 的无序数对 (a,b) 个数。
// 限制：1000 ms / 128 MB（config.json）；数据规模 n<=10^7（100%）。
//
// ------------------------------- 算法 -------------------------------
// 设 a>b（a=b 时 gcd=a、a xor a=0，无解，故 a!=b；无序对与 a>b 一一对应）。
//   1) gcd(a,b) | (a-b)  =>  gcd(a,b) <= a-b；
//   2) 任意整数有 a xor b >= a-b（同奇偶且 |a-b| <= a xor b）；
//   故 gcd(a,b)=a xor b 时三数相等：gcd(a,b) = a-b = a xor b =: c。
//   于是 a = i*c（c|a），b = a-c；反过来若 a-b==a xor b==c 则 gcd(a,a-c)=gcd(a,c)=c
//   （因 c|a），条件成立。故只需枚举 c 与其倍数 a：
//        for c in 1..n/2:  for a = 2c, 3c, ... <= n:  if ((a ^ (a-c)) == c) ++ans;
//   每个无序对 (a,b)（a>b）唯一对应一个 c=gcd 与倍数 a，故恰好计一次。
// 复杂度 O(n log n) 时间（sum_{c<=n/2} n/c ≈ n ln n ≈ 1.6e8 @ n=1e7）、O(1) 额外空间。
// 答案规模 <= 循环次数 < 1.6e8，用 long long 计数（输出用 %lld）。
//
// ---------------------------- 样例自检 ----------------------------
//   n=3 : c=1 时 a=2 -> 2^1=3 != 1；a=3 -> 3^2=1 == 1 -> ans=1（题面样例 3 -> 1）✓
//   n=1 : 无对 -> 0；  n=2 : (1,2) gcd=1 但 1^2=3 -> 0
#include <cstdio>

int main() {
    long long n;
    if (scanf("%lld", &n) != 1) return 0;
    long long ans = 0;
    for (long long c = 1; c <= n / 2; ++c) {
        for (long long a = c + c; a <= n; a += c) {
            long long b = a - c;
            if ((a ^ b) == c) ++ans;
        }
    }
    printf("%lld\n", ans);
    return 0;
}
