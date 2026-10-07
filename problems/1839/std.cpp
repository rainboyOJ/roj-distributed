// 一本通 1839《【05NOIP提高组】谁拿了最多奖学金》标程（C++17，stdin -> stdout）
//
// ===================== 参考来源（联网检索 + 按题面改写，非盲抄）=====================
// 检索入口：CSDN 站内搜索 API
//   https://so.csdn.net/api/v3/search?q=一本通 1839 谁拿了最多奖学金
//   （原始响应存 work/sources/csdn_search_1839.json，命中共 63 条）
// 官方题面（与 content.md 逐字核对，1000 ms / 65536 KB）：
//   http://ybt.ssoier.cn:8088/problem_show.php?pid=1839
// 同题交叉印证（NOIP2005 提高组第一题，题面逐字相同，1000ms / 65536kB）：
//   http://noi.openjudge.cn/ch0109/04/
// 参考解法（正文抽取件存 work/sources/，算法完全一致，无结论冲突）：
//   [1] https://blog.csdn.net/u014117969/article/details/136336073
//       《信息学奥赛一本通：1839：【05NOIP提高组】谁拿了最多奖学金》
//       给出 scanf 版与 cin 版两份参考程序：逐条件累加奖金、`if (tmp > max)` 扫描取最大值。
//   [2] https://blog.csdn.net/hybridcow_horse/article/details/123533452
//       同题逐条件累加写法（max 初值 -1）。
//   [3] https://blog.csdn.net/m0_63954165/article/details/124025989
//       逐条件累加写法（字符串 stoi 解析变体）。
//   [4] https://blog.csdn.net/sy820413/article/details/133972018
//       逐条件累加写法。
//   [5] https://blog.csdn.net/strawberrytreea/article/details/126362069
//       面向对象（class student）逐条件累加写法。
//   [6] https://blog.csdn.net/2402_84298973/article/details/146396263
//       结构体数组写法。
//   [7] https://blog.csdn.net/qq_45083002/article/details/132449439
//       逐条件累加写法。
//   [8] https://blog.csdn.net/lq1990717/article/details/122518654
//       多数组/结构体两种写法，并明确说明并列取先出现的最大值下标（`money[i] > money[mxi]`）。
//   [9] https://blog.csdn.net/lvcheng0309/article/details/117333673
//   [10] https://blog.csdn.net/2301_80084031/article/details/135776930
//       逐条件累加写法。
//
// 各来源算法一致：五项规定逐条判定、严格大于（>80 / >85 / >90），奖金累加；
// 扫描取"奖金总数最大"者，并列时取输入中最早出现者（题面第二段明文规定）。
// 来源全用 bits/stdc++.h（本机 Apple clang 不可用），本标程改为标准头、自写实现。
//
// ============================== 题意与关键判读 ==============================
// 一、每名学生可同时获得多项奖学金（题面明文，例：姚林 87/82/干部 → 4000+850=4850），
//     故「同名多奖项」不构成歧义：五项条件各自独立累加，获奖人数不限。
// 二、并列总分：题面明文「如果有两位或两位以上的学生获得的奖金最多，输出他们之中在输入
//     文件中出现最早的学生的姓名」。本标程用严格 `>` 前向扫描实现该裁定（先出现者先占有，
//     相等不覆盖）。
// 三、题面「假设总有同学能满足获得奖学金的条件」意味着正常输入下 max>0。若出现
//     五条件全不满足的退化输入（全零，题面保证之外），按并列裁定推广：所有学生同以 0 元
//     并列最多，输出最先出现的学生；本标程 max 初值取 -1，对该退化输入给出确定输出而非
//     未定义行为（见 gen-report.md 风险点 1）。
// 四、数据范围（题面明文）：1<=N<=100；期末平均成绩、班级评议成绩 ∈ [0,100]；
//     是否干部/是否西部 ∈ {Y,N}；论文数 ∈ [0,10]；姓名长度 1..20 的大小写英文字母。
//     单生最高奖金 = 8000+4000+2000+1000+850 = 15850，总和上界 100*15850 = 1585000，
//     int 足够；本标程用 int 累加（上下界均有断言级余量），输出精确十进制整数。
// 五、限制 time 1000 ms / memory 64 MB（config.json，与官方页一致）：算法 O(N)，常数极小。
//
// 输出格式：三行 —— 姓名 / 该生奖金总数 / N 名学生奖金总和，行末单个 '\n'。
// =============================================================================

#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;  // 无输入时安全退出

    int best_total = -1;             // -1：题面保证 N>=1；见关键判读三
    std::string best_name;
    int sum = 0;

    for (int i = 0; i < n; ++i) {
        std::string name;
        int avg;       // 期末平均成绩
        int cls;       // 班级评议成绩
        char leader;   // 是否学生干部：Y / N
        char west;     // 是否西部省份学生：Y / N
        int papers;    // 发表论文数
        std::cin >> name >> avg >> cls >> leader >> west >> papers;

        int total = 0;
        if (avg > 80 && papers >= 1) total += 8000;        // 1) 院士奖学金
        if (avg > 85 && cls > 80)   total += 4000;         // 2) 五四奖学金
        if (avg > 90)               total += 2000;         // 3) 成绩优秀奖
        if (avg > 85 && west == 'Y') total += 1000;        // 4) 西部奖学金
        if (cls > 80 && leader == 'Y') total += 850;       // 5) 班级贡献奖

        sum += total;
        if (total > best_total) {  // 严格 > ⇒ 并列时保留最早出现者
            best_total = total;
            best_name = name;
        }
    }

    std::cout << best_name << '\n' << best_total << '\n' << sum << '\n';
    return 0;
}
