// 一本通 2020：【例4.5】第几项（目标 ROJ 题号 5022）
//
// 题意：对正整数 n, m，求 s = 1 + 2 + 3 + ... + n，当加到第几项（最小的 n）时 s 的值超过 m？
//       输入 m；输出 n。数据范围：1 <= m <= 40000。
//       例：m = 1000 -> n = 45（S_44 = 990 <= 1000 < 1035 = S_45）。
//
// 解法（网络来源，已改写，非盲抄）：
//   [1] https://blog.csdn.net/lq1990717/article/details/116675502
//       《信息学奥赛一本通 2020：【例4.5】第几项》（君义NOIP）
//       解法1：不断 i++、sum += i，直到 sum > m（while 循环）后输出 i；
//       解法2：for(i = 1; sum <= m; ++i) sum += i; 输出 i-1。
//   [2] https://blog.csdn.net/2402_84298973/article/details/145050742
//       《第几项（信息学奥赛一本通-2020）》：while(s <= m){ s += n; n++; } 输出 --n。
//   [3] https://blog.csdn.net/2301_79128218/article/details/138002149
//       《2020：【例4.5】第几项》：while(s <= m){ ++n; s += n; } 输出 n。
//   三个来源结论完全一致：累加到「首次严格大于 m」时的项数即为答案（注意是
//   `sum <= m` 继续加，而不是 `sum < m`；m = 1000 时若写成 sum < m 会输出 44，与样例不符）。
//   本题 m <= 40000，S_283 = 40186 已是最大项数，循环次数 <= 283，O(sqrt(m)) 且常数极小。
//
// 本标程相对来源的改写点：
//   - 统一为 stdin -> stdout 的 scanf/printf 风格（参考 problems/1000/std.cpp）；
//   - 用 long long 存储 sum（防未来扩大范围时溢出，本题 int 亦足够），n 为 long long；
//   - 写成「先判断、再加」的清晰形式，避免来源解法2中 i-1 这类易错的修正；
//   - 答案恒 >= 2（m >= 1 时 S_1 = 1 不超过任何合法 m），无需特判。
#include <cstdio>

int main() {
    long long m;
    if (scanf("%lld", &m) != 1) return 0;  // 按题意 m 必有输入；读失败直接退出

    long long sum = 0;  // s = 1 + 2 + ... + n
    long long n = 0;    // 当前已加的项数
    while (sum <= m) {  // 尚未「超过」m，继续加下一项
        ++n;
        sum += n;
    }
    printf("%lld\n", n);
    return 0;
}
