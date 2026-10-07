// 一本通 1696《前缀和》
// 题意：给定字符串 s，求所有长度为偶数的前缀在 s 中出现的次数之和（可重叠）。
//
// 思路来源：
//   1. 与本题同型的经典题 "JZOJ 5178 / SSL_1216 So many prefix?" 思路一致，
//      使用 KMP 的 next（前缀函数）数组 + DP 统计每个前缀出现的总次数。
//   2. CSDN 题解目录确认 1696 位于《高手训练·二、字符串算法·第2章 KMP算法》：
//      https://blog.csdn.net/qq_36230375/article/details/136483654
//   （网络流传实现均已自行验证：样例 1/2 均输出 6 / 30，见 gen-report.md）
//
// 算法（KMP 前缀函数 + 计数）：
//   pi[i]（下方 nxt[i]）为长度 i 的前缀的最长真 border 长度。
//   把每个长度 i 的前缀看作节点，它每作为一次 border 出现，就向父节点 nxt[i]
//   贡献一次出现；再加上自身作为整串起点的那一次。
//   于是从长到短做“子树求和”：cnt[i] = 1 + sum_{j: nxt[j]==i} cnt[j]。
//   实际等价于：cnt 先全置 1，再从 n 到 1 反向 cnt[nxt[i]] += cnt[i]。
//   最后累加长度为偶数的 cnt[i]。
//
// 复杂度 O(|s|)，答案上界约 10^10，用 long long。

#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int n = (int)s.size();

    // nxt[i]：长度 i 的前缀的最长真 border 长度（1-indexed）
    vector<int> nxt(n + 1, 0);
    int k = 0;
    for (int i = 2; i <= n; ++i) {
        while (k > 0 && s[k] != s[i - 1]) k = nxt[k];
        if (s[k] == s[i - 1]) ++k;
        nxt[i] = k;
    }

    // cnt[i]：长度 i 的前缀在整个串中出现的次数（含自身作为整串起点的那一次）
    vector<long long> cnt(n + 1, 1);
    cnt[0] = 0;
    for (int i = n; i >= 1; --i) {
        cnt[nxt[i]] += cnt[i];
    }
    long long ans = 0;
    for (int i = 2; i <= n; i += 2) ans += cnt[i];
    cout << ans << '\n';
    return 0;
}
