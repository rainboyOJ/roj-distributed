// 一本通 2050《【例5.20】字串包含》标程（C++17，stdin -> stdout）
//
// 参考来源（本文件为改写实现，未逐字照抄任何一份来源；来源之间结论一致，
// 与题面冲突时以题面为准 —— 经核对无冲突）：
//   1. https://blog.csdn.net/lq1990717/article/details/122518206
//      《信息学奥赛一本通 2050：【例5.20】字串包含 | OpenJudge NOI 1.17 19:字符串移位包含问题》
//      —— 给出两条路线：(解法1) 显式枚举循环移位 + 逐字符比较子串；
//         (解法2) 构造新字符串（s1 += s1 等价于环形展开）后用 find/strstr 判断子串。
//         并明确「先让 s1 是较长的字符串，s2 是较短的字符串」（长度约束），本标程采用解法2。
//   2. https://blog.csdn.net/2402_84298973/article/details/146304062
//      《字串包含（信息学奥赛一本通-2050）》—— 同思路：if (s1.size() < s2.size()) swap(s1,s2);
//      s1 += s1; if (s1.find(s2) != -1) "true" else "false"；交叉印证「长者作容器 + 倍长查子串」。
//   3. https://blog.csdn.net/lvcheng0309/article/details/117331852
//      《信息学奥赛一本通（2050：【例5.20】字串包含）》—— C 语言版（字符数组 + 手工移位/strstr），
//      印证输出语义 true/false 与样例；算法同上。
//   4. 官方题面（用于核对语义/限制）：http://ybt.ssoier.cn:8088/problem_show.php?pid=2050
//      （实抓核对：时间 1000 ms / 内存 65536 KB，与 config.json 一致）
//
// 题意：一次循环移位 = 把首字符移到末尾。判定「其中一个字符串是否是另一字符串
//       经过若干次循环移位后的新串的子串」，是则输出 true，否则 false。
//
// 关键点（长度约束）：某字符串 X 的任意循环移位串的长度恒为 |X|，
//   因此若 |Y| > |X|，Y 绝不可能是 X 的移位串的子串；此时只可能 X 是 Y 的移位串的子串。
//   故先令 s1 = 较长者、s2 = 较短者，问题化为「s2 是否为 s1 某个循环移位的子串」。
//   而长度不超过 |s1| 的「某个循环移位的子串」的全体，恰为 s1+s1 的所有长度 |s2| 的子串，
//   于是只需判断 s2 是否为 s1+s1 的子串。
//   注意：不能无条件地同时检查 (s2 是 s1+s1 子串) 与 (s1 是 s2+s2 子串)，
//   那样在 |s2| > |s1| 且 s2 恰好跨越 s1 的两个周期片段时会假阳性
//   （例：s1="aba", s2="baab" 题面语义应为 false）。这是本题最常见的错解陷阱。
//
// 复杂度：O(|s1| * |s2|) 一趟子串匹配，|s| <= 30，可忽略不计。
//
// 本文件的改写点：
//   - 用 scanf/printf（仓库 problems/1000/std.cpp 风格）替代来源的 cin/cout；
//   - 用 std::string + 手写朴素匹配（不依赖 std::string::find 的库实现细节），
//     并提供长度防御（输入超长也不越界）；
//   - 显式写明「长者作容器」的长度约束与错解陷阱。

#include <cstdio>
#include <cstring>
#include <string>
#include <algorithm>

// 朴素子串匹配：返回 needle 在 hay 中首次出现的下标，未找到返回 -1。
// 与 std::string::find 语义一致，但实现独立，便于与 work/brute.cpp 交叉验证。
static int naive_find(const std::string &hay, const std::string &needle) {
    const int n = (int)hay.size();
    const int m = (int)needle.size();
    if (m == 0) return 0;                 // 空串视为任意位置匹配（本数据不出现，仅作防御）
    if (m > n) return -1;
    for (int i = 0; i + m <= n; ++i) {
        int j = 0;
        while (j < m && hay[i + j] == needle[j]) ++j;
        if (j == m) return i;
    }
    return -1;
}

int main() {
    char buf1[4096], buf2[4096];
    // 题面：一行两个字符串，单个空格隔开，仅含字母和数字，长度不超过 30。
    if (scanf("%4095s %4095s", buf1, buf2) != 2) return 0;   // 空输入/缺参：安静退出

    std::string s1(buf1), s2(buf2);
    if (s1.size() < s2.size()) std::swap(s1, s2);            // 长者作容器（长度约束，见文件头）

    const std::string doubled = s1 + s1;                     // 环形展开：所有移位串的子串来源
    if (naive_find(doubled, s2) >= 0)
        printf("true\n");
    else
        printf("false\n");
    return 0;
}
