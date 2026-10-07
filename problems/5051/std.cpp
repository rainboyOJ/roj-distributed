// 一本通 2049《【例5.19】字符串判等》（目标 ROJ 题号 5051）标程
//
// 题意：输入两行字符串（每行只由大小写字母和空格组成），在「忽略大小写、忽略空格」
//       的语义下判断两者是否相等；相等输出 YES，否则输出 NO。
//       即：把每行做「删去所有空格 + 大写字母转小写」后比较，相同则 YES。
//
// 输入输出：stdin -> stdout，两行输入，一行 YES/NO 输出。
//
// 参考来源（均已用 curl 实取正文逐行核对，本文件为改写实现，非盲抄）：
//   [1] 官方 OJ 页《2049：【例5.19】字符串判等》（题面/样例/限制 1000 ms / 65536 KB 的唯一权威口径）
//       http://ybt.ssoier.cn:8088/problem_show.php?pid=2049
//       —— 题面原文未给出字符串长度上限；同题面在计蒜客 T1115 的版本给出「字符串长度不超过 100」，
//          且全部网络 AC 代码的字符数组都开 105 / 256 / 1000，本包据此按每行 <= 100 字符造数据
//          （依据链见 gen-report.md 风险点 1）。
//   [2] 博客园《2049：【例5.19】字符串判等》
//       https://www.cnblogs.com/zheng1945/p/16343940.html
//       —— 参考代码：getline 读两行；循环 while(s1[i]==' ') s1.erase(i,1); 删空格；
//          自写 strlwr 把 'A'..'Z' 减 'A' 加 'a' 转小写；最后 if(s1==s2) YES else NO。
//   [3] CSDN《信息学奥赛一本通 2049：【例5.19】字符串判等》（双指针 / 转化字符串两种解法）
//       https://blog.csdn.net/lq1990717/article/details/122445181
//       （原站对本网络环境返回 TLS 错误，经 Wayback 快照实取正文核对：
//        http://web.archive.org/web/20250721220602/https://blog.csdn.net/lq1990717/article/details/122445181）
//       —— 解法 2「转化字符串而后比较」：把 s1、s2 各自原地压缩成「只含小写字母、无空格」的串
//          （大写 +32 变小写，空格跳过），再 strcmp。本标程采用的正是这一思路。
//   [4] CSDN《【信息学奥赛一本通】2049：【例5.19】字符串判等》
//       https://blog.csdn.net/sy820413/article/details/133960350
//       （Wayback：http://web.archive.org/web/20250721220609/https://blog.csdn.net/sy820413/article/details/133960350）
//       —— 双指针写法 char s1[105], s2[105]; 用 cin.getline 读入，跳过空格、按
//          s1[i]==s2[j] || s1[i]==s2[j]+32 || s1[i]+32==s2[j] 判同字母。与 [3] 结论一致。
//   [5] CSDN《一本通-2049：【例5.19】字符串判等》
//       https://blog.csdn.net/m0_61990249/article/details/136157703
//       （Wayback：http://web.archive.org/web/20250721220611/https://blog.csdn.net/m0_61990249/article/details/136157703）
//       —— getline 读入；'A'..'Z' 加 32 转小写；拼接时 if(c!=' ') 跳过空格；最后 str1==str2。
//   [6] CSDN《【信息学奥赛】2049：【例5.19】字符串判等》
//       https://blog.csdn.net/qq_43779149/article/details/129216058
//       （Wayback：http://web.archive.org/web/20250721220607/https://blog.csdn.net/qq_43779149/article/details/129216058）
//       —— char s1[256]; fgets 读入；同一循环里「大写 +32」并「非空格才转存」，再 strcmp。
//   [7] CSDN《字符串的判定：判断两个由大小写字母和空格组成的字符串…》（同题面、计蒜客 T1115 口径）
//       https://blog.csdn.net/chengminyang/article/details/112986841
//       （Wayback：http://web.archive.org/web/20250404072037/https://blog.csdn.net/ChengMinYang/article/details/112986841）
//       —— 唯一一处给出范围声明的同题面版本：「字符串长度不超过 100」；本包数据长度上限即取 100。
//   七个来源在算法上完全一致（忽略空格 + 折叠大小写后比较，输出 YES/NO），没有任何冲突；
//   题面【提示】仅说明本评测系统（Linux）不支持 strupr/strlwr，属实现注意而非歧义。
//
// 本标程相对来源的改写点：
//   - 不落字符数组、不设行缓冲：用 getchar() 逐字符读入，边读边「丢空格 + 转小写」，
//     直接压进 std::string 后再比较；因此没有 [3][4] 那种 char s1[105] 的硬上界，
//     行长为任意值都正确（本包数据仍按 <=100 造，见 [1][7]）。
//   - 顺手忽略 '\r'：兼容 CRLF 行尾（Windows 记事本保存的输入），不影响任何 LF 输入。
//   - 输出用 printf（对齐 problems/1000/std.cpp 的 cstdio 风格），末行带换行。
//
// 复杂度：O(L1+L2) 时间（L 为两行长度），额外空间 O(L1+L2)。

#include <cstdio>
#include <string>

// 读取一行，返回「删去所有空格 + 大写字母转小写」后的规范串。
// 换行结束该行；若先遇 EOF 也返回已读到的内容（空串表示空行/空输入）。
static std::string readNormalizedLine() {
    std::string s;
    int c;
    while ((c = getchar()) != EOF) {
        if (c == '\n') break;
        if (c == '\r') continue;             // 兼容 CRLF
        if (c == ' ') continue;              // 忽略空格
        if (c >= 'A' && c <= 'Z') c += 32;   // 忽略大小写：统一转小写
        s.push_back(static_cast<char>(c));
    }
    return s;
}

int main() {
    std::string a = readNormalizedLine();
    std::string b = readNormalizedLine();
    printf("%s\n", a == b ? "YES" : "NO");
    return 0;
}
