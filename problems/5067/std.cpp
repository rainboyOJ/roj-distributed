// 一本通 2066《【例2.3】买图书》标程
//
// 参考来源（网络 C++ 题解，已联网逐一核对、本机编译验证后改写）：
//   1. https://blog.csdn.net/lq1990717/article/details/119962764
//      《信息学奥赛一本通 2066：【例2.3】买图书》
//      参考代码（解法 1，cin/cout）：double n, m; cin >> n >> m;
//                          cout << fixed << setprecision(2) << n - m * 0.8;
//      参考代码（解法 2，scanf/printf）：double n, m; scanf("%lf %lf", &n, &m);
//                          printf("%.2f", n - m * 0.8);
//   2. https://blog.csdn.net/geekprand/article/details/128750231
//      《C++ 2066:买图书（史上最详细版）》
//      参考代码：int a, b; cin >> a >> b; printf("%.2f", a - b * 0.8);
//   3. https://www.cnblogs.com/bianchengmao/p/16713740.html
//      《信息学奥赛一本通—2066：【例2.3】买图书》
//      参考代码：double n, m; cout << fixed << setprecision(2) << n - (m * 0.8) << endl;
//   4. https://blog.csdn.net/cbh666888/article/details/118053383
//      《信息学奥赛一本通——2066：【例2.3】买图书》
//      参考代码：double n, m, a, b; cin >> n >> m; a = m * 0.8; b = n - a; printf("%.2lf", b);
//
// 四个来源结论完全一致：答案 = n - m * 0.8，输出保留 2 位小数。
// 题面未声明 n、m 的类型与范围；本标程按 double 读入（同时兼容整数与小数输入，
// 与来源 1/3/4 一致），即「打 8 折 = 乘 0.8，再从 n 中减去」。
//
// 【对拍发现的修正】直接 printf 计算 n - m*0.8 存在浮点符号瑕疵：当数学答案恰为 0
// （n = 0.8m，如 80 100）时，m*0.8 的舍入误差使差值为 ±4e-15 量级的小量；
// 若该误差为负，printf("%.2f") 会打印 "-0.00"（本机 Apple clang -O2 因 FMA 收缩
// 实测 80 100 -> -0.00，而该输入数学答案与 x86 无 FMA 编译结果均为 0.00）。
// 故输出前做「零附近归一化」：输入为整数或至多两位小数的金额时，答案的小数位 ≤ 3，
// 最小非零绝对值 ≥ 1e-3；在 10^6 量级上 double 的舍入误差约 1e-10，因此 |ans| < 1e-6
// 只可能来自舍入误差（数学答案为 0），归零后统一打印 "0.00"。
// 以题面样例验证：n = 100, m = 100 -> 100 - 80 = 20.00，与【输出样例】一致。
#include <cstdio>
#include <cmath>

int main() {
    double n, m;
    scanf("%lf %lf", &n, &m);  // 小明的钱 n 元、书原价 m 元
    double ans = n - m * 0.8;  // 8 折后书价 m*0.8，剩余金额
    if (fabs(ans) < 1e-6) ans = 0.0;  // 零附近归一化：消除 "-0.00" 与极小正噪声
    printf("%.2f\n", ans);            // 保留 2 位小数
    return 0;
}
