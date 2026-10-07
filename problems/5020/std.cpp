// 一本通 2018《【例4.3】输出奇偶数之和》标程
//
// 题意：利用 for 循环，分别输出 1~n 之间所有奇数的和、偶数的和。
//   输入：一行一个整数 n；输出：一行两个整数，偶数之和在前、奇数之和在后，用一个空格隔开。
//   数据规模：1 <= n <= 100。
//
// 参考来源（网络题解，已按题面逐条核对后改写，非盲抄）：
//   1. https://blog.csdn.net/lvcheng0309/article/details/116546508
//      《信息学奥赛一本通（2018：【例4.3】输出奇偶数之和）》——
//      给出 C 参考代码：for(i=1;i<=n;i++) if(i%2==0) s1+=i; else s2+=i;
//      并 printf("%d %d\n", s1, s2)，确认「偶数之和在前、奇数之和在后」。
//   2. https://blog.csdn.net/lq1990717/article/details/116675169
//      《信息学奥赛一本通 2018：【例4.3】输出奇偶数之和》—— C++ 写法
//      cout << sumEven << ' ' << sumOdd;（sumOdd 为奇数和、sumEven 为偶数和），顺序一致。
//   3. https://blog.csdn.net/jhgcjw/article/details/121455401
//      《C++语言基础——C++一本通：第四章 循环结构的程序设计：第一节 for语句：2018》——
//      if(i%2==0) x+=i; else y+=i; cout << x << " " << y;（x=偶数和、y=奇数和）。
//   4. https://blog.csdn.net/tflstjs/article/details/121057040
//      《一本通2018：【例4.3】输出奇偶数之和》—— 同思路的另一种 C 写法，输出顺序同上。
//   官方题目页（用于核对题面与样例）：http://ybt.ssoier.cn:8088/problem_show.php?pid=2018
//
// 各来源结论一致：输入 n，for 循环累加，先输出偶数和、再输出奇数和，中间一个空格，行末换行。
//
// 边界与溢出说明：n <= 100 时偶数和最大 2550、奇数和最大 2500，int 足够；
// 这里仍用 long long 累加，以防真实评测数据范围被放宽时（n 达到约 92682 时 n^2/4 才越过
// int32 上限 2147483647）出现整型溢出。样例 10 -> "30 25"。
#include <cstdio>

int main() {
    long long n;
    if (scanf("%lld", &n) != 1) return 0;  // 题面保证 1 <= n <= 100

    long long sumEven = 0, sumOdd = 0;  // sumEven:偶数之和, sumOdd:奇数之和
    for (long long i = 1; i <= n; ++i) {
        if (i % 2 == 0)
            sumEven += i;
        else
            sumOdd += i;
    }

    printf("%lld %lld\n", sumEven, sumOdd);
    return 0;
}
