// 1800 质数 —— 标准程序
// 题意：将 1..n 分成尽可能少的集合，使每个集合的元素和均为质数；输出集合数与方案（任意方案），无解输出 -1。
//
// 算法（基于哥德巴赫猜想的结论，n<=6000 时结论经计算全部成立）：
//   记 S = n*(n+1)/2。
//   1) n == 1：S = 1 不是质数，任何划分都不可行 -> 输出 -1（唯一无解情形）。
//   2) S 是质数 -> cnt = 1（1..n 全部放一个集合）。只有 n = 2 时 S = 3 为质数。
//   3) 否则若存在质数 p 使 p 与 S-p 均为质数 -> cnt = 2：
//        S 为偶数时由哥德巴赫猜想（已大量数值验证）必有这样的分解；
//        S 为奇数时两质数之和必为偶数，只能 p = 2 且 S-2 为质数。
//      方案：{1..n} 中贪心取一个和为 p 的子集（n 往下取，剩余需求 rem 恒 <= sum(1..i)，
//      故必然恰好取满），补集和即 S-p（质数）。
//   4) 否则 cnt = 3：取互不相同的质数 a,b <= n 使 S-a-b 仍为质数，
//      令集合 1 = {a}、集合 2 = {b}、集合 3 = 其余元素（和恰为 S-a-b，为质数）。
//      依据：任一大于 5 的整数可写成三个质数之和（哥德巴赫弱猜想，已验证），
//      且 n>=18 时总能搜到满足条件的 (a,b)。
//   答案只可能是 -1/1/2/3，且最小性由"质数和"的素数个数下界直接给出。
//
// 参考来源（网络题解；题意/结论来源，代码为自行重写实现，并经样例与合法性校验）：
//   1. https://blog.csdn.net/qq_35866453/article/details/74806673
//      《【GDOI2018模拟7.8】质数 乱搞+哥德巴赫猜想》——题面与本题完全一致
//      （"将 1-n 中的数字分成尽量少的集合，使得每个集合的和都为素数，n<=6000"），
//      给出同一结论：S 为素数->1；S 可写成两素数之和->2；否则由哥德巴赫猜想->3；找不到则 -1。
//   2. https://blog.csdn.net/u011056504/article/details/74906040
//      《【GDOI2018模拟7.8】质数》（同题，另一份题解/实现，用于交叉确认结论）
//   3. https://blog.csdn.net/last_freezen_yue/article/details/75145368
//      《质数,函数【GDOI2018模拟7.8】》（同题，第三份题解）
// 复杂度：埃氏筛 O(S log log S) + 决策 O(S)，S <= 18003000，实测远低于 1000 ms / 256 MB。
#include <cstdio>
#include <vector>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    if (n == 1) {           // S = 1 非质数，唯一无解情形
        printf("-1\n");
        return 0;
    }

    const long long S = 1LL * n * (n + 1) / 2;   // 元素总和，n<=6000 -> S<=18003000

    // 埃氏筛：筛出 [0, S] 的合数标记
    vector<char> comp(S + 1, 0);
    comp[0] = comp[1] = 1;
    for (long long i = 2; i * i <= S; ++i)
        if (!comp[i])
            for (long long j = i * i; j <= S; j += i) comp[j] = 1;

    vector<int> ans(n + 1, 0);

    if (!comp[S]) {         // 情况 2：总和为质数 -> 1 个集合
        printf("1\n");
        for (int i = 1; i <= n; ++i) printf("1%c", i == n ? '\n' : ' ');
        return 0;
    }

    // 情况 3：找质数 p，使 p 与 S-p 均为质数 -> 2 个集合
    long long p = -1;
    for (long long x = 2; x <= S / 2; ++x)
        if (!comp[x] && !comp[S - x]) { p = x; break; }

    if (p != -1) {
        // 贪心构造和为 p 的子集（从 n 往下取）
        long long rem = p;
        for (int i = n; i >= 1 && rem > 0; --i)
            if (i <= rem) { ans[i] = 1; rem -= i; }
        for (int i = 1; i <= n; ++i)
            if (ans[i] == 0) ans[i] = 2;
        printf("2\n");
        for (int i = 1; i <= n; ++i) printf("%d%c", ans[i], i == n ? '\n' : ' ');
        return 0;
    }

    // 情况 4：cnt = 3，取互异质数 a,b <= n 且 S-a-b 为质数
    vector<int> pr;
    for (int i = 2; i <= n; ++i)
        if (!comp[i]) pr.push_back(i);

    long long a = -1, b = -1;
    for (size_t i = 0; i < pr.size() && a < 0; ++i) {
        for (size_t j = 0; j < pr.size(); ++j) {
            if (pr[j] == pr[i]) continue;
            if (!comp[S - pr[i] - pr[j]]) { a = pr[i]; b = pr[j]; break; }
        }
    }

    if (a < 0) {            // 理论上有解，兜底输出 -1
        printf("-1\n");
        return 0;
    }

    for (int i = 1; i <= n; ++i) ans[i] = 3;
    ans[a] = 1;
    ans[b] = 2;
    printf("3\n");
    for (int i = 1; i <= n; ++i) printf("%d%c", ans[i], i == n ? '\n' : ' ');
    return 0;
}
