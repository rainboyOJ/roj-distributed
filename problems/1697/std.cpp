// 一本通 1697《深意》
// 题意：单词 t 有两种含义（原意与"深意"）。串 s 中出现的每一处 t 都可以选择取
//       原意或取深意（取深意即该处内容被替换成另一种含义，视为不同），求 s 的
//       不同含义总数，对 1e9+7 取模。
//
// 思路（同型经典题 HDU 5763 Another Meaning，KMP + 线性 DP）：
//   预处理 t 在 s 中的所有出现位置（KMP，O(|s|+|t|)）；
//   设 dp[i] = 前 i 个字符构成的前缀的含义数，dp[0]=1：
//     dp[i] = dp[i-1]                （第 i 位结尾处没有出现 t，末尾不替换）
//     dp[i] += dp[i-m]  (若 s[i-m+1..i] = t)（末尾这段 t 取深意）
//   答案 dp[n]。非重叠/重叠均自动正确：末尾取深意的那段是"恰好以 i 结尾的匹配"，
//   前面部分沿用 dp[i-m]，不重不漏。
//
// 参考来源：
//   - https://blog.csdn.net/zwj1452267376/article/details/52068827 （HDOJ 5763 题解）
//   - https://blog.csdn.net/kevin66654/article/details/52091803 （HDOJ 5763 题解）
//   本题（一本通 1697）未搜到独立公开 AC 代码，按上述同型题思路自研实现并自证：
//   样例 + 暴力对拍（见 work/brute.cpp）均通过。
//
// 复杂度：O(sum(|s|+|t|))，|s|<=1e5, n<=10，远低于 1s 限制。

#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

using namespace std;

typedef long long ll;
const ll MOD = 1000000007LL;
const int MAXN = 100005;

char bufS[MAXN], bufT[MAXN];
int nxt[MAXN];      // t 的 next（fail）数组，1-based 长度语义
int dp[MAXN];      // dp[i]: s 前 i 个字符的含义数
bool occ[MAXN];    // occ[i]: s[i-m+1..i] 恰好等于 t（以 i 结尾存在匹配）

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    while (n--) {
        scanf("%s", bufS);
        scanf("%s", bufT);
        string s = bufS, t = bufT;
        int a = (int)s.size(), b = (int)t.size();

        // KMP 失配指针（对 t 自身）
        nxt[0] = -1;
        for (int i = 0, j = -1; i < b;) {
            if (j == -1 || t[i] == t[j]) nxt[++i] = ++j;
            else j = nxt[j];
        }

        // KMP 扫 s，标记以 i 结尾的完整匹配
        memset(occ, 0, sizeof(bool) * (a + 1));
        for (int i = 0, j = 0; i < a;) {
            if (j == -1 || s[i] == t[j]) {
                ++i; ++j;
                if (j == b) {
                    occ[i] = true;
                    j = nxt[j];
                }
            } else j = nxt[j];
        }

        // DP
        dp[0] = 1;
        for (int i = 1; i <= a; ++i) {
            dp[i] = dp[i - 1];
            if (occ[i]) dp[i] = (int)(((ll)dp[i] + dp[i - b]) % MOD);
        }
        printf("%d\n", dp[a]);
    }
    return 0;
}
