// 一本通 2058《【例3.10】简单计算器》 标程（C++17，stdin -> stdout）
// ---------------------------------------------------------------------------
// 题意：一行输入「第一个数 第二个数 运算符」，运算符 ∈ {+, -, *, /}，
//       输出表达式结果；除数为 0 输出 "Divided by zero!"，
//       运算符非法（不为 + - * / 之一）输出 "Invalid operator!"。
//       题面【提示】给出的样例 2 为 "2 1.2 -" -> "0.8"，说明操作数可以是小数，
//       故按 double 读入；结果用 C 的 %g（6 位有效数字、去尾随零、整数不带小数点）
//       输出，与题面样例 "34 56 +" -> "90"、"2 1.2 -" -> "0.8" 完全一致。
//
// 参考来源（网络检索后改写，未逐字复制任何一份代码）：
//   [1] 官方题面（含样例 2 与 1000 ms / 65536 KB 限制）
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2058
//   [2] 信息学奥赛一本通 2058：【例3.10】简单计算器
//       https://blog.csdn.net/lq1990717/article/details/120770435
//       （double 读入 + switch 分派；除数为 0 特判，default 分支输出 Invalid operator!）
//   [3] 【2058】简单计算器
//       https://blog.csdn.net/lwx3289765163/article/details/120990410
//       （同上，switch + 除零特判）
//   [4] 2058：【例3.10】简单计算器
//       https://blog.csdn.net/2301_79128218/article/details/132249347
//       （double 读入；case '/' 内先判 b==0 再算）
//   [5] 一本通2058：【例3.10】简单计算器
//       https://blog.csdn.net/tflstjs/article/details/119983906
//       （double 读入；先判断 (b==0 && op=='/') 再分派）
//
// 契约（与上述来源一致，也即本包数据的判定约定）：
//   - 结果按 6 位有效数字打印、去掉无意义的尾随零与小数字符点，
//     等价于 C++ 默认 ostream 输出 / printf("%g")；
//   - 除数为 0 优先于运算符合法性判断（op=='/' 且 b==0 -> Divided by zero!）；
//   - 运算符非法时不进行任何数值运算。
#include <cstdio>

int main() {
    double a = 0.0, b = 0.0;
    char op = 0;  // 与各参考实现一致：运算符只取一个字符（char c; cin >> c;）
    if (scanf("%lf %lf %c", &a, &b, &op) != 3) return 0;  // 格式串空格跳过前导空白

    switch (op) {
        case '+':
            printf("%g\n", a + b);
            break;
        case '-':
            printf("%g\n", a - b);
            break;
        case '*':
            printf("%g\n", a * b);
            break;
        case '/':
            if (b == 0.0) {
                printf("Divided by zero!\n");
            } else {
                printf("%g\n", a / b);
            }
            break;
        default:
            printf("Invalid operator!\n");
            break;
    }
    return 0;
}
