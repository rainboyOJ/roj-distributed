// 一本通 2046《【例5.15】替换字母》（目标 ROJ 题号 5048）标程
// ---------------------------------------------------------------------------
// 题意（本包 content.md；官方页 http://ybt.ssoier.cn:8088/problem_show.php?pid=2046
// 本轮用 curl 实抓核对，题面五节与 content.md 逐字一致，页面显示
// 「时间限制: 1000 ms 内存限制: 65536 KB」，与 config.json 的 time=1000 / memory=64MB 一致）：
//   【题目描述】在应用计算机编辑文档的时候，我们经常遇到替换任务。如把文档中的
//               “电脑”都替换成“计算机”。现在请你编程模拟一下这个操作。
//   【输入】输入两行内容，第 1 行是原文（长度不超过 200 个字符），第 2 行包含以空格
//           分隔的两个字符 A 和 B，要求将原文中所有的字符 A 都替换成字符 B，
//           注意：区分大小写字母。
//   【输出】一行，输出替换后的结果。
//   【输入样例】I love China. I love Beijing. / I U
//   【输出样例】U love China. U love Beijing.
//
// 参考来源 URL（本轮均用 curl 实取正文后改写，未盲抄；正文留存于 work/sources/）：
//   [1] https://blog.csdn.net/lq1990717/article/details/122375391
//       君义NOIP《信息学奥赛一本通 2046：【例5.15】替换字母》。给出四种等价解法：
//       ① char 数组：`cin.getline(s,205)` + `cin>>a>>b` + 原地 `s[i]=b` + `cout<<s`；
//       ② string：`getline(cin,s)` + `cin>>a>>b` + 原地替换 + `cout<<s`；
//       ③④ 同样两种输入的「逐字符输出」写法（命中 A 就输出 B，否则输出原字符）。
//       该文并点明考点 = 字符数组 / string 类 / **读入带空格的字符串**
//       （C++14 起 C 的 gets() 已不可用，替代品是 cin.getline / getline(cin,·)）。
//   [2] https://blog.csdn.net/lvcheng0309/article/details/117299422
//       《信息学奥赛一本通（2046：【例5.15】替换字母）》。给出 C 版（`gets(s)` +
//       `scanf("%c %c",&old,&new)` + 原地替换 + `puts(s)`）与 C++ 版
//       （`getline(cin,s)` + `cin>>c1>>c2` + 命中即 `cout<<c2` 否则 `cout<<s[i]` + `cout<<endl`）。
//   [3] https://blog.csdn.net/sy820413/article/details/133871359
//       《【信息学奥赛一本通】2046：【例5.15】替换字母》。`char s[1000];`
//       `cin.getline(s,1000); cin>>a>>b; len=strlen(s);` 遍历「命中输出 b、否则输出 s[i]」；
//       【题目考点】同样写明「本题考了利用 cin.getline(,) 可以输入空格」。
//   [4] https://blog.csdn.net/xiaobino_o/article/details/146255852
//       《2046：【例5.15】替换字母--getline、取地址》。`getline(cin, s)` + `cin>>a>>b`，
//       用 `for (auto &i : s) if (i==a) i=b;` 原地改，并强调「必须用 getline 才能正确处理
//       原文中的空格」；输出 `cout << s << endl`。
//   [5] https://blog.csdn.net/2301_77117031/article/details/129719840
//       《2046【例5.15】替换字母(c++)》。getline + cin>>c>>b + 遍历原地改 + 逐字符输出。
//   [6] https://blog.csdn.net/gexuze1761/article/details/129652624
//       《2046：【例5.15】替换字母》（含题面转载）。`getline(cin,a); cin>>y>>t;`
//       `for(i=0;i<=a.size()-1;i++) if(a[i]==y)a[i]=t;` 后 `cout<<a;`（无行末 endl）。
//   [7] https://blog.csdn.net/jtc110716/article/details/122636369
//       《c++2046替换字母》。与 [6] 同构（string + getline + cin>>y>>t + 原地替换 + cout<<a）。
//   [8] https://blog.csdn.net/qq_45083002/article/details/132401608
//       《C++信息学奥赛2046：【例5.15】替换字母》。逐行注释版：`getline(cin, s)` 保证原文
//       含空格也能整行读入，`cin>>a>>b` 读两个字符，遍历 `if(s[i]==a) s[i]=b;`，`cout<<s`。
//
// 多来源结论核对（无冲突）：8 个来源的算法完全一致 —— **整行读入原文（含空格）→ 读入两个
//   （非空白）字符 A、B → 把原文中所有等于 A 的字符改成 B（大小写敏感）→ 整行输出**。
//   差异仅在：① 行读取方式（cin.getline(char[n]) / getline(cin,string) / gets）；
//   ② 改字符还是「命中原样逐字输出」；③ 输出是否补 endl；④ 用 char 数组还是 string。
//   这些差异在「第 1 行一行原文、第 2 行 `A B`」的输入下完全等价。
//   题面无歧义、无需停下确认（与题面冲突的写法为零；来源 [2] 的 C 版 gets 只是过时 API，
//   语义与其余来源相同）。
//
// 由来源反推的两条**数据约束**（决定 data.py 的取值，见 gen-report.md）：
//   * 全部 8 个来源都用 `cin>>a>>b` 或 `scanf("%c %c")` 读 A、B —— 这两种读法都会跳过空白，
//     所以官方数据里 A、B **不可能是空白字符**（否则这些 AC 代码不可能通过）。
//     本包因此只用**非空白可见 ASCII** 作 A、B；
//   * 全部来源都用「整行读取」原文 —— 原文**可以含空格**（题面样例本身就含空格）。
//     本包数据因此允许原文含空格（含连续空格、行首空格），但避免行尾空格（见 gen-report.md 风险点）。
//     另：A/B 是 `char`，8 个来源都无法表达多字节字符，故数据只用 ASCII 原文（同见风险点）。
//
// 本标程相对来源的改写点（不逐字复制任何一份来源）：
//   * 输入用 `fgets` 读**整行**（等价于 [1] 的 getline 路线），剥行尾 '\n'/'\r'
//     （CRLF 容错，来源均未处理）；
//   * 第 2 行用「跳过空白取第 1 个非空白字符 = A，再跳过空白取下一个非空白字符 = B」解析，
//     因而 `A B`、`A  B`、`AB` 三种书写都得到同一结果（与 `cin>>a>>b` 行为一致，见上）；
//   * 替换用**原地逐字节扫描**（[1]①②/[4]/[5]/[6]/[7] 的路线），O(n) 时间、O(1) 额外空间；
//   * 输出统一「原文（已替换）+ 恰一个 '\n'」，行末不留多余空格（比部分来源更严格）；
//   * 缓冲区 1 MiB 并全程长度保护：题面上限 200 字符，超出 5000 倍，即使数据源与实际
//     题面不一致（真数据更长）也不会截断/越界/崩溃；空输入、空行、缺第 2 行、超长输入
//     都安全（缺 B 时保守地原样输出，见下方 `hasB`）。
// ---------------------------------------------------------------------------
#include <cstdio>
#include <cstring>

namespace {

// 输入缓冲上限：题面上限 200 字符，1 MiB 预留约 5000 倍余量（防御性，不影响语义）
constexpr size_t kBufSize = 1u << 20;

// 题面真正的空白判定：空格 / 制表 / 换行 / 回车 / 垂直制表 / 换页
// （不用 ctype 的 isspace，避免负值入参的未定义行为）
inline bool isBlank(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\v' || c == '\f';
}

}  // namespace

int main() {
    // ---- 第 1 行：原文（可含空格，故必须整行读取）----
    static char text[kBufSize];  // 题面保证 <= 200 字符；1 MiB 是防御性余量
    if (fgets(text, sizeof(text), stdin) == NULL) {
        return 0;  // 完全没有输入：没有内容可输出（题面保证必有两行）
    }
    size_t n = strlen(text);
    while (n > 0 && (text[n - 1] == '\n' || text[n - 1] == '\r')) {
        text[--n] = '\0';  // 剥行尾换行 / CRLF 的 '\r'
    }

    // ---- 第 2 行：以空格分隔的两个字符 A 和 B ----
    static char line2[kBufSize];
    char A = '\0', B = '\0';
    bool hasA = false, hasB = false;
    if (fgets(line2, sizeof(line2), stdin) != NULL) {
        size_t m = strlen(line2), i = 0;
        while (i < m && isBlank(line2[i])) ++i;  // 跳到 A
        if (i < m) {
            A = line2[i++];
            hasA = true;
        }
        while (i < m && isBlank(line2[i])) ++i;  // 跳到 B
        if (i < m) {
            B = line2[i++];
            hasB = true;
        }
    }

    // ---- 替换：把原文中所有字符 A 换成 B（区分大小写）----
    // A 与 B 都读到才替换：若第 2 行缺 B（题面保证不会），缺省语义取「不做替换」，
    // 保证不会把字符错改成 '\0' 而截断输出。
    if (hasA && hasB) {
        for (size_t i = 0; i < n; ++i) {
            if (text[i] == A) {
                text[i] = B;
            }
        }
    }

    // ---- 输出：一行结果 + 恰一个 '\n'（行末无多余空白）----
    fputs(text, stdout);
    putchar('\n');
    return 0;
}
