// 一本通 2073《【例2.16】三角形面积》（目标 ROJ 题号 5074）标程
//
// 题意：给定三角形三边 a、b、c，用海伦公式求面积：
//         p = (a + b + c) / 2
//         s = sqrt( p * (p-a) * (p-b) * (p-c) )
//       单组输入（一行三个数），输出面积，保留 3 位小数（题面【输出】原文）。
//
// 参考来源（均为网络 C++/C 题解，已联网取回原文、本机编译并按题面样例验证后改写，
// 非盲抄）：
//   1. https://blog.csdn.net/lq1990717/article/details/120655703
//      《信息学奥赛一本通 2073：【例2.16 】三角形面积》（君义NOIP）
//      给两解：(a) cin >> a >> b >> c; p=(a+b+c)/2;
//                    cout << fixed << setprecision(3) << sqrt(p*(p-a)*(p-b)*(p-c));
//               (b) scanf("%lf %lf %lf", &a,&b,&c); p=(a+b+c)/2;
//                    printf("%.3f", sqrt(p*(p-a)*(p-b)*(p-c)));
//      并点明本题考点：算术应用题 + 海伦公式 + "输出浮点数保留 x 位小数" +
//      引入 <cmath> 调用 double sqrt(double)。
//   2. https://blog.csdn.net/flower_vegetable/article/details/118996456
//      《信息学奥赛一本通-2073：【例2.16 】三角形面积》
//      参考代码：double a,b,c; scanf("%lf%lf%lf",&a,&b,&c);
//                double p=(a+b+c)/2; printf("%.3f", sqrt(p*(p-a)*(p-b)*(p-c)));
//      —— 与来源 1(b) 同思路同写法。
//   3. https://blog.csdn.net/lvcheng0309/article/details/118051534
//      《信息学奥赛一本通（2073：【例2.16 】三角形面积）》
//      参考代码（C）：double a,b,c,p,s; scanf("%lf%lf%lf",&a,&b,&c);
//                     p=(a+b+c)/2; s=sqrt(p*(p-a)*(p-b)*(p-c)); printf("%.3lf\n",s);
//      —— 增加行末换行，与仓库 1000/2071 等题的输出惯例一致。
//   4. https://blog.csdn.net/qq214936qq/article/details/136426718
//      《信息学奥赛一本通 2073：【例2.16 】三角形面积》
//      参考代码：同上的 scanf/printf 版（printf("%.3f", ...)），交叉印证。
//   官方题面（核对输入输出格式、样例与 1000 ms / 65536 KB 限制）：
//   http://ybt.ssoier.cn:8088/problem_show.php?pid=2073
//     题面样例：输入 2.1 3.1 4.1 -> 输出 3.179；题面**未声明**三边的取值范围
//     与小数位数（本包据此自定工作范围，见 data.py 头部注释）。
//
// 来源一致性核查：4 个可读来源的公式完全一致（海伦公式 + 保留 3 位小数），
// 与官方题面一致，**无冲突、无歧义**，故继续。
//
// 实现说明（本标程相对来源的改写点）：
//   * 读入用 double（scanf "%lf"，兼容整数与小数形式的边长，与全部来源一致），
//     stdin -> stdout，scanf/printf 风格参考 problems/1000/std.cpp。
//   * **零附近归一化（防御性，防 -0.00 / nan）**：题面给的是三角形的三边长，
//     但当输入退化（a+b==c，如 1 2 3）或极端接近退化时，double 下
//     p*(p-a)*(p-b)*(p-c) 可能因舍入得到 -0.0、极小负数或 NaN，直接开方会输出
//     "-0.000" 或 "nan"。这里在开方前做 `if (!(s2 > 0.0)) s2 = 0.0;`：
//     仅把 ≤0 / -0.0 / NaN 归零，正数原样保留。本题自定数据域内（0.1 <= a,b,c
//     <= 1000.0，一位小数，满足严格三角不等式）最小非退化面积为 0.00433
//     （0.1 0.1 0.1），远大于浮点噪声，故归一化不会误伤合法答案。
//   * 输出 printf("%.3f\n")：3 位小数、行末一个换行，与题面样例 `3.179` 一致。
//
// 复杂度：O(1)（一次乘法链 + 一次开方 + 一次格式化输出），
// 时限 1000 ms / 内存 64 MB 无任何压力。

#include <cstdio>
#include <cmath>

int main() {
    double a, b, c;
    if (scanf("%lf %lf %lf", &a, &b, &c) != 3) return 0;

    double p = (a + b + c) / 2.0;           // 半周长
    double s2 = p * (p - a) * (p - b) * (p - c);  // 海伦公式的被开方项
    if (!(s2 > 0.0)) s2 = 0.0;              // 防御：-0.0 / 极小负数 / NaN 一律归零

    printf("%.3f\n", sqrt(s2));             // 保留 3 位小数（题面要求）
    return 0;
}
