// 一本通 1699《石环》标程
// 参考解法来源：博客园 youlv《[题目记录]一本通高手训练-石环》
//   https://www.cnblogs.com/youlv/p/18592015
// 思路（已改写并自证）：
//   把环复制一遍 s2 = s + s（长度 2n）。在环上拿走 k 个连续石头，
//   等价于在 s2 上保留一段长为 m = n - k 的连续子串。
//   s2 中相邻相同的位置是"断点"，把 s2 切成若干段；一段内部任意子串的
//   相邻字符都两两不同。剩下的环美丽只需再保证"首尾字符不同"。
//   对长度为 len 的段，长为 m 的子串共有 len-m+1 个；"所有长为 m 的
//   子串首尾都相同" 等价于 该段存在长度为 len-m+1 的 border（前后缀相等），
//   即 KMP 前缀函数的 border 链。m=1（只剩 1 个石头）无相邻对，恒美丽。
//   因此：先给每个 m 计数 +1，再对每条 border 长度 b 把 m=len-b+1 减 1；
//   最后 m 的计数 >0 表示存在合法方案。
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    int caseNo = 0;
    while (cin >> s) {
        caseNo++;
        int n = (int)s.size();
        string s2 = s + s;          // 环展开为 2n 的线性串
        int N = 2 * n;

        vector<int> res(n + 1, 0);  // res[m]：剩 m 个石头可行段的净计数
        vector<int> pi(N + 1, 0);   // 每段内的 KMP 前缀函数（复用）

        // 处理 s2 上的一个段 [l, r]（0-indexed，闭区间）
        auto process = [&](int l, int r) {
            int L = r - l + 1;
            // KMP 前缀函数，pi[i] = 段内前 i 个字符的最长真 border 长度
            pi[0] = 0;
            pi[1] = 0;
            for (int i = 2; i <= L; i++) {
                int j = pi[i - 1];
                while (j > 0 && s2[l + i - 1] != s2[l + j]) j = pi[j];
                if (s2[l + i - 1] == s2[l + j]) j++;
                pi[i] = j;
            }
            // 先认为每个长度 m 都可从本段取到
            int cap = min(L, n);
            for (int m = 1; m <= cap; m++) res[m]++;
            // 对每条真 border 长度 b，m = L - b + 1 的所有子串首尾都相同，
            // 该长度从本段不可行，扣掉。
            int j = pi[L];
            while (j > 0) {
                int m = L - j + 1;
                if (m <= n) res[m]--;
                j = pi[j];
            }
        };

        int l = 0;
        for (int i = 1; i < N; i++) {
            if (s2[i] == s2[i - 1]) {   // 相邻相同 -> 断点
                process(l, i - 1);
                l = i;
            }
        }
        process(l, N - 1);

        cout << "Case " << caseNo << ": ";
        for (int k = 0; k < n; k++) {
            int m = n - k;               // 拿走 k 个后剩 m 个
            cout << (res[m] > 0 ? '1' : '0');
        }
        cout << '\n';
    }
    return 0;
}
