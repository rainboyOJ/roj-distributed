// 一本通 1683 《稗田阿求》 标程
// 参考来源: https://www.cnblogs.com/icys/p/15134537.html (博客园 Icys《[一本通1683]稗田阿求》)
// 思路(在来源基础上改写):
//   每组"文字段+数列"给出一个 字母->数字 的部分单射(题面保证组内合法)。
//   两组相容 <=> 同一字母给出的数字不冲突 且 不同字母不映到同一数字。
//   两两相容的若干组合并后仍是一个部分单射(任何冲突必在某一对之间暴露),
//   剩余字母数 == 剩余数字数, 必可补全为 1..N 的一一对应。
//   故答案 = M 个点的相容图上的最大团。M<=40, 用 64 位状压 + 分支限界 DFS。
// 与来源代码的差异/修复说明:
//   - 重写为 C++17 风格, 去除 goto, 逻辑等价;
//   - M<=40 < 64, unsigned long long 掩码无溢出风险;
//   - 剪枝改为 "上界 <= ans 即剪" (取等也无法更优, 直接剪掉, 更快且正确);
//   - 答案最大为 M<=40, int 足够, 无 int 溢出隐患。
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

int n, m;
int mp[45][26];               // mp[i][c]: 第 i 组中字母 c 对应的数字, 0 = 该字母未出现
unsigned long long compat[45]; // compat[i] 第 (j-1) 位为 1 <=> 第 i 组与第 j 组相容
int ans = 0;

void dfs(int u, int cnt, unsigned long long cand) {
    if (cnt + (m - u + 1) <= ans) return; // 后面全选也无法超过当前最优
    if (u > m) { ans = max(ans, cnt); return; }
    if ((cand >> (u - 1)) & 1ULL)         // 第 u 组与已选集合全部相容, 可以选
        dfs(u + 1, cnt + 1, cand & compat[u]);
    dfs(u + 1, cnt, cand);                // 不选第 u 组
}

int main() {
    scanf("%d %d", &n, &m);
    for (int i = 1; i <= m; i++) {
        static char str[128];
        scanf("%s", str);
        int L = (int)strlen(str);
        for (int j = 0; j < L; j++) {
            int v; scanf("%d", &v);
            mp[i][str[j] - 'A'] = v;      // 组内合法, 同字母重复读入的值相同
        }
    }
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= m; j++) {
            if (i == j) continue;
            bool ok = true;
            bool usedNum[27] = {false};
            for (int c = 0; c < 26 && ok; c++) {
                if (mp[i][c] && mp[j][c] && mp[i][c] != mp[j][c]) { ok = false; break; }
                int v = mp[i][c] ? mp[i][c] : mp[j][c];
                if (!v) continue;
                if (usedNum[v]) ok = false;  // 不同字母映到同一数字
                else usedNum[v] = true;
            }
            if (ok) compat[i] |= 1ULL << (j - 1);
        }
    dfs(1, 0, ~0ULL);
    printf("%d\n", ans);
    return 0;
}
