// 一本通 2057《【例3.9 】星期几》—— 标程（C++17，stdin -> stdout）
// 目标 ROJ 题号 5059（落地由主控脚本完成，本包未触碰 problems/）
//
// 题意（.ybt-import/staging/2057/content.md）：
//   读入表示星期几的数字，输出对应英文名称：
//   1 -> Monday, 2 -> Tuesday, 3 -> Wednesday, 4 -> Thursday,
//   5 -> Friday, 6 -> Saturday, 7 -> Sunday；
//   其它任何输入 -> input error!（题面明文：「错误输入请输出：input error!」）
//   题面【输入样例】1 -> 【输出样例】Monday。
//   限制（config.json 与官方 OJ 页一致）：time 1000 ms / memory 65536 KB。
//
// 参考来源（本包 worker 于本轮联网逐篇抓取正文核对；所有来源解法结论一致：
//   1..7 各对应一个英文名，其余走 default/else 打印 input error!）：
//   [1] https://blog.csdn.net/lq1990717/article/details/120770285
//       《信息学奥赛一本通 2057：【例3.9 】星期几》（君义NOIP）
//       给出 switch、if…else if、string 数组三种 AC 写法；数组版为
//       `string s[8]={"","Monday",...,"Sunday"}; if(i>=1&&i<=7) cout<<s[i]; else cout<<"input error!";`
//   [2] https://www.cnblogs.com/xuchaoyue/p/16265855.html
//       《ybt 2057：【例3.9 】星期几》（博客园）—— switch 版；作者特别强调
//       「漏下了大小写」是本题易错点（英文名首字母大写、其余小写）。
//   [3] https://blog.csdn.net/flower_vegetable/article/details/119278275
//       《信息学奥赛一本通-2057：【例3.9 】星期几》—— if/else-if 链 + printf 版。
//   [4] https://blog.csdn.net/weixin_70576261/article/details/161998155
//       《【星期几】信息学奥赛一本通C语言解法（题号2057）》—— C 语言 switch + printf 版。
//   [5] https://blog.csdn.net/wdajsnhc/article/details/79349948
//       《星期数字转英文名》—— if-else-if 与 switch 两解并列，结论相同。
//   [6] https://blog.csdn.net/2301_79128218/article/details/132249294
//       《2057：【例3.9 】星期几》—— switch 版 + 思路分析（default 打印 input error!）。
//   [7] https://blog.csdn.net/2401_84500159/article/details/141091950
//       《〈2057：【例3.9 】星期几〉》—— switch 版。
//   [8] https://blog.csdn.net/tflstjs/article/details/119900829
//       《一本通2057：【例3.9 】星期几》—— if/else-if 链版。
//   [9] https://blog.csdn.net/m0_73220913/article/details/129109998
//       《信息学奥赛一本通答案dj星期几2057》—— switch 版，逐 case 注释。
//   [10] https://blog.csdn.net/lwx3289765163/article/details/120990398
//       《【2057】星期几》—— switch 版。
//   [11] https://blog.csdn.net/meterochan/article/details/135325164
//       《2057：【例3.9 】星期几 —— 信息学奥赛高级题库》—— switch 版（正文有付费墙截断，
//        可见部分与本标程结论一致，仅作交叉印证）。
//   [12] https://www.cfanz.cn/resource/detail/YvyyyoErWwrNj
//       《信息学奥赛一本通（c++）：2057：【例3.9 】星期几-CFANZ编程社区》—— switch 版。
//   官方题面（本包实测抓取，核对标题 / 限制 / 样例）：
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2057
//       时间限制 1000 ms，内存限制 65536 KB，样例 1 -> Monday
//       （本轮实抓页面：提交数 140892 / 通过数 76033；正文各节由站点清空，仅余标题与样例）。
//
// 多来源结论一致，无冲突。唯一细节差异：部分来源 cout<<...<<endl（行尾换行）、
// 部分不换行；评测忽略行末空白，本标程统一输出行尾 `\n`（语料惯例，见 problems/1000）。
//
// 本实现为本包改写（scanf/printf 风格，参考 problems/1000/std.cpp）：
//   - 用 long long 读入：是全部 int 版网络题解的严格超集（自定工作范围见 data.py），
//     域上限附近不会截断；
//   - 分支结构用「一次区间判定 + 查表」，与网络题解的 switch / if 链语义等价，
//     但把 7 个英文串集中存表、只写一遍，便于逐字核对大小写（来源 [2] 提示的易错点）；
//   - 表下标 0 位放空串，配合 1..7 的闭区间判定，任何输入都不会越界读；
//   - 1..7 之外（含 0、8、负数、超大数）一律打印 input error!（题面要求的错误提示，
//     小写 + 感叹号，逐字符比对题面）；
//   - 无输入 / 非法 token 时静默退出（不输出任何内容）；
//   - 纯整数比较，无浮点、无算术中间量，不存在溢出 / 精度风险。复杂度 O(1)。
//
// 字符级核对（题面 vs 本文件字符串，逐字对照）：
//   Monday / Tuesday / Wednesday / Thursday / Friday / Saturday / Sunday / input error!

#include <cstdio>

int main() {
    long long n;
    if (scanf("%lld", &n) != 1) return 0;  // 无输入 / 非法 token：不输出，直接退出

    // 下标 0 占位空串；1..7 分别为七个英文名（首字母大写，来源 [2] 的易错点）。
    static const char* name[8] = {
        "", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    };

    if (1 <= n && n <= 7) {
        printf("%s\n", name[n]);          // 闭区间 [1, 7]：有效输入分支
    } else {
        printf("input error!\n");         // 题面要求的错误提示（含感叹号）
    }
    return 0;
}
