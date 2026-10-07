// 一本通 1692 字符串编码
// 参考来源：无公开解法来源（检索 CSDN 站内搜索 / 博客园 / Bing / DuckDuckGo 均未找到本题
// 现成 AC 代码，仅找到高手训练篇题解目录
//   https://blog.csdn.net/qq_36230375/article/details/136483654
// 与本题官方题面 http://ybt.ssoier.cn:8088/problem_show.php?pid=1692 ）。
// 以下为依据题面（并经两个样例校准语义）自研的解法。
//
// 题意：选取若干对互不相交的小写字母对（每个字母至多出现一次），编码时把串中每个被选中
// 的字母换成其配对字母（对换 a<->b）；未被选中的字母保持不变（由样例1位置5不合法、
// 位置7合法可确认此语义）。求 S 有多少个子串能编码成 T，升序输出起点（1-based）。
//
// 正确性论证：
//  设编码对应映射 f。f 必须满足：
//   (1) f 在"出现的字母"上是双射（字母对互不相交，一个字母不会被两个来源映射）；
//   (2) 对合性：若 a、b 都在子串 U 中出现且 f(a)=b，则必有 f(b)=a（a,b 构成一对）。
//       若 f(a)=b 而 b 不在 U 中出现，则选上字母对 (a,b) 即可，无额外约束。
//  因此子串 U 可编码为 T 当且仅当：
//   (A) U 与 T "模式同构"：存在不同字母间的双射 g 使 g(U[j])=T[j] 对所有 j 成立；
//   (B) 诱导双射 g 满足对合条件：a、b 都在 U 中出现且 g(a)=b 时 g(b)=a。
//  判定 (A) 用 Baker 参数化匹配的 prev 编码：prevX[i] = i 减去 X[i] 上一次出现的位置
//  （未出现过为 0）。经典结论：X 与 Y 模式同构当且仅当 prev 数组逐位相等。
//  对 S 的窗口 [p,p+m-1]，窗口内第 j 位的编码值为
//      e_p(j) = prevS[p+j-1]  （若 prevS[p+j-1] < j，即前一次出现落在窗口内）
//             = 0             （否则）。
//  用双 rolling hash 比较 e_p 与 prevT：H_p = Σ_j B^{m-j}·e_p(j)（64 位自然溢出，两组
//  独立基数）。窗口右移时，注意到 prevpos(i)=i-prevS[i] 在 {i: prevS[i]>0} 上是单射
//  （prevpos(i)=k 要求 S[i]=S[k]），故每次滑动至多有一个下标 i*（prevpos(i*)=p）的编码
//  值从 i*-p 变为 0，其余不变；于是
//      H_{p+1} = (H_p - B^{m-1}·e_p(1))·B + e_{p+1}(m) - B^{m-j'}·(i*-p)
//  其中 e_p(1) 恒为 0，j'=i*-p，全部 O(1) 维护。
//  哈希相等的候选窗口再做判定 (B)：预处理 firstPos[p][a] = 字母 a 在位置 ≥p 的首次出现
//  （O(26n) 建表），对窗口内每个出现字母 a，取其窗内首现位置 j_a，令 b=T[j_a]；若 b 也
//  在窗内出现（首现 j_b），检查 T[j_b]=a。每窗 O(26)。
//  总复杂度 O(26n + n + m)，双 64 位哈希碰撞概率约 2^-128，可忽略。
#include <cstdio>
#include <cstring>
#include <vector>
using namespace std;

typedef unsigned long long ull;

const int MAXN = 200005;
const int INF = 1 << 30;

int n, m;
char S[MAXN], T[MAXN];      // 1-based
int pvS[MAXN], pvT[MAXN];
int nxtIdx[MAXN];           // prevpos(i)=p 的唯一 i（无则 0）
ull pw1[MAXN], pw2[MAXN];
int (*fp)[26];              // firstPos[p][a]

int main() {
    scanf("%d %d", &n, &m);
    scanf("%s %s", S + 1, T + 1);

    // prev 编码
    {
        int last[26];
        memset(last, 0, sizeof(last));
        for (int i = 1; i <= n; i++) {
            int c = S[i] - 'a';
            pvS[i] = last[c] ? i - last[c] : 0;
            last[c] = i;
        }
        memset(last, 0, sizeof(last));
        for (int i = 1; i <= m; i++) {
            int c = T[i] - 'a';
            pvT[i] = last[c] ? i - last[c] : 0;
            last[c] = i;
        }
    }
    for (int i = 1; i <= n; i++)
        if (pvS[i] > 0) nxtIdx[i - pvS[i]] = i; // prevpos 单射

    // 哈希基数与幂
    ull B1 = 91138233ULL, B2 = 97266353ULL;
    pw1[0] = pw2[0] = 1;
    for (int i = 1; i <= m; i++) { pw1[i] = pw1[i - 1] * B1; pw2[i] = pw2[i - 1] * B2; }

    // T 的哈希
    ull HT1 = 0, HT2 = 0;
    for (int j = 1; j <= m; j++) {
        HT1 = HT1 * B1 + (ull)pvT[j];
        HT2 = HT2 * B2 + (ull)pvT[j];
    }
    // 注：H_p 也按 H = Σ B^{m-j} e(j) 累积，与上式同构（e(j) 依次左移进位）。

    // firstPos 表：fp[p][a] = 字母 a 在 ≥p 的首次出现（无则 INF）
    fp = new int[n + 2][26];
    for (int a = 0; a < 26; a++) fp[n + 1][a] = INF;
    for (int p = n; p >= 1; p--) {
        memcpy(fp[p], fp[p + 1], sizeof(fp[p]));
        fp[p][S[p] - 'a'] = p;
    }

    vector<int> ans;
    // 初始窗口 p=1 的哈希（窗口不足 m 长时也先算前 min(m,n) 位无意义，仅当 n>=m 使用）
    ull H1 = 0, H2 = 0;
    if (n >= m) {
        for (int j = 1; j <= m; j++) {
            ull e = (pvS[j] < j) ? (ull)pvS[j] : 0ULL;
            H1 = H1 * B1 + e;
            H2 = H2 * B2 + e;
        }
    }
    for (int p = 1; p + m - 1 <= n; p++) {
        if (H1 == HT1 && H2 == HT2) {
            // 判定 (B)：诱导双射的对合条件
            bool ok = true;
            for (int a = 0; a < 26 && ok; a++) {
                int ia = fp[p][a];
                if (ia > p + m - 1) continue;       // a 不在窗内
                int b = T[ia - p + 1] - 'a';        // g(a)
                if (b == a) continue;
                int ib = fp[p][b];
                if (ib > p + m - 1) continue;       // b 不在窗内：选 (a,b) 即可
                if (T[ib - p + 1] != char('a' + a)) ok = false; // 需 g(b)=a
            }
            if (ok) ans.push_back(p);
        }
        // 滑动到 p+1
        if (p + m <= n) {
            // e_p(1) 恒 0，无需减首项；整体左移一位（乘 B）并加入新右端 e_{p+1}(m)
            ull eNew = (pvS[p + m] < m) ? (ull)pvS[p + m] : 0ULL;
            H1 = H1 * B1 + eNew;
            H2 = H2 * B2 + eNew;
            // 修正唯一可能变化的下标 i*（prevpos(i*)=p，且仍在新窗内）
            int is = nxtIdx[p];
            if (is && is <= p + m - 1) {
                int jp = is - p;                    // 新窗内相对下标
                ull d = (ull)(is - p);              // 旧编码值
                H1 -= pw1[m - jp] * d;
                H2 -= pw2[m - jp] * d;
            }
        }
    }

    printf("%d\n", (int)ans.size());
    for (size_t i = 0; i < ans.size(); i++)
        printf("%d%c", ans[i], i + 1 == ans.size() ? '\n' : ' ');
    return 0;
}
