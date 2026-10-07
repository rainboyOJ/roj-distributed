#include <cstdio>

// 一本通 2019：【例4.4】求阶乘
// 题意：读入正整数 n（1 ≤ n ≤ 20），输出 n! = 1*2*...*n。
// 数据范围声明 1 ≤ n ≤ 20，20! = 2432902008176640000 ≈ 2.43e18 < 2^63-1 ≈ 9.22e18，
// 因此用 64 位有符号整数（long long）即可精确表示，无需高精度。
//
// 参考来源（已改写，仅取思路/写为 C++17 stdin→stdout）：
// [1] 君义_noip《信息学奥赛一本通 2019：【例4.4】求阶乘》
//     https://blog.csdn.net/lq1990717/article/details/116675422
//     要点：n ≤ 20 时 20! 为 18 位数，只能用 long long 表示；累乘变量初值必须为 1。
// [2] whsgs2010《信息学奥赛一本通网站（C++版）例题2019：【例4.4】求阶乘 参考答案》
//     https://blog.csdn.net/whsgs2010/article/details/132527807
//     要点：for (i = 1; i <= n; ++i) res *= i; 输出 res。
// [3] summe4《信息奥赛一本通2019：【例4.4】求阶乘》
//     https://blog.csdn.net/summe4/article/details/128554831
//     要点：同上，附一本通评测通过记录 statusx.php?runidx=20575487。
// 三份来源结论一致：n ≤ 20 用 long long 累乘即可，无冲突，与题面一致。

int main() {
    long long n = 0;
    if (scanf("%lld", &n) != 1) return 0;
    long long res = 1;                 // 0! = 1；本题 n ≥ 1，初值为 1 是关键
    for (long long i = 1; i <= n; ++i) {
        res *= i;                      // 20! 仍在 long long 范围内，不会溢出
    }
    printf("%lld\n", res);
    return 0;
}
