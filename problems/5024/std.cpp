// 【一本通 2022】【例4.7】最小n值
// 题意：给定正整数 m（题面数据范围 m <= 11），求最小的正整数 n，使得
//       1 + 1/2 + 1/3 + ... + 1/n >= m。
//
// 参考来源（网络题解，已按本仓库风格改写为 C++17 stdin->stdout）：
//   [1] 信息学奥赛一本通 2022：【例4.7】最小n值 —— CSDN / lq1990717
//       https://blog.csdn.net/lq1990717/article/details/119711142
//       原思路：设部分和 s（浮点）、分母 i；while (s < m) { s += 1/i; ++i; }
//               循环退出时 s >= m，而 i 已多加 1，故答案 n = i - 1。
//   [2] 同题另解（for 循环写法，检索"一本通 2022 最小n值 题解"得到）
//       https://blog.csdn.net/mydream8/article/details/122361944
//
// 改写要点：
//   * m 按题面用整数读入（正整数），累加与比较用 double（题解强调"要做实数除法，
//     相关变量必须设为浮点型"）；
//   * 答案 n 用 long long 计数；
//   * 精度评估：m <= 11 时答案最大为 n = 33617，double 朴素累加的绝对误差量级约
//     n * eps * H_n ~ 1e-11，远小于 H_n 与整数 m 之间的最小间隙（跨过阈值时
//     差值为 1/n >= 1/33617 ~ 3e-5），因此比较不会产生误判（已用精确有理数穷举核对）。
#include <cstdio>

int main() {
    long long m;
    if (scanf("%lld", &m) != 1) return 0;  // 读入 m
    double s = 0.0;                        // 调和级数部分和 1 + 1/2 + ... + 1/i
    long long i = 1;                       // 当前分母
    while (s < m) {                        // 尚未达到 m 就继续累加下一项
        s += 1.0 / (double)i;
        ++i;
    }
    printf("%lld\n", i - 1);               // 退出时 i 多加了一次，答案为 i - 1
    return 0;
}
