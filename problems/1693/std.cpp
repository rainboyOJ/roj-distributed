// 一本通 1693《正确答案》
// 题面：n 个人各答 m 道判断题（答案 N/Y），其中恰有 p 个人满分（答案串 == 标准答案），
//       q 个人零分（答案串 == 标准答案的反串/补串），其余人既非满分也非零分。
//       求字典序最小的标准答案串，无解输出 -1。
//
// 思路来源（同一题 jzoj 3888《正确答案》的题解）：
//   https://blog.csdn.net/g2523054231/article/details/103019146
//   该文给出三种情况：p,q>0 时找 cnt==p 且反串 cnt==q 的串；
//   q>p=0 时用反串补；p=q=0 时找字典序最小缺失串。
//   本文按其思路改写并补齐 p=q=0 的贪心构造（原文第三段被截断，此处自行推导）。
//
// 算法：
//   * 统计每个答案串出现次数 cnt。
//   * p>0：标准答案必是某个出现恰 p 次的串 S，再要求 cnt[comp(S)]==q，
//          枚举所有候选取字典序最小。
//   * p==0 && q>0：标准答案 S 不在输入中出现（cnt[S]==0），且 comp(S) 出现恰 q 次，
//          故 S=comp(x)，枚举 cnt[x]==q 的 x，取字典序最小。
//   * p==0 && q==0：S 与 comp(S) 都不得出现在输入中。把「禁止集合」看作
//          A ∪ comp(A)（A 为去重后的答案串集合）。用贪心逐位构造字典序最小串：
//          前缀 P 能继续扩展到合法全长串，当且仅当「以 P 为前缀的禁止串个数」
//          小于 2^(剩余长度)。用排序 + 二分求前缀计数。
//
// 复杂度：O(n*m + K*m) 量级，n<=30000, m<=500，轻松通过 1s 限制。

#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
using namespace std;

static inline string comp(const string &s) {
    string t = s;
    for (char &c : t) c = (c == 'N') ? 'Y' : 'N';
    return t;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, p, q;
    if (!(cin >> n >> m >> p >> q)) return 0;

    vector<string> raw(n);
    unordered_map<string, int> cnt;
    cnt.reserve((size_t)n * 2);
    for (int i = 0; i < n; i++) {
        cin >> raw[i];
        cnt[raw[i]]++;
    }

    string ans;
    bool found = false;

    if (p > 0) {
        // 标准答案必是出现次数恰为 p 的串
        for (const auto &kv : cnt) {
            if (kv.second == p) {
                string t = comp(kv.first);
                auto it = cnt.find(t);
                int c = (it == cnt.end()) ? 0 : it->second;
                if (c == q) {
                    if (!found || kv.first < ans) {
                        ans = kv.first;
                        found = true;
                    }
                }
            }
        }
    } else if (q > 0) {
        // p==0：标准答案不出现；它的反串出现恰 q 次
        for (const auto &kv : cnt) {
            if (kv.second == q) {
                string s = comp(kv.first);
                if (cnt.find(s) == cnt.end()) {  // cnt[s] == 0
                    if (!found || s < ans) {
                        ans = s;
                        found = true;
                    }
                }
            }
        }
    } else {
        // p==0 && q==0：标准答案及其反串都不能出现在输入中
        // 禁止集合 F = A ∪ comp(A)（去重）。
        vector<string> f;
        {
            vector<string> tmp;
            for (const string &x : raw) {
                tmp.push_back(x);
                tmp.push_back(comp(x));
            }
            sort(tmp.begin(), tmp.end());
            tmp.erase(unique(tmp.begin(), tmp.end()), tmp.end());
            f.swap(tmp);
        }

        // 以 pref 为前缀的 F 中串的个数
        auto prefixCount = [&](const string &pref) -> long long {
            int d = (int)pref.size();
            if (d == 0) return (long long)f.size();
            auto lo = lower_bound(f.begin(), f.end(), pref);
            string hi = pref;
            hi.append(m - d, 'Z');  // 'Z' > 'Y'，区间 [pref, pref+ZZZ..) 即所有前缀为 pref 的串
            auto up = upper_bound(f.begin(), f.end(), hi);
            return (long long)(up - lo);
        };

        auto cap = [](int e) -> unsigned long long {
            if (e >= 63) return ~0ULL;
            return 1ULL << e;
        };

        string s;
        bool ok = true;
        for (int d = 0; d < m; d++) {
            int rem = m - d - 1;  // 选出本字符后还剩几位
            bool chosen = false;
            for (char ch : {'N', 'Y'}) {  // 贪心先试 'N'，保证字典序最小
                string pref = s + ch;
                long long bad = prefixCount(pref);  // 以 pref 为前缀的禁止串个数
                unsigned long long need = cap(rem);
                if ((unsigned long long)bad < need) {
                    s.push_back(ch);
                    chosen = true;
                    break;
                }
            }
            if (!chosen) {
                ok = false;
                break;
            }
        }
        if (ok) {
            ans = s;
            found = true;
        }
    }

    if (found) {
        cout << ans << '\n';
    } else {
        cout << "-1\n";
    }
    return 0;
}
