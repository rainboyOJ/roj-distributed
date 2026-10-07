// 一本通 2062 【例1.3】电影票
//
// 题意：已知一位小朋友的电影票价是 10 元，输入人数 x，
//       输出「人数 总票价」，中间用一个空格隔开（总票价 = x * 10）。
// 样例：输入 2 => 输出 2 20
//
// 参考来源（网络题解，已按题面逐条核对后改写，非盲抄）：
//   https://blog.csdn.net/tflstjs/article/details/118758436   （一本通2062：【例1.3】电影票）
//   https://blog.csdn.net/qq_29887971/article/details/127192066（信息学奥赛一本通-2062 题解）
//   https://blog.csdn.net/m0_68700248/article/details/124718656（信息学奥赛一本通--2062电影票）
//   https://blog.csdn.net/zjx120307/article/details/126051926 （一本通 2062，C++/Python 双解）
//   https://blog.csdn.net/setprecisiona/article/details/128150486（2062：电影票，含格式说明）
//   https://blog.csdn.net/zhxincsdn/article/details/140589187 （[一本通 2062] 电影票，int 溢出的讨论）
//
// 来源结论核对：
//   - 全部来源的算法一致：读入 x，输出 x 与 x*10，中间一个空格；
//   - include007（https://blog.csdn.net/include007/article/details/118052751）的代码额外
//     `cout << setiosflags(ios::fixed) << setprecision(2)`，会输出 `2 20` 之外的写法风险
//     （对整数无影响，但属多余、易误导），不采用；
//   - zhxincsdn 指出 int 可能溢出、提出「末尾添 0」技巧，本题按其提示改用 long long。
//
// 自定工作范围（题面未声明 x 的范围）：1 <= x <= 1e8，此时 x*10 <= 1e9，
// 仍在 int32 安全范围内（书中 int 写法亦可 AC），long long 仅作保险。
// 输出格式严格按题面：人数 + 一个空格 + 总票价（末尾换行，OJ 忽略行末空白）。
#include <cstdio>

int main() {
    long long x;
    if (scanf("%lld", &x) != 1) return 0;  // 读入人数
    printf("%lld %lld\n", x, x * 10);      // 人数 总票价
    return 0;
}
