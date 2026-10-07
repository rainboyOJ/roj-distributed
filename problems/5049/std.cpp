// 一本通 2047《【例5.16】过滤空格》—— 标程（C++17，stdin -> stdout）
// 目标 ROJ 题号 5049（落地由主控脚本完成，本包未触碰 problems/）
//
// 题意（.ybt-import/staging/2047/content.md，逐字摘录）：
//   【题目描述】过滤多余的空格。一个句子中也许有多个连续空格，过滤掉多余的空格，
//              只留下一个空格。
//   【输入】一行，一个字符串（长度不超过 200），句子的头和尾都没有空格。
//   【输出】过滤之后的句子。
//   【输入样例】Hello      world.This is    c language.
//   【输出样例】Hello world.This is c language.
//   限制（config.json，与官方 OJ 页一致）：time 1000 ms / memory 65536 KB。
//
// 参考来源（本包 worker 于本轮联网用 curl 逐篇实取正文核对；原始正文留存
// work/sources/*.txt，检索响应留存 work/evidence/*.json）：
//   [1] https://blog.csdn.net/lq1990717/article/details/122375442
//       君义_noip《信息学奥赛一本通 2047：【例5.16】过滤空格 | OpenJudge NOI 1.7 23:过滤多余的空格》。
//       主来源，给出五种写法（结论完全一致）：
//         解法 1（char 数组）：cin.getline(s_in,205) 后遍历，遇空格累计 bn，
//            bn==1 才写入输出数组，遇非空格把 bn 清零并照抄；
//         解法 1'（string）：同思路 + push_back；
//         解法 2：`for i<len: if s[i]==' ' bn++; else bn=0; if(s[i]!=' '||bn==1) putchar(s[i]);`
//            —— 等价于「连续空格只保留一个」；
//         解法 3（string）：`while(cin>>s) cout<<s<<' ';`
//         解法 3'（C）：`while(scanf("%s",s)!=EOF) printf("%s ",s);`
//       该文并注明解法 3/3'「输入遇空格或换行中止，用 while 循环重复输入（没有输入空格）」，
//       即「按词读取 + 词间补一个空格」的路线（输出带行尾空格，OJ 忽略行末空白）。
//       本标程采用解法 1/2 的「逐字符扫描 + 只保留每段空格的首个」路线（改写，非逐字复制）。
//   [2] https://blog.csdn.net/qq_40790042/article/details/120043459
//       《一本通：2047：【例5.16】过滤空格》。gets 读整行后
//       `for(i=0;i<len;i++) if(a[i+1]!=' '||a[i]!=' ') cout<<a[i];`
//       —— 等价形态：非空格字符恒输出，空格只在其后一位不是空格时输出（即每段留一个）。
//       本标程与该文同解，但把判据写在前向扫描里，避免读 a[len]（越界读下标 len）。
//   [3] https://blog.csdn.net/2301_80084031/article/details/135758583
//       《一本通 2047：过滤空格》。法一 getline 后
//       `if(s[i]!=' ') cout<<s[i]; else if(s[i]==' '&&s[i+1]!=' ') cout<<s[i];`（同 [2] 判据）；
//       法二 `while(cin>>s) cout<<s<<" ";`（词读取路线）。
//   [4] https://blog.csdn.net/2301_80096514/article/details/135191701
//       《2047过滤空格（C语言）》。`while((scanf("%s",s))!=EOF) printf("%s ",s);`
//       —— 纯词读取路线，靠 OJ 忽略行末空白接受行尾多余空格。
//   [5] https://blog.csdn.net/xinshuai_1/article/details/134238121
//       《c++ 信息学奥赛 2047：【例5.16】过滤空格》。`while(scanf("%s",&st)==1) printf("%s ",st);`
//   [6] https://blog.csdn.net/2402_84298973/article/details/146281833
//       《过滤空格（信息学奥赛一本通-2047）》。`while(cin>>s) cout<<s<<' ';`
//   [7] https://blog.csdn.net/a3031655208/article/details/143689054
//       《信息学奥赛一本通（c++版）2047：【例5.16】过滤空格》。getline + vector +
//       isspace/isalpha 条件写回 —— 该实现依赖「空格前一个字符是字母」，遇到
//       `a.  b`（空格前是标点）会整段丢弃空格，属脆弱实现；此处仅登记来源面，
//       本标程不采用其判据（题面只要求按「空格」过滤，不涉及字符类别）。
//   [8] https://blog.csdn.net/sy820413/article/details/133872127
//       《【信息学奥赛一本通】2047：【例5.16】过滤空格》—— 付费墙截断，正文仅题目描述
//       （时间限制 1000 ms / 内存限制 65536 KB / 提交数 34396 / 通过数 22068），仅作题面印证。
//   [9] https://blog.csdn.net/ffsdfg/article/details/127631960
//       《信息学奥赛一本通：2047：【例5.16】过滤空格》—— 「关注即可阅读」截断，
//       可见部分仅题面（时间限制 1000 ms / 内存限制 65536 KB / 提交数 20053 / 通过数 12693），
//       仅作题面与限制的交叉印证。
//   [10] https://blog.csdn.net/m0_73220913/article/details/129599969
//        《信息学奥赛一本通答案dj过滤空格2047》—— 同样被截断，无可见代码，仅作来源面登记。
//   [11] 官方题面页（本轮实抓，留存 work/evidence/ybt2047_official_page.html）：
//        http://ybt.ssoier.cn:8088/problem_show.php?pid=2047
//        标题「2047：【例5.16】过滤空格」，时间限制 1000 ms、内存限制 65536 KB、
//        提交数 76430 / 通过数 51003；正文各节被站点清空，仅余标题、限制与两组样例
//        （样例与 content.md 逐字节一致）。
//   [12] OpenJudge NOI 同题（本轮实抓，留存 work/evidence/openjudge_noi_1_7_23.html）：
//        http://noi.openjudge.cn/ch0107/23/ 「23:过滤多余的空格」，
//        总时间限制 1000ms、内存限制 65536kB，描述/输入/输出/样例与 content.md 逐字一致
//        （说明本题是 OpenJudge NOI 1.7 第 23 题的一本通收录版）。
//
// 多来源结论核对（无冲突）：所有可读来源的算法语义一致 —— 把每个「连续空格段」压缩成
//   一个空格，非空格字符原样保留；差异仅在实现路线（逐字符扫描 vs 按词读取）与
//   输出是否带行尾空格（按词读取类的 `cout<<s<<' '` 带行尾空格，被 OJ 因忽略行末空白接受）。
//   题面无歧义：头尾无空格已由题面保证，故「逐字符扫描」与「按词重排」在合法数据上输出相同。
//   题面唯一未明说的是「输出是否以换行结束」——全部来源均带行尾（endl / 行尾空格 + 换行），
//   本标程统一输出行尾 `\n`（仓库惯例，见 problems/1000），行末空白评测忽略。
//
// 本标程相对来源的改写点：
//   * 输入用 `fgets` 读**整行**，先剥行尾 '\n'/'\r'（CRLF 容错，来源均未处理）；
//   * 判定用「前向跳段扫描」：遇到一个空格段就整段跳过，仅当段后还有内容且已输出过
//     非空内容时才补一个空格。与来源 [2]/[3] 的「看后一位」判据语义等价，但不做任何
//     越界下标访问（来源 [2] 读 a[len]），且不依赖「空格前后字符是否字母」（来源 [7] 的脆弱点）；
//   * 缓冲区 1 MiB 并全程带长度保护：题面上限 200 字符，远超；任何超长/空输入都不越界、不崩溃；
//   * 语义上等价于「按空格切词后以单个空格连接」，故对「头尾是否有空格」都比主流来源更稳健
//     （行首空格段丢弃、行尾空格段丢弃）；对题面保证的合法数据（头尾无空格）输出与全部来源一致。
//   * 纯 O(n) 单次扫描，无动态分配。
//
// 字符级核对（题面样例 vs 本实现输出，见 work/sample1.in 与 gen-report.md §3）：
//   输入 "Hello      world.This is    c language."
//   输出 "Hello world.This is c language."（6 空格段→1、4 空格段→1）

#include <cstdio>
#include <cstring>

int main() {
    static char line[1 << 20];  // 题面保证 ≤ 200 字符；1 MiB 为防御性上界

    if (fgets(line, sizeof(line), stdin) == NULL) {
        return 0;  // 空输入：无数据可处理，静默退出（题面保证有一行）
    }

    size_t n = strlen(line);
    // 剥行尾换行（含 CRLF 容错）——只剥行尾的 '\n'/'\r'，不从行内剥任何字符
    while (n > 0 && (line[n - 1] == '\n' || line[n - 1] == '\r')) {
        line[--n] = '\0';
    }

    static char out[1 << 20];
    size_t m = 0;  // 已产出的期望输出长度

    for (size_t i = 0; i < n;) {
        if (line[i] == ' ') {
            // 跳过整段连续空格
            size_t j = i;
            while (j < n && line[j] == ' ') {
                ++j;
            }
            // 仅当「前面已有内容」且「后面还有内容」时，才保留一个空格；
            // 这样行首空格段与行尾空格段自然被丢弃（题面保证头尾无空格，此处为稳健性）
            if (m > 0 && j < n) {
                out[m++] = ' ';
            }
            i = j;
        } else {
            out[m++] = line[i++];  // 非空格字符原样保留（含 '.'、逗号等任意字符）
        }
    }

    out[m] = '\0';
    fputs(out, stdout);
    putchar('\n');  // 行尾换行：仓库惯例，评测忽略行末空白
    return 0;
}
