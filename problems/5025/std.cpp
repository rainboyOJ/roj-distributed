// 一本通 2023《【例4.8】数据统计》（目标 ROJ 题号 5025）标程
//
// 题意（题面 content.md，已在官方 OJ 页核对）：
//   输入一行若干个整数（题面【提示】：数据个数不超过 100；
//   题目描述：输入保证这些数都是不超过 1000 的整数）。
//   输出一行：最小值、最大值、平均值（保留 3 位小数），空格分隔。
//   样例：输入 `1 2 3` -> 输出 `1 3 2.000`。
//   限制：1000 ms / 65536 KB（config.json 记 time 1000 / memory 64MB）。
//
// 参考来源（均经 curl 联网取回正文与代码块、本机编译并按题面样例验证后改写，非盲抄）：
//   1. https://blog.csdn.net/lq1990717/article/details/120893399
//      《信息学奥赛一本通 2023：【例4.8】数据统计》（君义_noip）
//      解法：`int a, sum=0, n=0, mx=0, mn=1001;`
//            `while (cin >> a) { if(a>mx) mx=a; if(a<mn) mn=a; sum+=a; n++; }`
//            `cout << mn << ' ' << mx << ' '; cout << fixed << setprecision(3) << (double)sum/n;`
//      并点明本题考点：while 循环 + 「输入不确定个数的数字」(cin 流在无输入时返回 false)。
//   2. https://blog.csdn.net/2301_79128218/article/details/140647149
//      《2023：【例4.8】数据统计》（悬垂指针delete ptr；*ptr；）
//      C 语言版：`int min=10000, max=-10000; double sum=0;`
//                `while (scanf("%d", &x) != -1) { if(x<min) min=x; if(x>max) max=x; sum+=x; n++; }`
//                `printf("%d %d %.3lf", min, max, ave);`
//      并明确「sum/n 需强制转换以避免整数除法」。
//   3. https://blog.csdn.net/jhgcjw/article/details/122564653
//      《C++语言基础——C++一本通：第四章 循环结构的程序设计…2023：【例4.8】数据统计》
//      `#define INF 0x3f3f3f3f`，`int a,i=0,max=-INF,min=INF,sum=0;`
//      `while(scanf("%d",&a)!=EOF){ ... } avg=(double)sum/i; printf("%d %d %.3lf\n",min,max,avg);`
//   4. https://blog.csdn.net/google20/article/details/127712753
//      《一本通2023：【例4.8】数据统计C语言解法》
//      `int n=0,min=10000,max=-10000; ... while (scanf("%d",&x)!=-1) {...} printf("%d %d %.3lf",min,max,ave);`
//   5. https://blog.csdn.net/shanchuan2012/article/details/56925154
//      《算法竞赛入门经典 ch2_ex_2_5 最小值、最大值和平均值》（本题原始出处，同一题目，
//      书内样例 `2 8 3 5 1 7 3 6` -> `1 8 4.375`）：
//      `int x, n=0, min=INF, max=-INF, s=0; while (scanf("%d",&x)==1) { s+=x; if(x<min) min=x;
//       if(x>max) max=x; n++; } printf("%d %d %.3f\n", min, max, (double)s/n);`
//   官方题面（核对输入输出格式、样例与 1000 ms / 65536 KB 限制）：
//      http://ybt.ssoier.cn:8088/problem_show.php?pid=2023
//
// 来源一致性核查：5 个可读来源的算法完全一致——读入直到 EOF，边读边维护
//   min / max / sum / count，最后输出 `min max %.3f(sum/n)`；只有实现风格不同
//   （cin vs scanf、min/max 初值 1001/0 vs 10000/-10000 vs ±INF、%.3lf vs %.3f）。
//   结论无冲突；唯一语义含糊处是题面只声明上界（「不超过 1000」）未声明下界，
//   处理方式见下。样例 `1 2 3` 按各来源算法均得 `1 3 2.000`，与题面一致。
//
// 本标程相对来源的改写点（防御性增强，不改变题面语义）：
//   * 初值统一用 INT_MAX / INT_MIN（来源 3、5 的 INF 写法），**不采用**来源 1 的
//     `mn=1001, mx=0` / 来源 2、4 的 `min=10000, max=-10000`——那些初值依赖
//     「数据均非负且 <= 1000」这一题面未明写的假设，一旦数据含 0 以外的小值/负值
//     就会给出错误的 min/max。采用 ±INF 后对任意 int 输入都正确。
//   * sum 用 long long（本题 n<=100、值<=1000，sum<=100000，int 也够；用 long long
//     是为避免将来上游放宽范围时在 `sum += x` 处静默溢出）。
//   * 求平均改成显式 `(double)sum / n`（与来源 2 强调的「避免整数除法」一致）。
//   * 输出用 printf("%d %d %.3f\n", ...)：与全部来源的格式一致（题面样例
//     `1 3 2.000`），行末换行与仓库 1000/2071 等题的输出惯例一致。
//   * 空输入防御：题面「一行，若干个整数」+「数据个数不超过 100」意味着至少 1 个数；
//     若真遇到空文件（EOF 立刻返回），直接不输出，避免 0 除。
//
// 复杂度：O(数据个数)（读一遍、常数空间），对 1000 ms / 64 MB 无压力。

#include <cstdio>
#include <climits>

int main() {
    long long sum = 0;          // 和（long long 防御性，见头部说明）
    int n = 0;                  // 数据个数
    int mn = INT_MAX;           // 最小值：初值取 int 上界，见头部说明
    int mx = INT_MIN;           // 最大值：初值取 int 下界
    int x;

    while (scanf("%d", &x) == 1) {   // 读入直到 EOF
        if (x < mn) mn = x;
        if (x > mx) mx = x;
        sum += x;
        n++;
    }

    if (n == 0) return 0;       // 空输入的防御分支（题面保证至少一个整数）

    printf("%d %d %.3f\n", mn, mx, (double)sum / n);  // 保留 3 位小数（题面【输出】）
    return 0;
}
