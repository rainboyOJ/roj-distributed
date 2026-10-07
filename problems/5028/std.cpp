// 一本通 2026《【例4.12】阶乘和》— 标程（C++17，stdin -> stdout）
// 题号：ybt 2026 / 目标 ROJ 5028   |   限制：time 1000 ms，memory 65536 KB
//
// 题意：输入正整数 n，求 S = 1! + 2! + 3! + ... + n!，输出 S。样例：n=3 -> 9。
// 数据范围（题面【提示】明文）：1 <= n <= 10。
//
// 参考来源 URL（本轮均逐条联网抓取原文核对后改写，非盲抄）：
//   [1] 官方题面（样例 3 -> 9、1000 ms / 65536 KB、1<=n<=10）
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2026
//   [2] CSDN · 君义NOIP《信息学奥赛一本通 1091:求阶乘的和 | 2026：【例4.12】阶乘和 |
//       OpenJudge NOI 1.5 34:求阶乘的和》——给出四种解法：双层循环 O(n^2)、阶乘函数 O(n^2)、
//       迭代 O(n)（v *= i; sum += v）、递归；四者结果一致
//       https://blog.csdn.net/lq1990717/article/details/112387062
//   [3] CSDN · afrwwew《2026：【例4.12】阶乘和》——"模拟"（双层循环按定义逐项求阶乘）与
//       "数学方法"（递推 i! = (i-1)! * i 后累加）两种做法，均 AC
//       https://blog.csdn.net/afrwwew/article/details/135610273
//   [4] CSDN · 橙子教师（lvcheng0309）《信息学奥赛一本通（2026：【例4.12】阶乘和）》——
//       递归阶乘函数 fact(n) + 主循环累加，`int` 版本，输出 %d
//       https://blog.csdn.net/lvcheng0309/article/details/116719185
//   [5] CSDN · Doopny@（2402_84298973）《阶乘和（信息学奥赛一本通-2026）》——
//       迭代写法，用 long long 累乘累加
//       https://blog.csdn.net/2402_84298973/article/details/146173734
//   [6] OEIS A007489（a(n) = Sum_{k=1..n} k!）——外部独立真值表，用于交叉核对本包全部输出：
//       0, 1, 3, 9, 33, 153, 873, 5913, 46233, 409113, 4037913, 43954713, ...
//       https://oeis.org/A007489
//
// 思路（来源 [2]-解法3 与 [3]-数学方法，两者本质相同，全部来源结论无冲突）：
//   记 term = i!，则 term = (i-1)! * i，无需每次从头连乘，单重循环即可：
//     term = 1, sum = 0
//     for i = 1..n:  term *= i;  sum += term;     // 循环第 i 轮后 term = i!，sum = 1!+...+i!
//   时间复杂度 O(n)，空间 O(1)。
//
// 数值与精度说明（回应任务书「浮点口径」提醒）：
//   * 本题**全程整数运算、无任何浮点**，不存在 2058 那类 %g / printf 的平台差异问题；
//     输出用 %lld（整数精确十进制），macOS / glibc / Windows 三平台逐字节一致。
//   * 上界 n=10 时 10! = 3628800、S = 4037913，远小于 int 上限 2^31-1，故来源 [4] 的
//     `int` 版本在本数据范围内也不溢出。本标程仍用 long long（零成本）以免对越界输入
//     产生有符号溢出 UB —— 例如若评测数据意外含 n=13，long long 结果 6749977113 仍是
//     精确值，而 int 版会溢出成垃圾值。二者在 n<=12 时输出完全相同（12! = 479001600，
//     S = 522956313 < 2^31-1），因此这一选择不影响本题任何合法输入的判定。
//   * 输入按 long long 读入，兼容前导零 / 正号 / 任意前后空白（评测数据统一为 `n\n`）。
#include <cstdio>

int main() {
    long long n;
    if (scanf("%lld", &n) != 1) return 0;  // 无输入（空文件）时安全退出

    long long term = 1;  // term：当前项 i!
    long long sum = 0;   // sum：1! + 2! + ... + i!
    for (long long i = 1; i <= n; ++i) {
        term *= i;   // 本轮结束后 term = i!
        sum += term; // 累加 i!
    }

    printf("%lld\n", sum);
    return 0;
}
