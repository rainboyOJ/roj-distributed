// 一本通 1706《串包含问题》标程
// 题意：给定 n 个 01 串 s[1..n] 与正整数 m，求长度为 2m 的"反对称"01 串中，
//       包含这 n 个串作为子串的个数，模 998244353。
// 反对称：对任意 1<=i<=|s|，s[i] != s[|s|-i+1]。
//
// 思路（自研，网络未找到本题公开 AC 代码）：
//   长度为 2m 的反对称串由前 m 位 T 完全确定：S = T + ~reverse(T)。
//   因此问题转化为：统计长度为 m 的 01 串 T，使得 S=F(T) 包含所有模式串。
//   一个模式 p 在 S 中出现的位置只有三类：
//     (L) 完全落在左半段  <=> p 是 T 的子串；
//     (R) 完全落在右半段  <=> q = ~reverse(p) 是 T 的子串；
//     (M) 横跨中点。设左侧匹配长度 k (1<=k<=L-1)，则它等价于：
//           T 的后缀 k 位 == p 的前 k 位（A），且
//           T 的后缀 L-k 位 == q 的前 L-k 位（B）。
//         两者同时成立当且仅当"较长者的后缀 == 较短者"且 T 的后缀等于较长者。
//         而 A、B 分别是 p、q 的前缀，所以在 AC 自动机中 A/B 对应的节点
//         一定已经存在（就是 p、q 在 trie 上的前缀节点）。
//   于是把 p、q 作为"任意位置命中"的模式插入 AC 自动机；对每个可行的 k，
//   在"较长前缀"对应的 trie 节点上打上"结尾才命中"的 mid 标记。
//   DP 按 T 从左到右逐位转移，状态 (自动机节点, 已命中模式集合的 bitmask)，
//   末尾再合并 mid 标记，统计 mask 覆盖全部模式的状态。
//
// 复杂度：trie 节点数 <= 1 + 2*sum|s_i| <= 1201，DP O(m * 节点数 * 2^n * 2)。
//
// 参考来源 URL：无公开解法来源（网络搜索未找到本题题解，思路为自研推导）。

#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <algorithm>
using namespace std;

static const int MOD = 998244353;

struct Node {
    int ch[2];
    int fail;
    int endAny;   // 以该节点结尾的"任意位置命中"模式 bitmask（p 或 q）
    int midMask;  // 以该节点为后缀才命中（横跨中点）的模式 bitmask
    int hitAll;   // 沿 fail 链累积的 endAny
    int midAll;   // 沿 fail 链累积的 midMask
    Node() : fail(0), endAny(0), midMask(0), hitAll(0), midAll(0) {
        ch[0] = ch[1] = 0;
    }
};

static vector<Node> tr;

static int newNode() {
    tr.emplace_back();
    return (int)tr.size() - 1;
}

static string reverseComp(const string& s) {
    string t = s;
    reverse(t.begin(), t.end());
    for (char& c : t) c = (c == '0') ? '1' : '0';
    return t;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<string> s(n);
    for (int i = 0; i < n; ++i) cin >> s[i];

    tr.clear();
    tr.emplace_back(); // root = 0

    vector<vector<int>> pNode(n), qNode(n);
    int fullMask = 0;

    // 插入 p 与 q
    for (int j = 0; j < n; ++j) {
        if (s[j].empty()) continue; // 空串恒被包含，不产生约束（数据中应不存在）
        fullMask |= (1 << j);

        string q = reverseComp(s[j]);

        pNode[j].assign(s[j].size() + 1, 0);
        int cur = 0;
        for (int i = 0; i < (int)s[j].size(); ++i) {
            int c = s[j][i] - '0';
            if (!tr[cur].ch[c]) tr[cur].ch[c] = newNode();
            cur = tr[cur].ch[c];
            pNode[j][i + 1] = cur;
        }
        tr[cur].endAny |= (1 << j);

        qNode[j].assign(q.size() + 1, 0);
        cur = 0;
        for (int i = 0; i < (int)q.size(); ++i) {
            int c = q[i] - '0';
            if (!tr[cur].ch[c]) tr[cur].ch[c] = newNode();
            cur = tr[cur].ch[c];
            qNode[j][i + 1] = cur;
        }
        tr[cur].endAny |= (1 << j);
    }

    // 打横跨中点的 mid 标记
    for (int j = 0; j < n; ++j) {
        int L = (int)s[j].size();
        if (L < 2) continue;
        string p = s[j];
        string q = reverseComp(p);
        for (int k = 1; k <= L - 1; ++k) {
            string A = p.substr(0, k);          // 左侧匹配 k 位
            string B = q.substr(0, L - k);      // 右侧匹配 L-k 位
            if (k > L - k) {
                // 较长者是 A（p 的前缀，长度 k）
                if (A.substr(k - (L - k)) == B) {
                    tr[pNode[j][k]].midMask |= (1 << j);
                }
            } else {
                // 较长者是 B（q 的前缀，长度 L-k）
                if (B.substr((L - k) - k) == A) {
                    tr[qNode[j][L - k]].midMask |= (1 << j);
                }
            }
        }
    }

    // 构建 fail 指针（BFS），并顺带累积 hitAll / midAll
    queue<int> que;
    tr[0].hitAll = tr[0].endAny;
    tr[0].midAll = tr[0].midMask;
    for (int c = 0; c < 2; ++c) {
        int v = tr[0].ch[c];
        if (v) {
            tr[v].fail = 0;
            que.push(v);
        } else {
            tr[0].ch[c] = 0;
        }
    }
    while (!que.empty()) {
        int u = que.front();
        que.pop();
        tr[u].hitAll = tr[u].endAny | tr[tr[u].fail].hitAll;
        tr[u].midAll = tr[u].midMask | tr[tr[u].fail].midAll;
        for (int c = 0; c < 2; ++c) {
            int v = tr[u].ch[c];
            if (v) {
                tr[v].fail = tr[tr[u].fail].ch[c];
                que.push(v);
            } else {
                tr[u].ch[c] = tr[tr[u].fail].ch[c];
            }
        }
    }

    int nodes = (int)tr.size();
    int states = 1 << n;
    vector<int> dp((size_t)nodes * states, 0), ndp((size_t)nodes * states, 0);
    dp[0 * states + 0] = 1;

    for (int step = 0; step < m; ++step) {
        fill(ndp.begin(), ndp.end(), 0);
        for (int u = 0; u < nodes; ++u) {
            int base = u * states;
            for (int mask = 0; mask < states; ++mask) {
                int val = dp[base + mask];
                if (!val) continue;
                for (int c = 0; c < 2; ++c) {
                    int v = tr[u].ch[c];
                    int nm = mask | tr[v].hitAll;
                    int& dst = ndp[v * states + nm];
                    dst += val;
                    if (dst >= MOD) dst -= MOD;
                }
            }
        }
        dp.swap(ndp);
    }

    long long ans = 0;
    for (int u = 0; u < nodes; ++u) {
        int base = u * states;
        for (int mask = 0; mask < states; ++mask) {
            if ((mask | tr[u].midAll) == fullMask) {
                ans += dp[base + mask];
                if (ans >= MOD) ans -= MOD;
            }
        }
    }
    cout << ans % MOD << '\n';
    return 0;
}
