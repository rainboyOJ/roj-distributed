// 一本通 2065《【例2.2】整数的和》（目标 ROJ 题号 5066）标程
//
// 题意：输入 a、b、c 这 3 个整数，输出它们的和（单组输入：一行三个整数）。
//
// 参考来源（本题的 C++ 题解 / AC 代码，均已被下方改写，未盲抄）：
//   1. https://blog.csdn.net/lq1990717/article/details/119843652
//      《信息学奥赛一本通 2065：【例2.2】整数的和》
//      给出两解：cin >> a >> b >> c; cout << a + b + c;
//                 scanf("%d %d %d", &a, &b, &c); printf("%d", a + b + c);
//   2. https://blog.csdn.net/zjx120307/article/details/126077791
//      《信息学奥赛一本通——2065：【例2.2】整数的和》
//      d = a + b + c; cout << d;
//   3. https://blog.csdn.net/qiaoweichen/article/details/119653980
//      《信息学奥赛一本通题库2065 【例2.2】整数的和》：思路同上（输入三数再求和）。
//   4. 官方题面（题目描述/输入/输出/样例，未声明数据范围）
//      http://ybt.ssoier.cn:8088/problem_show.php?pid=2065
//
// 说明：题面只说“整数”，未声明取值范围；上面各来源均用 int 读写。
// 本标程按题面“3 个整数直接相加”的语义改写为 long long（scanf/printf，
// 风格参考 problems/1000/std.cpp），即使 a+b+c 超出 32 位也不会溢出，
// 输出仅一个整数加换行，与所有来源结论一致。
//
// 复杂度：O(1)（一次加法 + 常数次 I/O）。

#include <cstdio>

int main() {
    long long a, b, c;
    scanf("%lld %lld %lld", &a, &b, &c);
    printf("%lld\n", a + b + c);
    return 0;
}
