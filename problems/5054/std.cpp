// 一本通 2052《【例3.2】范围判断》（目标 ROJ 题号 5054）标程
//
// 题意（.ybt-import/staging/2052/content.md）：
//   读入一个整数 a；若 a > 1 并且 a < 100，则输出 yes；否则不输出任何内容。
//   区间是开区间 (1, 100)，即 a ∈ {2, 3, ..., 99} 时输出 yes。
//
// 参考来源（网络题解 / AC 代码，均已被改写，未盲抄；本标程为本包自写）：
//   1. https://blog.csdn.net/lq1990717/article/details/120656293
//      《信息学奥赛一本通 2052：【例3.2】范围判断》
//      给出两解：if (a > 1 && a < 100) cout << "yes";
//                 cout << (a > 1 && a < 100 ? "yes" : "");
//      并指出「不能写为 1<a<=100，必须写为 a > 1 && a < 100」。
//      （注：该文【解题思路】散文里有一处笔误写成「小于等于 100」，
//       但其两段代码均为 a < 100，与题面「小于100」一致，以题面为准。）
//   2. https://blog.csdn.net/tflstjs/article/details/119881881
//      《一本通2052：【例3.2】范围判断》：if(a>1&&a<100) cout<<"yes";
//   3. https://blog.csdn.net/ffsdfg/article/details/127190531
//      《信息学奥赛一本通：2052：【例3.2】范围判断》：scanf("%d",&a); if(a>1&&a<100) printf("yes");
//   4. https://blog.csdn.net/flower_vegetable/article/details/119083450
//      《信息学奥赛一本通-2052：【例3.2】范围判断》：if(a<100&&a>1) printf("yes");
//   5. https://blog.csdn.net/mydream8/article/details/121884798
//      《信息学奥赛一本通（2052：【例3.2】范围判断）》：cin >> a; if(a>1&&a<100) cout << "yes" << endl;
//   6. https://blog.csdn.net/weixin_62460981/article/details/123670170
//      《【信息学奥赛】2052：【例3.2】范围判断（C++）》：if(i > 1 && i < 100) cout<<"yes";
//
//   官方题面（核对题意 / 限制 / 样例）：
//   http://ybt.ssoier.cn:8088/problem_show.php?pid=2052
//   时间限制 1000 ms，内存限制 65536 KB（与 config.json 一致）。
//
// 多来源结论一致：区间为开区间 (1,100)，满足时输出 yes、不满足时什么都不输出。
//
// 实现说明：
//   - 题面只说「一个整数」，未声明取值范围。按自然的有符号 32 位域自定工作范围
//     [-2147483648, 2147483647]（int 域的全区间，也是数据生成器使用的范围）。
//   - 用 long long 读写，即使评测数据超出 32 位也不会截断/溢出（保险起见）。
//   - 不满足条件时不输出任何字符（连换行也不输出），与题面「否则不输出」一致；
//     满足条件时输出 "yes" 加一个换行（忽略行末空白的评测器均可判对）。
//   - 风格参考 problems/1000/std.cpp（cstdio + scanf/printf，C++17，stdin→stdout）。
//   - 复杂度 O(1) 时间、O(1) 空间。

#include <cstdio>

int main() {
    long long a;
    if (scanf("%lld", &a) != 1) return 0;  // 无输入时不做任何输出
    if (a > 1 && a < 100) {
        printf("yes\n");
    }
    return 0;
}
